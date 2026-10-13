"""Module Readiness Advisor, AI step.

You type a request in plain English. An AI model works out which
capability in the catalogue it matches, or asks a question back if the
request is too vague. The fixed rules in advisor.py then decide
readiness, so the AI never decides readiness itself.

Usage:
    py ask.py "We need somewhere private to keep our application logs"
    py ask.py --test

Needs a free Gemini API key in the GEMINI_API_KEY environment variable.
Never put the key in a file.
"""

import json
import os
import sys

from google import genai
from google.genai import types

from advisor import assess, load

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def match_request(client, request, capabilities):
    """Ask the model which capability fits. Returns (capability_id, question)."""
    options = "\n".join(f"- {c['id']}: {c['name']}" for c in capabilities)
    prompt = f"""You help a cloud platform team understand infrastructure requests.

Here are the capabilities the team offers:
{options}

Request from an application team:
"{request}"

If the request clearly matches one capability, return its id.
If the request is too vague to match with confidence, return null for
capability and write one short question that would make it clear.
Never invent an id that is not in the list.

Reply only with JSON in this shape:
{{"capability": "<id or null>", "question": "<question or empty>"}}"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0,
        ),
    )
    answer = json.loads(response.text)
    chosen = answer.get("capability")
    question = answer.get("question") or "Could you describe what the application needs?"

    # Never trust the model blindly. An id that is not in the catalogue
    # is treated as unclear rather than shown to the user.
    valid_ids = {c["id"] for c in capabilities}
    if chosen not in valid_ids:
        return None, question
    return chosen, ""


def show_breakdown(capability, existing):
    reuse, build, dependencies, readiness = assess(capability, existing)
    print(f"Matched capability: {capability['name']}")
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


def run_tests(client, capabilities):
    tests = load("ai_tests.yaml")["tests"]
    passed = 0
    for test in tests:
        chosen, question = match_request(client, test["request"], capabilities)
        expected = test["expected"]
        ok = chosen == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        got = chosen or f"asked back: {question}"
        print(f"{status}  {test['request']}")
        print(f"      expected {expected}, got {got}")
    print("=" * 60)
    print(f"AI matching score: {passed} of {len(tests)}")


def main():
    if len(sys.argv) < 2:
        print('Type your request in quotes, for example: py ask.py "a cache for sessions"')
        return

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("No API key found. In the terminal run:  $env:GEMINI_API_KEY=\"your key\"")
        return

    client = genai.Client(api_key=key)
    capabilities = load("catalog.yaml")["capabilities"]

    if sys.argv[1] == "--test":
        run_tests(client, capabilities)
        return

    request = " ".join(sys.argv[1:])
    chosen, question = match_request(client, request, capabilities)
    if chosen is None:
        print("The request is not clear enough to assess.")
        print(f"Question back to the team: {question}")
        return

    existing = {item["id"] for item in load("inventory.yaml")["existing_resources"]}
    capability = next(c for c in capabilities if c["id"] == chosen)
    show_breakdown(capability, existing)


if __name__ == "__main__":
    main()
