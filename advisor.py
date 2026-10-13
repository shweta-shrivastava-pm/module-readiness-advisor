"""Module Readiness Advisor, version 0.2.

Reads the inventory and the module catalogue, prints a readiness
breakdown for every capability, then scores itself against the
expected answers from the evaluation set.
"""

from pathlib import Path

import yaml

DATA = Path(__file__).parent / "data"

# Dependencies that need a conversation before work can start.
DECISION_TYPES = {"approval", "demand"}

# Dependencies that stop work starting. Platform APIs are usually
# quick to switch on, so they are reported but do not block.
BLOCKING_TYPES = {"module_or_resource", "existing_repository", "networking", "security_iam"}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def assess(capability, existing):
    own_parts = {part["id"] for part in capability["sub_modules"]}
    reuse = set()
    build = []
    dependencies = list(capability.get("dependencies", []))

    for part in capability["sub_modules"]:
        if part["id"] in existing:
            reuse.add(part["id"])
        else:
            build.append(part)
        for used in part.get("uses", []):
            if used in existing:
                reuse.add(used)
            elif used not in own_parts:
                dependencies.append(
                    {"type": "module_or_resource", "need": f"{used} must exist first"}
                )

    types = {d["type"] for d in dependencies}
    if types & DECISION_TYPES:
        readiness = "Needs decision"
    elif types & BLOCKING_TYPES:
        readiness = "Blocked"
    else:
        readiness = "Ready"

    return reuse, build, dependencies, readiness


def main():
    existing = {item["id"] for item in load("inventory.yaml")["existing_resources"]}
    passed = 0
    failed = []
    capabilities = load("catalog.yaml")["capabilities"]

    for capability in capabilities:
        reuse, build, dependencies, readiness = assess(capability, existing)

        print("=" * 60)
        print(f"Case {capability['case']}: {capability['name']}")
        print(f"  Readiness: {readiness}")
        print(f"  Already exists, reuse: {', '.join(sorted(reuse)) or 'nothing'}")
        print("  To build:")
        for part in build:
            print(f"    - {part['id']} (story: {part['story']})")
        print("  Dependencies:")
        for d in dependencies:
            print(f"    - {d['type']}: {d['need']}")
        if not dependencies:
            print("    - none")

        expected = capability.get("expected_readiness")
        if expected == readiness:
            passed += 1
        else:
            failed.append(f"Case {capability['case']}: expected {expected}, got {readiness}")

    print("=" * 60)
    print(f"Score: {passed} of {len(capabilities)} cases match the evaluation set")
    for line in failed:
        print(f"  MISMATCH  {line}")


if __name__ == "__main__":
    main()
