"""Small dependency-free report formatter."""
import argparse


def render(rows):
    return "\n".join(f"{name}: {count}" for name, count in rows)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.parse_args(argv)
    print(render([("apples", 2), ("pears", 3)]))


if __name__ == "__main__":
    main()
