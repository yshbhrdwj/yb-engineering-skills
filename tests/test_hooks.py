"""Behavioral CLI hook tests; GitHub is a local executable stub, never a live merge."""
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MERGE = ROOT / "claude-code/hooks/yb_merge_gate.py"
STOP = ROOT / "claude-code/hooks/yb_stop_check.py"
HEAD = "a" * 40
OTHER = "b" * 40


def isolated_git_environment():
    # A test must never inherit an alternate real index/worktree or user signing
    # policy. Shell oracle checks also avoid arbitrary shell startup files.
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") and key not in {"BASH_ENV", "ENV"}}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
    return env


def evidence():
    return {"number": 7, "state": "OPEN", "isDraft": False, "headRefOid": HEAD,
            "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN", "author": {"__typename": "User", "login": "author"},
            "reviews": {"pageInfo": {"hasNextPage": False}, "nodes": [
                {"state": "APPROVED", "submittedAt": "2026-11-01T10:00:00Z",
                 "author": {"__typename": "Bot", "login": "trusted[bot]"}, "commit": {"oid": HEAD}}]},
            "reviewThreads": {"pageInfo": {"hasNextPage": False}, "nodes": []}}


@unittest.skipIf(os.name == "nt", "CLI executable stub uses a POSIX shebang")
class MergeHookTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="yb-hook-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.git_env = isolated_git_environment()
        subprocess.run(["git", "init", "-q", "-b", "feature/checkout", str(self.repo)], env=self.git_env, check=True)
        (self.repo / ".claude").mkdir()
        (self.repo / ".claude/yb-hooks.json").write_text(json.dumps({"trusted_reviewers": ["trusted[bot]"]}))
        self.fixture = self.root / "fixture.json"
        self.log = self.root / "calls.jsonl"
        self.bin = self.root / "bin"
        self.bin.mkdir()
        executable = self.bin / "gh"
        executable.write_text(f"#!{sys.executable}\n" + r'''
import json, os, sys
from pathlib import Path
f=json.loads(Path(os.environ['MOCK_FIXTURE']).read_text())
a=sys.argv[1:]
with open(os.environ['MOCK_LOG'],'a') as log:log.write(json.dumps(a)+'\n')
if a[:2]==['api','graphql']:
 stage='graphql';pr=f['pr']
 # Match the API selection contract: unrequested actor types are not returned.
 if '__typename' not in next((x for x in a if x.startswith('query=')), ''):
  pr.get('author',{}).pop('__typename',None)
  for review in pr.get('reviews',{}).get('nodes',[]):review.get('author',{}).pop('__typename',None)
 out={'data':{'repository':{'pullRequest':pr}}}
elif a[:2]==['pr','checks']: stage='checks'; out=f.get('checks',[{'name':'test','state':'SUCCESS','bucket':'pass'}])
elif a[:2]==['repo','view']:stage='repo';out={'nameWithOwner':'local/repo','url':'https://github.com/local/repo'}
elif a[:2]==['pr','view'] and a[-1]=='number':
 # gh requires a positional target whenever --repo is present.
 if '--repo' in a and (len(a)<3 or a[2].startswith('-')):
  print('argument required when using the --repo flag',file=sys.stderr);sys.exit(1)
 stage='number';out={'number':7}
elif a[:2]==['pr','view']:stage='fresh';out={'headRefOid':f.get('fresh',f['pr']['headRefOid'])}
else:sys.exit(90)
if f.get('fail')==stage:
 print(f.get('stderr','unavailable'),file=sys.stderr);sys.exit(f.get('exit_code',1))
print(json.dumps(out))
''')
        executable.chmod(0o755)
        self.env = dict(self.git_env, PATH=str(self.bin) + os.pathsep + os.environ.get("PATH", ""),
                        MOCK_FIXTURE=str(self.fixture), MOCK_LOG=str(self.log), PYTHONDONTWRITEBYTECODE="1")
        self.env.pop("GH_REPO", None)
        self.env.pop("GH_HOST", None)
        self.data = {"pr": evidence()}
        self.script = MERGE

    def run_hook(self, command=None, code=0):
        self.fixture.write_text(json.dumps(self.data))
        command = command or f"gh pr merge 7 --squash --match-head-commit {HEAD}"
        result = subprocess.run([sys.executable, str(self.script)], input=json.dumps({
            "cwd": str(self.repo), "tool_name": "Bash", "tool_input": {"command": command}}),
            text=True, capture_output=True, env=self.env, timeout=10)
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_approved_exact_head_and_required_checks_allow_direct_merge(self):
        self.run_hook()
        self.assertEqual(len(self.calls()), 4)
        self.assertFalse(any("mutation" in arg for call in self.calls() for arg in call))

    def test_rejects_stale_and_absent_pin_before_network(self):
        for command in ("gh pr merge 7", f"gh pr merge 7 --match-head-commit {OTHER}"):
            with self.subTest(command=command):
                self.run_hook(command, code=2)

    def test_negative_dismissed_untrusted_self_and_stale_reviews_block(self):
        for change in ({"state": "CHANGES_REQUESTED"}, {"state": "DISMISSED"},
                       {"author": {"__typename": "User", "login": "stranger"}}, {"author": {"__typename": "User", "login": "author"}},
                       {"commit": {"oid": OTHER}}, {"state": "COMMENTED"}):
            with self.subTest(change=change):
                self.data["pr"] = evidence()
                self.data["pr"]["reviews"]["nodes"][0].update(change)
                self.run_hook(code=2)

    def test_latest_decisive_review_overrides_old_approval(self):
        old = self.data["pr"]["reviews"]["nodes"][0]
        later = deepcopy(old)
        later.update(state="CHANGES_REQUESTED", submittedAt="2026-11-01T11:00:00Z")
        self.data["pr"]["reviews"]["nodes"].append(later)
        self.run_hook(code=2)
        latest = deepcopy(later)
        latest.update(state="APPROVED", submittedAt="2026-11-01T12:00:00Z")
        self.data["pr"]["reviews"]["nodes"].append(latest)
        self.run_hook()

    def test_comments_do_not_erase_a_changes_requested_review(self):
        nodes = self.data["pr"]["reviews"]["nodes"]
        negative = deepcopy(nodes[0])
        negative.update(state="CHANGES_REQUESTED", author={"__typename": "User", "login": "another"})
        comment = deepcopy(negative)
        comment.update(state="COMMENTED", submittedAt="2026-11-01T12:00:00Z")
        nodes.extend([negative, comment])
        self.run_hook(code=2)

    def test_issue_comment_or_reaction_never_substitutes_for_approval(self):
        self.data["pr"]["reviews"]["nodes"] = []
        for body in ("Didn't find any major issues", "I found major issues", ":+1:"):
            self.data["comments"] = [{"body": body, "author": {"__typename": "Bot", "login": "trusted[bot]"}}]
            self.run_hook(code=2)
        self.assertFalse(any("comments" in call for call in self.calls()))

    def test_threads_pagination_draft_closed_and_conflicts_block(self):
        mutations = [lambda p:p["reviewThreads"]["nodes"].append({"isResolved": False}),
                     lambda p:p["reviews"]["pageInfo"].update(hasNextPage=True),
                     lambda p:p["reviewThreads"]["pageInfo"].update(hasNextPage=True),
                     lambda p:p.update(isDraft=True), lambda p:p.update(state="CLOSED"),
                     lambda p:p.update(mergeable="UNKNOWN"), lambda p:p.update(number=9)]
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.data["pr"] = evidence()
                mutation(self.data["pr"])
                self.run_hook(code=2)

    def test_required_checks_pending_failed_cancelled_or_unknown_block(self):
        for bucket in ("pending", "fail", "cancel", "unknown"):
            self.data["checks"] = [{"name": "test", "bucket": bucket}]
            self.run_hook(code=2)
        self.data["checks"] = [{"name": "test", "bucket": "skipping"}]
        self.run_hook()

    def test_server_merge_blocker_prevents_missing_required_checks_from_passing(self):
        for state in ("BLOCKED", "BEHIND", "UNKNOWN", "UNSTABLE", None):
            for missing in (False, True):
                with self.subTest(state=state, missing=missing):
                    self.data = {"pr": evidence()}
                    self.data["pr"]["mergeStateStatus"] = state
                    if missing:
                        self.data.update(fail="checks", stderr="no required checks reported on the 'main' branch", exit_code=1)
                    self.run_hook(code=2)
        self.assertFalse(any(call[:2] == ["pr", "checks"] for call in self.calls()))

    def test_server_has_hooks_state_with_successful_checks_is_supported(self):
        self.data["pr"]["mergeStateStatus"] = "HAS_HOOKS"
        self.run_hook()

    def test_no_required_checks_is_explicitly_supported(self):
        self.data.update(fail="checks", stderr="no required checks reported on the 'main' branch", exit_code=1)
        self.run_hook()

    def test_api_failure_and_head_movement_block(self):
        for stage in ("repo", "graphql", "checks", "fresh"):
            self.data["fail"] = stage
            self.run_hook(code=2)
        self.data.pop("fail")
        self.data["fresh"] = OTHER
        self.run_hook(code=2)

    def test_repo_flag_url_environment_and_global_position_resolve_exactly(self):
        commands = [f"gh pr merge 7 -R example.com/other/repo --match-head-commit {HEAD}",
                    f"gh -R example.com/other/repo pr merge 7 --match-head-commit {HEAD}",
                    f"gh pr -R example.com/other/repo merge 7 --match-head-commit {HEAD}",
                    f"GH_REPO=example.com/other/repo gh pr merge 7 --match-head-commit {HEAD}",
                    f"gh pr merge https://example.com/other/repo/pull/7 --match-head-commit {HEAD}"]
        for command in commands:
            self.log.unlink(missing_ok=True)
            self.run_hook(command)
            calls = self.calls()
            self.assertIn("example.com", calls[0])
            self.assertIn("owner=other", calls[0])
            self.assertIn("name=repo", calls[0])
            self.assertIn("example.com/other/repo", calls[1])
        self.run_hook(f"gh pr merge https://example.com/other/repo/pull/7 -R github.com/local/repo --match-head-commit {HEAD}", code=2)

    def test_body_and_subject_repository_like_values_never_change_the_target(self):
        commands = [
            f"gh pr merge 7 --body '--repo=other/repo' --delete-branch --match-head-commit {HEAD}",
            f"gh pr merge 7 --subject '--repo=other/repo' --match-head-commit {HEAD}",
            f"gh pr merge 7 --body '-R' --subject '--repo' --match-head-commit {HEAD}",
            f"gh pr merge 7 --body=--repo=other/repo --subject=--repo=other/repo --match-head-commit {HEAD}",
            f"gh -R github.com/local/repo pr merge 7 --body '--repo=other/repo' --match-head-commit {HEAD}",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.log.unlink(missing_ok=True)
                self.run_hook(command)
                graphql = next(call for call in self.calls() if call[:2] == ["api", "graphql"])
                self.assertIn("owner=local", graphql)
                self.assertIn("name=repo", graphql)
                self.assertNotIn("owner=other", graphql)

    def test_method_like_body_and_subject_values_are_consumed_as_values(self):
        for command in (
            f"gh pr merge 7 --body '--squash' --rebase --match-head-commit {HEAD}",
            f"gh pr merge 7 --subject '--merge' --squash --match-head-commit {HEAD}",
            f"gh pr merge 7 --body=--rebase --merge --match-head-commit {HEAD}",
        ):
            with self.subTest(command=command):
                self.run_hook(command)

    def test_duplicate_methods_and_unknown_global_options_are_rejected(self):
        for command in (
            f"gh pr merge 7 --squash --squash --match-head-commit {HEAD}",
            f"gh pr merge 7 --squash --rebase --match-head-commit {HEAD}",
            f"gh --unknown value pr merge 7 --match-head-commit {HEAD}",
        ):
            with self.subTest(command=command):
                self.run_hook(command, code=2)
        self.assertEqual(self.calls(), [])

    def test_inherited_repo_and_omitted_number_resolve_without_local_repo_guess(self):
        self.env["GH_REPO"] = "other/repo"
        self.run_hook(f"gh pr merge --match-head-commit {HEAD}")
        self.assertEqual(self.calls()[0], ["pr", "view", "feature/checkout", "--repo", "github.com/other/repo", "--json", "number"])

    def test_current_branch_resolution_keeps_explicit_repository_and_branch(self):
        self.run_hook(f"gh pr merge -R example.com/other/repo --match-head-commit {HEAD}")
        self.assertEqual(self.calls()[0], ["pr", "view", "feature/checkout", "--repo", "example.com/other/repo", "--json", "number"])
        self.assertIn("owner=other", self.calls()[1])
        self.assertIn("example.com", self.calls()[1])

    def test_graphql_bot_identity_is_typed_and_cannot_be_impersonated(self):
        author = self.data["pr"]["reviews"]["nodes"][0]["author"]
        author.update(__typename="Bot", login="trusted")
        self.run_hook()
        for change in ({"__typename": "User", "login": "trusted"},
                       {"__typename": "User", "login": "trusted[bot]"},
                       {"__typename": "Unknown", "login": "trusted[bot]"},
                       {"login": "trusted[bot]"}):
            with self.subTest(change=change):
                self.data["pr"]["reviews"]["nodes"][0]["author"] = change
                self.run_hook(code=2)

    def test_human_trust_is_distinct_from_bot_trust_and_self_review(self):
        config = self.repo / ".claude/yb-hooks.json"
        config.write_text('{"trusted_reviewers":["trusted"]}')
        review = self.data["pr"]["reviews"]["nodes"][0]
        review["author"] = {"__typename": "User", "login": "trusted"}
        self.run_hook()
        review["author"] = {"__typename": "Bot", "login": "trusted"}
        self.run_hook(code=2)
        config.write_text('{"trusted_reviewers":["trusted[bot]"]}')
        self.data["pr"]["author"] = {"__typename": "Bot", "login": "trusted"}
        self.run_hook(code=2)

    def test_human_and_bot_with_same_slug_do_not_overwrite_each_other(self):
        bot = self.data["pr"]["reviews"]["nodes"][0]
        bot["author"] = {"__typename": "Bot", "login": "trusted"}
        negative = deepcopy(bot)
        negative.update(state="CHANGES_REQUESTED", submittedAt="2026-11-01T09:00:00Z",
                        author={"__typename": "User", "login": "trusted"})
        self.data["pr"]["reviews"]["nodes"].append(negative)
        self.run_hook(code=2)

    def test_review_timestamps_are_compared_as_instants(self):
        for newer in ("2026-11-01T10:00:00.500Z", "2026-11-01T05:30:00-05:00"):
            with self.subTest(newer=newer):
                self.data = {"pr": evidence()}
                later = deepcopy(self.data["pr"]["reviews"]["nodes"][0])
                later.update(state="CHANGES_REQUESTED", submittedAt=newer)
                self.data["pr"]["reviews"]["nodes"].append(later)
                self.run_hook(code=2)

    def test_incomplete_or_ambiguous_decisive_review_times_block(self):
        for timestamp in (None, "", "not-a-time", "2026-11-01T10:00:00"):
            with self.subTest(timestamp=timestamp):
                self.data = {"pr": evidence()}
                self.data["pr"]["reviews"]["nodes"][0]["submittedAt"] = timestamp
                self.run_hook(code=2)
        self.data = {"pr": evidence()}
        conflict = deepcopy(self.data["pr"]["reviews"]["nodes"][0])
        conflict["state"] = "CHANGES_REQUESTED"
        # Approval appears last; equal timestamps do not prove it superseded a veto.
        self.data["pr"]["reviews"]["nodes"].insert(0, conflict)
        self.run_hook(code=2)

    def test_nested_wrappers_combined_shell_flags_and_comment_substitutions_block(self):
        direct = "gh pr merge 7 --squash --admin"
        for command in (f'env bash -c "{direct}"', f'command bash -c "{direct}"',
                        f'env command bash -ec "{direct}"', f'sh -xc "{direct}"',
                        f'# don\'t bypass the gate\necho "$({direct})"',
                        f'eval "{direct}"', "$'gh' pr merge 7 --squash --admin"):
            with self.subTest(command=command):
                self.run_hook(command, code=2)
        self.assertEqual(self.calls(), [])

    def test_literal_tab_stripping_heredoc_is_data_and_following_merge_is_guarded(self):
        for prose in ("cat <<-'EOF'\n\tgh pr merge 7 --squash\n\tEOF",
                      "cat <<- 'EOF'\n\tgh pr merge 7 --squash\n\tEOF",
                      "cat <<'EOF' # don't parse this apostrophe\ngh pr merge\nEOF"):
            self.run_hook(prose)
        self.assertEqual(self.calls(), [])
        self.run_hook(prose + f"\ngh pr merge 7 --match-head-commit {HEAD}", code=2)

    def test_comment_boundaries_and_nonexecuting_wrapper_controls(self):
        self.run_hook("echo token#literal; gh pr merge 7 --admin", code=2)
        for command in ("env echo gh pr merge 7", "command -v gh pr merge", "# don't merge\necho safe",
                        'echo "$(# don\'t run gh pr merge\necho safe)"',
                        'bash -c "cat <<\'EOF\'\ngh pr merge 7\nEOF"'):
            self.run_hook(command)
        self.assertEqual(self.calls(), [])

    def test_wrapper_options_are_scoped_before_the_executable(self):
        for command in ("command gh pr merge 7 --admin --body -v",
                        "command -p gh pr merge 7 --admin --subject -V",
                        "command -- gh pr merge 7 --admin --body -v",
                        'env -S"gh pr merge 7 --admin"',
                        'env -S "command gh pr merge 7 --admin --body -v"',
                        "env -S 'gh' pr merge 7 --admin",
                        "env -S '-u UNUSED gh' pr merge 7 --admin",
                        "env -S '-- gh' pr merge 7 --admin",
                        "env --split-string='gh pr merge 7 --admin'",
                        "env --split-string='gh' pr merge 7 --admin"):
            with self.subTest(command=command):
                self.run_hook(command, code=2)
        for command in ("command -v gh pr merge", "command -pv gh pr merge --body -v",
                        'env -S "echo gh pr merge"', "env --split-string='echo gh pr merge'"):
            with self.subTest(command=command):
                self.run_hook(command)
        self.assertEqual(self.calls(), [])

    def test_escaped_whitespace_does_not_turn_a_word_internal_hash_into_a_comment(self):
        for command in ("echo foo\\ # literal; gh pr merge 7 --admin",
                        "echo foo\\\n#literal; gh pr merge 7 --admin"):
            with self.subTest(command=command):
                self.run_hook(command, code=2)
        for command in ("echo foo\\  # don't run gh pr merge", "echo foo # don't run gh pr merge"):
            self.run_hook(command)
        self.assertEqual(self.calls(), [])

    def test_adversarial_shell_execution_oracle_uses_only_the_local_gh_stub(self):
        direct = "gh pr merge 7 --squash --admin"
        vectors = ((f'# don\'t bypass\necho "$({direct})"', True),
                   (f'env bash -c "{direct}"', True), (f'command bash -c "{direct}"', True),
                   (f'bash -ec "{direct}"', True), (f'sh -xc "{direct}"', True),
                   (f'eval "{direct}"', True), ("$'gh' pr merge 7 --squash --admin", True),
                   ("command gh pr merge 7 --admin --body -v", True),
                   ('env -S"gh pr merge 7 --admin"', True),
                   ('env -S "command gh pr merge 7 --admin --body -v"', True),
                   ("env -S 'gh' pr merge 7 --admin", True),
                   ("env -S '-u UNUSED gh' pr merge 7 --admin", True),
                   ("echo foo\\ # literal; gh pr merge 7 --admin", True),
                   ("echo foo\\\n#literal; gh pr merge 7 --admin", True),
                   ("cat <<-'EOF'\n\tgh pr merge 7 --squash\n\tEOF", False))
        for command, executes in vectors:
            with self.subTest(command=command):
                self.log.unlink(missing_ok=True)
                self.run_hook(command, code=2 if executes else 0)
                self.assertEqual(self.calls(), [])
                # The stub never merges; it only records argv and exits. Running
                # real Bash establishes whether a vector is executable or prose.
                subprocess.run(["/bin/bash", "-c", command], cwd=self.repo,
                               env=self.env, capture_output=True, text=True, timeout=5)
                actual = any(call[:2] == ["pr", "merge"] for call in self.calls())
                self.assertEqual(actual, executes)

    def test_wrappers_compound_substitution_auto_and_admin_are_blocked(self):
        direct = f"gh pr merge 7 --match-head-commit {HEAD}"
        for command in (f"command {direct}", f"env GH_REPO=other/repo {direct}",
                        f"cd ../other && {direct}", f"echo $({direct})", f"bash -c '{direct}'",
                        f"echo `{direct}`", f'echo "$({direct})"',
                        direct + " --auto", direct + " --admin", direct + "\ngit status",
                        f"gh --unknown value pr merge 7 --match-head-commit {HEAD}"):
            with self.subTest(command=command):
                self.run_hook(command, code=2)
        self.assertEqual(self.calls(), [])

    def test_quoted_prose_and_echo_are_not_merge_commands(self):
        for command in ("echo 'gh pr merge 7'", "echo gh pr merge 7", "printf '%s' 'gh pr merge'",
                        "git commit -m 'Do not gh pr merge yet'", "cat <<'EOF'\ngh pr merge 7\nEOF",
                        'cat <<"EOF"\necho "$(gh pr merge 7)"\nEOF',
                        "echo '$(gh pr merge 7)'", "echo '`gh pr merge 7`'",
                        "gh issue create --title 'Merge instructions' --body 'Use gh pr merge later'"):
            with self.subTest(command=command):
                self.run_hook(command)
        self.assertEqual(self.calls(), [])

    def test_merge_after_quoted_heredoc_is_still_blocked(self):
        self.run_hook(f"cat <<'EOF'\nliteral prose\nEOF\ngh pr merge 7 --match-head-commit {HEAD}", code=2)
        self.assertEqual(self.calls(), [])

    def test_project_only_installation_never_falls_back_to_global_reviewers(self):
        installed = self.root / "home/.claude"
        (installed / "hooks").mkdir(parents=True)
        self.script = installed / "hooks/yb_merge_gate.py"
        shutil.copy2(MERGE, self.script)
        (installed / "yb-hooks.json").write_text(json.dumps({
            "project_reviewers_only": True, "trusted_reviewers": ["trusted[bot]"]}))
        project_config = self.repo / ".claude/yb-hooks.json"
        project_config.unlink()
        result = self.run_hook(code=2)
        self.assertIn("project reviewers only", result.stderr)
        self.assertEqual(self.calls(), [])
        project_config.write_text('{"trusted_reviewers":["stranger"],"project_reviewers_only":false}')
        self.run_hook(code=2)
        project_config.write_text('{"trusted_reviewers":["trusted[bot]"]}')
        self.run_hook()

    def test_missing_trust_configuration_blocks(self):
        (self.repo / ".claude/yb-hooks.json").write_text('{"trusted_reviewers":[]}')
        self.run_hook(code=2)
        self.assertEqual(self.calls(), [])

    def test_only_unambiguous_positive_ascii_pr_numbers_are_supported(self):
        for target in ("0", "007", "٧", "７"):
            with self.subTest(target=target):
                self.run_hook(f"gh pr merge {target} --match-head-commit {HEAD}", code=2)
        self.assertEqual(self.calls(), [])


@unittest.skipIf(os.name == "nt", "opt-in shell check requires a POSIX executable")
class StopHookTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="yb-stop-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.env = isolated_git_environment()
        self.counter = self.root / "count"
        self.session = self.root.name
        self.git("init", "-q")
        self.git("config", "user.name", "Hook tests")
        self.git("config", "user.email", "hooks@example.invalid")
        (self.repo / "file.txt").write_text("initial\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        (self.repo / ".claude").mkdir()
        self.check = self.repo / ".claude/yb-check.sh"
        self.write_check()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env, capture_output=True, text=True, check=True)

    def write_check(self, tail="exit 0"):
        import shlex
        self.check.write_text("#!/bin/sh\nprintf 'run\\n' >> " + shlex.quote(str(self.counter)) + "\n" + tail + "\n")
        self.check.chmod(0o755)

    def run_hook(self, code=0, **extra):
        payload = {"cwd": str(self.repo), "session_id": self.session, "stop_hook_active": False}
        payload.update(extra)
        result = subprocess.run([sys.executable, str(STOP)], input=json.dumps(payload),
                                text=True, capture_output=True, env=self.env, timeout=10)
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def count(self):
        return len(self.counter.read_text().splitlines()) if self.counter.exists() else 0

    def test_opt_in_only_and_recursion_guard(self):
        self.check.unlink()
        self.run_hook()
        self.write_check("exit 1")
        self.run_hook(stop_hook_active=True)
        self.assertEqual(self.count(), 0)

    def test_identical_dirty_content_is_checked_once(self):
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 1)
        (self.repo / "file.txt").write_text("changed\n")
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 2)

    def test_untracked_content_and_index_changes_invalidate_cache(self):
        self.run_hook()
        new = self.repo / "new.txt"
        new.write_text("one")
        self.run_hook()
        new.write_text("two")
        self.run_hook()
        self.git("add", "new.txt")
        self.run_hook()
        self.assertEqual(self.count(), 4)

    def test_failed_run_is_never_cached_and_clears_prior_success(self):
        self.write_check("exit 1")
        self.run_hook(code=2)
        self.run_hook(code=2)
        self.assertEqual(self.count(), 2)
        self.write_check()
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 3)

    def test_checks_that_change_files_do_not_cache_unverified_new_state(self):
        self.write_check("printf 'x' >> file.txt\nexit 0")
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 2)

    def add_submodule(self):
        origin = self.root / "submodule-source"
        origin.mkdir()
        subprocess.run(["git", "init", "-q", str(origin)], env=self.env, check=True)
        subprocess.run(["git", "-C", str(origin), "config", "user.name", "Hook tests"], env=self.env, check=True)
        subprocess.run(["git", "-C", str(origin), "config", "user.email", "hooks@example.invalid"], env=self.env, check=True)
        (origin / "source.txt").write_text("initial\n")
        subprocess.run(["git", "-C", str(origin), "add", "source.txt"], env=self.env, check=True)
        subprocess.run(["git", "-C", str(origin), "commit", "-qm", "fixture"], env=self.env, check=True)
        self.git("-c", "protocol.file.allow=always", "submodule", "add", "-q", str(origin), "dep")
        self.git("commit", "-qm", "add local submodule")
        return self.repo / "dep/source.txt"

    def test_dirty_submodule_edits_are_checked_each_time(self):
        source = self.add_submodule()
        source.write_text("dirty state one\n")
        self.run_hook()
        source.write_text("dirty state two\n")
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 3)

    def test_check_modifying_an_already_dirty_submodule_never_caches_success(self):
        source = self.add_submodule()
        source.write_text("dirty\n")
        self.write_check("printf 'x' >> dep/source.txt\nexit 0")
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 2)
        self.assertEqual(source.read_text(), "dirty\nxx")

    def test_check_making_a_clean_submodule_dirty_never_caches_new_state(self):
        source = self.add_submodule()
        self.write_check("printf 'x' >> dep/source.txt\nexit 0")
        self.run_hook()
        self.run_hook()
        self.assertEqual(self.count(), 2)
        self.assertEqual(source.read_text(), "initial\nxx")

    def test_timeout_is_bounded_and_failure_reported(self):
        self.write_check("sleep 20\nexit 0")
        (self.repo / ".claude/yb-hooks.json").write_text('{"check_timeout_seconds":1}')
        result = self.run_hook(code=2)
        self.assertIn("exceeded 1s", result.stderr)

    def test_unborn_repository_runs_opted_in_check(self):
        unborn = self.root / "unborn"
        unborn.mkdir()
        subprocess.run(["git", "init", "-q", str(unborn)], env=self.env, check=True)
        (unborn / ".claude").mkdir()
        check = unborn / ".claude/yb-check.sh"
        shutil.copy2(self.check, check)
        self.run_hook(cwd=str(unborn), session_id="unborn-" + self.session)
        self.assertEqual(self.count(), 1)

    def test_config_timeout_must_be_finite_and_bounded(self):
        for value in (0, 301, True, "10"):
            (self.repo / ".claude/yb-hooks.json").write_text(json.dumps({"check_timeout_seconds": value}))
            self.run_hook(code=2)
        self.assertEqual(self.count(), 0)


if __name__ == "__main__":
    unittest.main()
