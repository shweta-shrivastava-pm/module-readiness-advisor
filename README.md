# Module Readiness Advisor

**Live demo:** https://module-readiness-advisor.streamlit.app

A tool for platform product owners. You describe the infrastructure an application team needs in plain English, and it tells you whether that work is ready for the next sprint, what already exists, what must be built, and what will block it.

## The problem

On a cloud platform programme, one request such as "a data pipeline into the warehouse" is never one piece of work. It breaks into many sub modules. Some already exist and should be reused, some belong together in one story, and some are blocked behind networking, security or a decision nobody has made yet.

That knowledge usually sits with engineers and reaches sprint planning late, often as a blocker in the middle of the sprint. The manual fix is to ask the client about next sprint's modules weeks ahead. This tool does the analysis that goes into those questions.

## How it works

1. **AI understands the request.** Gemini matches the plain English request to a capability in the catalogue. If the request is too vague, it asks a question back instead of guessing. Any answer that is not a real catalogue entry is rejected.
2. **Fixed rules decide readiness.** The AI never decides readiness. Rules check each sub module against the inventory of what already exists, classify every dependency by type, and give one of three answers:

| Readiness | When |
|---|---|
| Needs decision | An approval is pending, or no team has confirmed it will use the module |
| Blocked | A missing module, networking, IAM or existing repository dependency |
| Ready | Nothing outstanding. Cloud APIs to switch on are listed but do not block |

3. **Sprint fit.** More than 8 new pieces is flagged as Needs splitting, with the stories to split it into.

## Results

| Test | Score |
|---|---|
| Readiness rules against the evaluation set | 23 of 23 cases |
| AI request matching, including 2 vague requests | 10 of 10 |

The readiness rules run automatically on every commit with GitHub Actions. The evaluation set was written before the code, and lives in [docs/evaluation-set.md](docs/evaluation-set.md).

## Design decisions

- **AI only where the input is unclear.** Matching free text needs AI. Readiness must be predictable and explainable, so it stays as rules.
- **Never trust the model blindly.** Every AI answer is checked against the catalogue before it is used.
- **Designed for an unreliable service.** When the AI service is busy, the tool waits and retries instead of failing.
- **No false reuse.** Something is marked as already existing only on an exact match with the inventory. A private DNS zone does not satisfy a need for a public one.

## Run it yourself

```
pip install -r requirements.txt
python advisor.py                 # readiness for every capability, with the score
python ask.py "your request"      # needs GEMINI_API_KEY set
python ask.py --test              # AI matching test
streamlit run app.py              # the web demo
```

## Project files

| File | What it is |
|---|---|
| [docs/module-readiness-advisor-prd.md](docs/module-readiness-advisor-prd.md) | Product requirements |
| [docs/evaluation-set.md](docs/evaluation-set.md) | Test cases with expected answers |
| data/catalog.yaml | Capabilities, sub modules and dependencies |
| data/inventory.yaml | What already exists |
| data/ai_tests.yaml | Plain English test requests |
| advisor.py | Readiness rules and self scoring |
| ask.py | AI request matching |
| app.py | Web demo |

## Note

Built on personal equipment, using public cloud documentation and synthetic data only. No employer or client material of any kind.

## Author

Shweta Shrivastava
