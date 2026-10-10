# Module Readiness Advisor

Plans cloud module delivery by finding dependencies and readiness before sprint planning.

## The problem

When a platform team is asked to deliver a cloud module, the request is rarely one piece of work. It splits into many smaller modules. Some already exist and should be reused. Some are blocked by networking or security prerequisites. Some need a decision from the client before anyone can start.

This information usually reaches planning late, as a blocker in the middle of a sprint. This tool surfaces it before planning, so the right conversations start early.

## What it does

Given a request such as "a BigQuery setup for an analytics workload", the advisor:

1. Breaks it into sub modules
2. Checks which already exist and should be reused
3. Finds dependencies and classifies them by type
4. Marks each item as Ready, Blocked, Needs decision or Needs splitting

## Status

Early stage. The product requirements and a 23 case evaluation set are written. The code is being built next.

See `docs/module-readiness-advisor-prd.md` for the full requirements and `docs/evaluation-set.md` for the test cases.

## Note

Built independently on personal equipment, using only public cloud services and synthetic examples. Not affiliated with any employer or client.

Author: Shweta Shrivastava