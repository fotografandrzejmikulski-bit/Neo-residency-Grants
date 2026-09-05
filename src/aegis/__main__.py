import argparse
import json

from .core import StateStore, Workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Aegis minimal local state demo")
    parser.add_argument("workflow", nargs="?", default="demo")
    args = parser.parse_args()

    workflow = Workflow(args.workflow, StateStore())
    state = workflow.load_state().commit({"status": "running"}, actor="cli")
    checkpoint = workflow.checkpoint()
    print(json.dumps({"workflow": args.workflow, "revision": state.revision, "checkpoint": checkpoint.id}))


if __name__ == "__main__":
    main()
