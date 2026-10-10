# Module Readiness Advisor: Evaluation Set

Twenty three capability requests with expected answers, written before any code exists.

Every example here is synthetic. No client, employer, repository or in flight work is referenced.

**The inventory used for all cases below** (what the organisation already has):
- Shared VPC with subnets in two regions
- Cloud DNS private zone
- A central KMS key ring
- A shared Artifact Registry

---

## Case 1

**Request:** A private storage bucket for application logs.

| Expected | |
|---|---|
| Sub modules | Storage bucket; bucket IAM binding |
| Already exists | KMS key ring |
| To build | Storage bucket, bucket IAM binding |
| Grouping | One story, the IAM binding is meaningless without the bucket |
| Dependencies | Security or IAM: a service account for the writing application |
| Readiness | Blocked |

---

## Case 2

**Request:** A Cloud Run service for an internal API.

| Expected | |
|---|---|
| Sub modules | Cloud Run service; service account; VPC connector; Artifact Registry repository |
| Already exists | Shared VPC; Artifact Registry |
| To build | Cloud Run service, service account, VPC connector |
| Grouping | VPC connector separate, the other two together |
| Dependencies | Networking: VPC connector needs a subnet range. Platform prerequisite: Cloud Run API enabled |
| Readiness | Blocked |

---

## Case 3

**Request:** A BigQuery setup for an analytics workload.

Chosen deliberately because in practice this kind of request decomposes much further than it looks. Expect ten or more items.

| Expected | |
|---|---|
| Sub modules | Dataset; tables; views; scheduled queries; IAM bindings at dataset and table level; encryption configuration; data transfer configuration; authorised views; partitioning and clustering configuration; audit log sink; cost controls or slot reservation |
| Already exists | KMS key ring |
| To build | Most of the above |
| Grouping | Dataset with tables and partitioning. IAM bindings separate. Scheduled queries and transfers separate. Audit sink separate |
| Dependencies | Security or IAM: dataset level access model. Existing application repository: where the source data already lives. Architecture or customer approval: whether cost controls are in scope |
| Readiness | Needs decision |
| Also | Demand not confirmed. See case 3a |

---

## Case 3a

**Request:** A Cloud SQL instance, where the consuming team has not confirmed they will use it.

This case exists because of a real failure mode. A module can be correctly decomposed, correctly sequenced, have no blockers, get built well, and still be waste if nobody consumes it.

| Expected | |
|---|---|
| Sub modules | Instance; database; users; backup configuration; private service access |
| Already exists | Shared VPC; KMS key ring |
| Dependencies | Demand not confirmed: no application team has committed to consuming this module |
| Readiness | Needs decision, and the decision is whether to build at all |

The correct behaviour is to surface demand as a readiness condition, not to plan the work. A module with no confirmed consumer should never be the thing you build first, however easy it is.

---

## Case 4

**Request:** A Pub/Sub topic and subscription for an event pipeline.

| Expected | |
|---|---|
| Sub modules | Topic; subscription; dead letter topic; IAM bindings |
| Already exists | Nothing relevant |
| To build | All four |
| Grouping | One story |
| Dependencies | Platform prerequisite: Pub/Sub API enabled |
| Readiness | Ready |

---

## Case 5

**Request:** An Azure storage account for document retention.

| Expected | |
|---|---|
| Sub modules | Storage account; container; private endpoint; diagnostic settings |
| Already exists | Nothing relevant in this inventory |
| To build | All four |
| Grouping | Account and container together. Private endpoint separate. Diagnostics separate |
| Dependencies | Networking: subnet for the private endpoint. Architecture or customer approval: the agreed IAM approach for the account |
| Readiness | Needs decision |

---

## Case 6

**Request:** A GKE cluster for a containerised application.

| Expected | |
|---|---|
| Sub modules | Cluster; node pools; workload identity; service account; network policy; cluster autoscaler config; logging and monitoring config; private endpoint config |
| Already exists | Shared VPC; Artifact Registry |
| To build | All except VPC and registry |
| Grouping | Cluster with node pools and autoscaler. Workload identity with service account. Network policy separate. Observability separate |
| Dependencies | Networking: pod and service IP ranges on the subnet. Security or IAM: workload identity binding. Platform prerequisite: GKE API |
| Readiness | Blocked |

---

## Case 7

**Request:** A private DNS record for an internal service.

| Expected | |
|---|---|
| Sub modules | DNS record set |
| Already exists | Cloud DNS private zone |
| To build | The record set only |
| Grouping | One story, trivially small |
| Dependencies | Module or resource: the service it points at must exist first |
| Readiness | Blocked |

Included as the easy case. The right answer is a small amount of work, and the tool should not inflate it.

---

## Case 8

**Request:** Monitoring and alerting for an existing application.

| Expected | |
|---|---|
| Sub modules | Notification channels; alert policies; dashboards; uptime checks; log based metrics |
| Already exists | Nothing relevant |
| To build | All five |
| Grouping | Notification channels first, alert policies depend on them. Dashboards separate. Uptime checks separate |
| Dependencies | Architecture or customer approval: who receives alerts and at what severity |
| Readiness | Needs decision |

The only blocker is a conversation, which is the clearest example of a type 6 dependency.

---

## Case 9

**Request:** A VPC and subnets for a new environment.

| Expected | |
|---|---|
| Sub modules | VPC; subnets; firewall rules; Cloud NAT; Cloud Router; private service access; flow logs |
| Already exists | Nothing, this is a new environment |
| To build | All seven |
| Grouping | VPC with subnets. Router with NAT. Firewall rules separate. Private service access separate |
| Dependencies | Architecture or customer approval: the IP address range allocation |
| Readiness | Needs decision |

---

## Case 10

**Request:** An Azure Kubernetes Service cluster.

| Expected | |
|---|---|
| Sub modules | AKS cluster; node pools; managed identity; role assignments; container registry access; log analytics workspace; network configuration |
| Already exists | Nothing in this inventory |
| To build | All seven |
| Grouping | Cluster with node pools. Identity with role assignments. Observability separate |
| Dependencies | Networking: subnet with sufficient address space. Security or IAM: managed identity and role assignments |
| Readiness | Blocked |

---

## Case 11

**Request:** Reuse the existing shared VPC for a new application, no new networking.

| Expected | |
|---|---|
| Sub modules | Subnet IAM binding only |
| Already exists | Shared VPC; subnets; Cloud DNS private zone |
| To build | The IAM binding only |
| Grouping | One story |
| Dependencies | Security or IAM: the service account to bind |
| Readiness | Blocked |

Included because the correct answer is almost entirely reuse. A tool that recommends rebuilding networking here has failed badly.

---

## Case 12

**Request:** A data pipeline from storage into the warehouse.

| Expected | |
|---|---|
| Sub modules | Source bucket; notification; Pub/Sub topic; subscription; processing job; destination dataset; destination tables; service accounts; IAM bindings; dead letter handling; scheduling; monitoring |
| Already exists | KMS key ring |
| To build | Most of the above |
| Grouping | Source side together. Processing separate. Destination side together. Monitoring separate |
| Dependencies | Existing application repository: the source data location. Security or IAM: cross service permissions. Architecture or customer approval: processing approach |
| Readiness | Needs decision |

Second large decomposition case. Expect twelve or more items.

---

## Case 13

**Request:** Secrets management for an application.

| Expected | |
|---|---|
| Sub modules | Secret; secret version; IAM bindings; rotation configuration |
| Already exists | KMS key ring |
| To build | All four |
| Grouping | Secret with version. IAM separate. Rotation separate |
| Dependencies | Security or IAM: who can access, and the rotation policy. Platform prerequisite: Secret Manager API |
| Readiness | Blocked |

---

## Case 14

**Request:** A load balancer for a public web application.

| Expected | |
|---|---|
| Sub modules | Global load balancer; backend service; health check; SSL certificate; URL map; forwarding rule; Cloud Armor policy |
| Already exists | Cloud DNS private zone, which is not the public zone needed here |
| To build | All seven |
| Grouping | Load balancer with URL map and forwarding rule. Backend with health check. Certificate separate. Cloud Armor separate |
| Dependencies | Networking: public DNS zone, which the inventory does not contain. Security or IAM: Cloud Armor rules. Architecture or customer approval: the WAF ruleset |
| Readiness | Needs decision |

Tests whether the tool notices that an existing private DNS zone does not satisfy a public DNS requirement. A near match is not a match.

---

## Case 15

**Request:** Something for our new application.

| Expected | |
|---|---|
| Sub modules | None, the request cannot be decomposed |
| Readiness | Cannot assess |
| Correct behaviour | Ask what the application needs, rather than guessing. Suggest a shortlist of common starting points and ask the user to choose |

Included deliberately. Guessing at a vague request is worse than asking.

---

## Case 16

**Request:** An Azure Function for scheduled processing.

| Expected | |
|---|---|
| Sub modules | Function app; app service plan; storage account; application insights; managed identity; role assignments |
| Already exists | Nothing in this inventory |
| To build | All six |
| Grouping | Function app with plan and storage. Identity with role assignments. Insights separate |
| Dependencies | Security or IAM: managed identity. Platform prerequisite: resource providers registered |
| Readiness | Blocked |

Note that the storage account looks like an independent item but is a hard requirement of the function app, so it belongs in the same story. Tests whether grouping is based on actual coupling rather than on resource type.

---

## Case 17

**Request:** A service account for an application to call internal APIs.

| Expected | |
|---|---|
| Sub modules | Service account; IAM role bindings; workload identity binding; key rotation if keys are used |
| Already exists | Nothing relevant |
| To build | Service account and bindings. Keys should not be created if workload identity is available |
| Grouping | One story |
| Dependencies | Architecture or customer approval: which roles are granted. Module or resource: the APIs it will call |
| Readiness | Needs decision |

---

## Case 18

**Request:** A Cloud Composer environment for orchestration.

| Expected | |
|---|---|
| Sub modules | Composer environment; service account; IAM bindings; bucket for DAGs; networking configuration; private IP configuration |
| Already exists | Shared VPC; KMS key ring |
| To build | Environment, service account, bindings, bucket |
| Grouping | Environment with networking. Service account with bindings. Bucket separate |
| Dependencies | Networking: subnet ranges for the environment. Security or IAM: service account permissions. Platform prerequisite: Composer API |
| Readiness | Blocked |

---

## Case 19

**Request:** An audit log sink to central storage, where no consuming team has asked for it.

| Expected | |
|---|---|
| Sub modules | Log sink; destination bucket; sink service account; IAM binding; retention policy |
| Already exists | KMS key ring |
| Dependencies | Demand not confirmed: no team has requested or committed to consuming these logs |
| Readiness | Needs decision, and the decision is whether to build at all |

Second unconfirmed demand case, to check the behaviour is consistent and not a one off.

---

## Case 20

**Request:** A Redis cache for session storage.

| Expected | |
|---|---|
| Sub modules | Memorystore instance; private service access; firewall rule; monitoring |
| Already exists | Shared VPC; private service access, already created in case 3a |
| To build | Instance, firewall rule, monitoring |
| Grouping | Instance with firewall rule. Monitoring separate |
| Dependencies | Platform prerequisite: Memorystore API |
| Readiness | Ready |

Included as a late case that is genuinely ready, so the set does not end up biased toward everything being blocked.

---

## Case 21

**Request:** A Vertex AI environment for a team building machine learning models.

| Expected | |
|---|---|
| Sub modules | Workbench instance; model endpoint; service account; IAM bindings; private connectivity; encryption configuration; storage bucket for training data |
| Already exists | Shared VPC; KMS key ring |
| To build | Workbench, endpoint, service account, bindings, private connectivity, bucket |
| Grouping | Workbench with service account and bindings. Endpoint separate. Private connectivity separate. Bucket separate |
| Dependencies | Platform prerequisite: Vertex AI API enabled. Networking: private connectivity to the shared VPC. Security or IAM: who can deploy models. Architecture or customer approval: whether public endpoints are ever allowed |
| Readiness | Needs decision |

Included because AI platform requests are becoming common and carry an extra governance question, who is allowed to deploy a model, that ordinary infrastructure does not.

---

## Case 22

**Request:** Document AI for processing scanned forms.

| Expected | |
|---|---|
| Sub modules | Document AI processor; input storage bucket; output storage bucket; service account; IAM bindings; encryption configuration |
| Already exists | KMS key ring |
| To build | Processor, both buckets, service account, bindings |
| Grouping | Processor with service account and bindings. Input and output buckets together |
| Dependencies | Platform prerequisite: Document AI API enabled. Architecture or customer approval: which processing region is allowed, since scanned forms may contain personal data |
| Readiness | Needs decision |

The region question is the real blocker here. A tool that marks this Ready because nothing technical is missing has missed the point.

---

## Case 23

**Request:** Access to a generative AI model API for an application team building a customer support assistant.

| Expected | |
|---|---|
| Sub modules | API enablement; service account; IAM bindings; quota configuration; private connectivity; request and response logging; data protection controls |
| Already exists | Shared VPC |
| To build | Service account, bindings, quota, private connectivity, logging, data protection controls |
| Grouping | Service account with bindings. Quota separate. Logging with data protection controls |
| Dependencies | Platform prerequisite: the model API enabled. Security or IAM: which identities can call the model. Architecture or customer approval: what data the model is allowed to see, and whether prompts and responses may be logged |
| Readiness | Needs decision |

The data question is what makes this different from ordinary infrastructure. Nothing technical is missing, yet it cannot start until someone decides what customer data may reach the model.

---

## Scoring

Each case is scored on four points, pass or fail:

1. Correct sub modules identified
2. Reuse correctly detected against the inventory
3. Dependencies correctly identified and classified by type
4. Grouping a platform engineer would agree with

Target: at least 19 of 23 on points 1 and 3. Point 2 must be 23 of 23, because a false "already exists" causes real work to be skipped.

Results published with failures included.
