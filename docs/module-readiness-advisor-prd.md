# Module Readiness Advisor

Product Requirements Document, version 2

Author: Shweta Shrivastava

---

## 1. Problem

When a platform team is asked to deliver a module, the request is rarely one piece of work. It decomposes into many sub modules. Some belong together in one story, some need their own, some already exist and should not be rebuilt, and some are blocked behind a networking or security prerequisite that cannot move until the client agrees to it.

The harder problem is where that information lives. It sits with the engineers, in technical calls and client discussions that the product owner is not part of. It usually reaches planning only once it has already become a blocker, surfacing at a standup or as an item moved to on hold. That is the most expensive moment to find out, because the sprint has already started.

The working answer is to ask the client about the next sprint's modules before planning, so blockers surface weeks ahead and there is time to resolve them. That works. What makes it slow is the part before the question: deciding which modules to ask about, what to ask, and which ones genuinely need an answer rather than a check.

This product does that part.

## 2. Users

**Primary: the platform product owner** planning the next two months of delivery, who needs to know which modules to raise with the client now, and what to ask about each one.

**Secondary: platform engineers** doing the decomposition analysis by hand today.

## 3. What it does

The user names a capability they need to deliver, for example "Cloud SQL for a customer facing application."

The advisor returns a readiness breakdown:

1. **Decomposition.** The sub modules this request actually contains
2. **Already exists.** Which of those are present in the organisation's inventory and should be reused rather than rebuilt
3. **To build.** Which are genuinely new work
4. **Grouping.** Which sub modules are correlated and belong in one user story, and which should be separate
5. **Blocked or needs decision.** Which have a dependency, what type it is, and who has to act
6. **Suggested sequencing.** What can go into the next sprint and what needs lead time first
7. **Sprint fit.** Whether the item plausibly fits in one sprint, or should be split because it is large, critical, or has a review gate in the middle of it

## 4. Scope

**In scope for version 1**
- Google Cloud and Azure
- Public module registries only: terraform-google-modules and Azure Verified Modules
- An inventory file the user supplies, listing what already exists
- Decomposition based on the module's declared sub modules and required inputs
- Dependency detection and classification into the six types in section 7
- A web interface showing the readiness breakdown
- Export of the breakdown as draft user stories

**Out of scope for version 1**
- AWS
- Generating or applying Terraform
- Effort estimation in days, the tool reports readiness, a human estimates effort
- Connecting to a live repository, the inventory is a file the user provides
- Any employer or client code, configuration, module, policy or inventory

## 5. Success measures

- A capability that takes an engineer an hour to analyse is broken down in under a minute
- Across a 20 request evaluation set, the tool identifies the correct sub modules for at least 16
- Every item marked "already exists" is actually in the supplied inventory, no false reuse
- A platform engineer reviewing the output agrees with the grouping in most cases

The third measure matters most. Telling someone to skip work that does not exist is the worst failure this product can have.

## 6. Requirements

| # | Requirement | Priority |
|---|---|---|
| 1 | Accept a named capability as input | Must |
| 2 | Decompose it into sub modules from the public registry | Must |
| 3 | Compare against a user supplied inventory and mark reuse | Must |
| 4 | Identify each dependency and classify it by type | Must |
| 5 | Group correlated sub modules and separate independent ones | Must |
| 6 | Mark each item as already exists, ready, blocked or needs decision | Must |
| 7 | Export the breakdown as draft user stories | Should |
| 8 | Explain in plain English why an item is blocked | Should |
| 9 | Flag items that will not fit one sprint and suggest a split point | Should |
| 10 | Show the dependency relationships visually | Could |

## 7. Dependency types

Version 1 classifies every dependency it finds into one of these. The type matters more than the fact of the dependency, because the type decides who has to act and how long it takes.

| Type | What it means | Who unblocks it |
|---|---|---|
| Module or resource | Another module must exist first, for example a networking component a compute module needs | The platform team, by sequencing |
| Existing application repository | The resource already exists in the application repository and the new module must reference or integrate with it rather than recreate it | The application team, by confirming what exists |
| Networking | Requires networking to be configured first: VPC, subnet, firewall rules, NAT, DNS and similar | The networking team |
| Security or IAM | Requires a service account, role, permission, key or security policy before the module can even be validated | The security team |
| Platform prerequisite | A required cloud API or service must be enabled, or another platform capability must exist | The platform team, usually quick |
| Architecture or customer approval | The work can be built, but is waiting on architecture, security or the customer to confirm the approach | A conversation, not a task |

The last type is the one that justifies the product. The first five are technical dependencies that a team can plan around. The sixth is a decision, and a decision that surfaces during sprint planning costs a conversation while the same decision surfacing mid sprint costs the sprint.

## 7a. Readiness states

| State | Meaning |
|---|---|
| Already exists | Present in the supplied inventory, do not rebuild |
| Ready | New work, no unmet dependency, can enter the next sprint |
| Blocked | Has a dependency of types 1 to 5 that is neither in the inventory nor in this request |
| Needs decision | Has a type 6 dependency. Start the conversation now, well ahead of the sprint it affects |
| Needs splitting | Not blocked, but large or critical enough that a review falls mid build, so it will carry over if planned as one item |

Carryover is usually not a blocker. It is a sizing failure. The critical modules attract the most review, which is exactly why they are the ones that spill into the next sprint. Flagging them before planning is cheaper than discovering it at the sprint review.

## 8. How it is judged

A 20 request evaluation set written before the build starts, each scored on:

- correct sub modules identified
- reuse correctly detected against the inventory
- dependencies correctly identified and correctly classified by type
- grouping a platform engineer agrees with

Results published as a table in the repository, failures included.

## 9. Deliverables

1. Public GitHub repository with the code and this PRD
2. Working demo deployed on Hugging Face Spaces
3. The 20 request evaluation table with results
4. A three minute walkthrough video
5. A short written note on what did not work and why

## 10. Risks

| Risk | Mitigation |
|---|---|
| Tool says a module exists when it does not, causing skipped work | Exact matching against the inventory only, never inferred. This is the one failure mode treated as unacceptable |
| Decomposition misses a sub module | Validate against the live registry, publish the misses in the evaluation table |
| Dependency detection is naive | Version 1 detects declared dependencies only, and says so plainly rather than guessing |
| Scope grows and nothing ships | Two clouds, one input format, no Terraform generation. Ship version 1 first |
| Confidentiality | Built on personal equipment, public registries only, a synthetic inventory file. No employer or client material of any kind |

## 11. Timeline

Roughly 20 hours.

| Stage | Work | Hours |
|---|---|---|
| 1 | PRD and the 20 request evaluation set | 2 |
| 2 | Registry lookup and decomposition | 5 |
| 3 | Inventory comparison and reuse detection | 3 |
| 4 | Prerequisite and readiness logic | 4 |
| 5 | Web interface and story export | 4 |
| 6 | Evaluation run, video, README | 2 |
