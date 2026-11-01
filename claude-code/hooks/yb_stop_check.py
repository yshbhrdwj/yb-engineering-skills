#!/usr/bin/env python3
"""Run an explicitly opted-in project check once per content state and session."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import signal
import sys
import tempfile


class CheckError(Exception):
    pass


def git(root, *args, allow_unborn=False):
    try:
        result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                                timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckError(f"cannot inspect repository ({type(exc).__name__})") from exc
    if result.returncode:
        if allow_unborn and args == ("rev-parse", "--verify", "HEAD"):
            return b"<unborn>"
        raise CheckError("cannot inspect repository content")
    return result.stdout


def dirty_submodules(root):
    # Git's diff records only "<commit>-dirty", not changes inside dirty submodules.
    status = git(root, "status", "--porcelain=v2", "--ignore-submodules=none", "-z")
    for record in status.split(b"\0"):
        fields = record.split(b" ", 3)
        if len(fields) >= 3 and fields[0] in {b"1", b"2", b"u"}:
            state = fields[2]
            if state.startswith(b"S") and state != b"S...":
                return True
    return False


def fingerprint(root, check):
    digest = hashlib.sha256()
    digest.update(git(root, "rev-parse", "--verify", "HEAD", allow_unborn=True))
    for args in (("ls-files", "--stage", "-z"),
                 ("diff", "--binary", "--no-ext-diff", "--no-textconv"),
                 ("diff", "--cached", "--binary", "--no-ext-diff", "--no-textconv")):
        digest.update(git(root, *args))
        digest.update(b"\0")
    for raw in git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
        if not raw:
            continue
        path = root / os.fsdecode(raw)
        digest.update(raw + b"\0")
        if path.is_symlink():
            digest.update(os.readlink(path).encode())
        elif path.is_file():
            with path.open("rb") as stream:
                while block := stream.read(1024 * 1024):
                    digest.update(block)
        digest.update(b"\0")
    digest.update(check.read_bytes())
    return digest.hexdigest()


def cache_path(root, session):
    if not session:
        return None
    identity = hashlib.sha256((str(root) + "\0" + session).encode()).hexdigest()
    cache = Path(tempfile.gettempdir()) / f"yb-engineering-skills-{getattr(os, 'getuid', lambda: 'user')()}"
    if cache.is_symlink():
        raise CheckError("check cache must not be a symlink")
    cache.mkdir(mode=0o700, exist_ok=True)
    if os.name != "nt" and (cache.stat().st_uid != os.getuid() or cache.stat().st_mode & 0o077):
        raise CheckError("check cache must be private to this user")
    target = cache / f"{identity}.json"
    if target.is_symlink():
        raise CheckError("check cache must not be a symlink")
    return target


def check_timeout(root):
    """Load installation defaults, then the explicitly opted-in project's override."""
    timeout = 120
    installed = Path(__file__).resolve().parents[1] / "yb-hooks.json"
    project = root / ".claude" / "yb-hooks.json"
    for config in dict.fromkeys((installed, project)):
        if not config.exists():
            continue
        try:
            values = json.loads(config.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise CheckError(f"invalid check configuration: {config}") from exc
        if not isinstance(values, dict):
            raise CheckError(f"{config} must contain a JSON object")
        timeout = values.get("check_timeout_seconds", timeout)
    if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
            or not 1 <= timeout <= 300 or not math.isfinite(timeout)):
        raise CheckError("check_timeout_seconds must be finite and between 1 and 300")
    return timeout


def check_command(check, platform=None):
    platform = platform or os.name
    if platform != "nt":
        return [str(check)]
    bash = os.environ.get("CLAUDE_CODE_GIT_BASH_PATH") or shutil.which("bash")
    if not bash:
        raise CheckError(".claude/yb-check.sh requires Bash on Windows; configure Git Bash or run project checks manually")
    return [bash, str(check)]


def terminate_check(process, platform=None):
    if (platform or os.name) == "nt":
        # Killing only bash leaves its check/test children running on Windows.
        try:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           capture_output=True, timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass
        if process.poll() is None:
            process.kill()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=5)


def stop(payload):
    if payload.get("stop_hook_active") is True:
        print("yb-stop-check: retry guard active; report any unresolved check failure honestly", file=sys.stderr)
        return
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_dir():
        return
    try:
        root = Path(git(cwd, "rev-parse", "--show-toplevel").decode().strip())
    except CheckError:
        return
    check = root / ".claude" / "yb-check.sh"
    if (check.is_symlink() or not check.resolve().is_relative_to(root.resolve()) or not check.is_file()
            or (os.name != "nt" and not os.access(check, os.X_OK))):
        return
    timeout = check_timeout(root)
    cacheable = not dirty_submodules(root)
    before = fingerprint(root, check) if cacheable else None
    cache = cache_path(root, payload.get("session_id", ""))
    if cacheable and cache and cache.is_file():
        try:
            if json.loads(cache.read_text()).get("fingerprint") == before:
                return
        except (OSError, ValueError):
            pass
    if cache:
        cache.unlink(missing_ok=True)
    try:
        with tempfile.TemporaryFile() as output_file:
            process = subprocess.Popen(check_command(check), cwd=root, stdout=output_file,
                                       stderr=subprocess.STDOUT, start_new_session=os.name != "nt")
            try:
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                terminate_check(process)
                raise CheckError(f".claude/yb-check.sh exceeded {timeout:g}s; report and resolve the timeout")
            output_file.seek(0, os.SEEK_END)
            output_file.seek(max(0, output_file.tell() - 12000))
            output = output_file.read().decode(errors="replace")
    except OSError as exc:
        raise CheckError("cannot execute opted-in .claude/yb-check.sh") from exc
    if code:
        print(output, file=sys.stderr)
        raise CheckError(f".claude/yb-check.sh failed (exit {code}); fix or report the blocker")
    # A formatter or test may change files. Cache only a checked, stable state.
    if cacheable and cache and not dirty_submodules(root) and fingerprint(root, check) == before:
        with tempfile.NamedTemporaryFile(mode="w", dir=cache.parent, delete=False) as staged:
            temporary = Path(staged.name)
            json.dump({"fingerprint": before}, staged)
        try:
            temporary.replace(cache)
        finally:
            temporary.unlink(missing_ok=True)


def main():
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise CheckError("invalid hook input")
        stop(payload)
    except (CheckError, OSError, ValueError, TypeError) as exc:
        print(f"yb-stop-check: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
