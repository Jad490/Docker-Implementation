# AWS Console Deployment Record

This is both the runbook and the evidence checklist for the sentiment analysis
application. Replace every `<...>` placeholder while performing the deployment.
Do not record passwords, secret values, account IDs, or access keys in screenshots.

## Deployment facts

| Item | Value |
|---|---|
| AWS account alias (not account ID) | `<record>` |
| Region | US East (N. Virginia), `us-east-1` |
| Deployment date | July 24, 2026 |
| IAM administrator | `jad-admin` |
| VPC | `sentiment-vpc` (`10.0.0.0/16`) |
| ECS cluster | `sentiment-cluster` |
| ECS service | `sentiment-service` |
| RDS instance | `sentiment-postgres` |
| Private S3 bucket | `sentiment-app-assets-jad-a7k2m9` |
| Application URL | `<record after deployment>` |

## Progress checkpoint — July 24, 2026

Completed and observed:

- Created `jad-admin`, granted console administrator access, enabled MFA, signed
  out of root, and continued as the IAM user.
- Selected `us-east-1` for the application resources.
- Created the VPC, five subnets, Internet Gateway, three route tables, route
  associations, and the public route to the Internet Gateway.
- Created security groups for the ALB, ECS task, RDS, and VPC interface
  endpoints, using security-group references instead of public database or
  application rules.
- Created the private RDS subnet group and a Single-AZ PostgreSQL
  `db.t4g.micro` instance. PostgreSQL log export produced the CloudWatch log
  group `/aws/rds/instance/sentiment-postgres/postgresql`.
- Created the S3 gateway endpoint and configured it for the private application
  route table.
- Created the ECS application task role and ECS task execution role. The task
  role is intended to read one exact S3 verification object. The execution role
  uses `AmazonECSTaskExecutionRolePolicy` and is intended to read the one RDS
  Secrets Manager secret.
- Created `/ecs/sentiment/backend` and `/ecs/sentiment/frontend` CloudWatch log
  groups with seven-day retention.
- Created the private S3 bucket and uploaded `deployment-source.zip`, which
  contains `buildspec.yml` plus the backend and frontend build contexts.

Verify before launching ECS:

- The task-role inline policy resource must be exactly
  `arn:aws:s3:::sentiment-app-assets-jad-a7k2m9/README.md`, and `README.md`
  must exist at the bucket root.
- The execution-role inline policy must reference the exact RDS-managed secret
  ARN, not `*`.
- Confirm that all four interface endpoints (`ecr.api`, `ecr.dkr`, `logs`, and
  `secretsmanager`) and the S3 gateway endpoint show `Available`.
- Confirm both ECR repositories, `sentiment-backend` and
  `sentiment-frontend`, exist and use immutable tags.
- Confirm RDS belongs to `sentiment-vpc`, uses
  `sentiment-db-subnet-group`, has no public access, and uses only
  `sentiment-rds-sg`.
- Change the RDS PostgreSQL CloudWatch log retention from `Never expire` to
  seven days if that edit has not yet been saved.

Not started yet:

- CodeBuild image build and ECR image push.
- ALB target group and Application Load Balancer.
- ECS cluster, task definition, service, and public application test.
- CloudWatch alarm and final logs/metrics exploration.
- CloudTrail evidence/trail, cost budget, Route 53/ACM research evidence, and
  final reproducibility screenshots.

## Design

The internet-facing Application Load Balancer spans two public subnets because
AWS requires an ALB to use at least two Availability Zones. It sends HTTP traffic
to the NGINX container on port 80. NGINX and FastAPI run as two containers in the
same Fargate task, so NGINX reaches FastAPI on `127.0.0.1:8000`. For this
cost-conscious lab, the service runs one task in one private application subnet.
FastAPI connects to private RDS PostgreSQL on port 5432. Although the database is
Single-AZ, AWS requires its DB subnet group to contain subnets in at least two
Availability Zones. RDS is not publicly accessible.

The backend model is downloaded during the CodeBuild image build and stored in
the ECR image. It is not downloaded from Hugging Face when Fargate starts. This
lets the runtime stay private without a NAT gateway.

Private AWS access uses these VPC endpoints:

- ECR API interface endpoint
- ECR Docker interface endpoint
- CloudWatch Logs interface endpoint
- Secrets Manager interface endpoint
- S3 gateway endpoint (also required for ECR image layers)

Interface endpoints are resources in VPC subnets; the S3 gateway endpoint is
associated with route tables. For this lab, the interface endpoints are placed
only in the application subnet's Availability Zone, matching the single running
task and avoiding duplicate endpoint hourly charges. This is not a highly
available production design. The endpoints should not be represented as
resources physically outside the VPC.

### Availability Zone layout

| Subnet | CIDR | AZ | Route |
|---|---:|---|---|
| `sentiment-public-a` | `10.0.0.0/24` | `<region>a` | `0.0.0.0/0 -> IGW` |
| `sentiment-public-b` | `10.0.1.0/24` | `<region>b` | `0.0.0.0/0 -> IGW` |
| `sentiment-app-a` | `10.0.10.0/24` | `<region>a` | local + endpoints |
| `sentiment-db-a` | `10.0.20.0/24` | `<region>a` | local only |
| `sentiment-db-b` | `10.0.21.0/24` | `<region>b` | local only |

The five-subnet layout keeps the logical separation shown in the architecture.
Subnets and route tables themselves have no hourly charge. The second public
subnet and second DB subnet do not imply a second Fargate task or a Multi-AZ RDS
instance.

### Security-group flows

| Security group | Inbound | Source |
|---|---|---|
| `sentiment-alb-sg` | TCP 80 | `0.0.0.0/0` |
| `sentiment-ecs-sg` | TCP 80 | `sentiment-alb-sg` |
| `sentiment-rds-sg` | TCP 5432 | `sentiment-ecs-sg` |
| `sentiment-endpoints-sg` | TCP 443 | `sentiment-ecs-sg` |

Do not open FastAPI port 8000 or PostgreSQL port 5432 to the internet.

## Phase 0 — safety and identity

### 0.1 Root account

1. Sign in as root only for initial identity setup.
2. Open the account security credentials page.
3. Confirm root MFA is enabled.
4. Confirm root has no access keys.
5. Sign out immediately after creating the administrator.

Outcome: root credentials are protected and will not be used for deployment.

Evidence:

- `[ ] 01-root-mfa.png` — MFA status only; redact identifiers.
- `[ ] 02-root-no-access-keys.png` — access-key status only.

### 0.2 IAM administrator

1. Open **IAM → Users → Create user**.
2. User name: `jad-admin`.
3. Enable Management Console access.
4. Do not create an access key.
5. Attach `AdministratorAccess` directly for this supervised lab.
6. Sign in using the account-specific IAM sign-in URL.
7. Open **Security credentials → Assign MFA device** and register MFA.
8. Continue all remaining work as `jad-admin`.

Why: this satisfies the lab requirement to stop using root. For a production
organization, IAM Identity Center and temporary credentials are preferred.

Evidence:

- `[ ] 03-jad-admin-permissions.png`
- `[ ] 04-jad-admin-mfa.png`
- `[ ] 05-jad-admin-login.png`

### 0.3 Billing protection

1. Open **Billing and Cost Management → Budgets → Create budget**.
2. Choose a monthly cost budget.
3. Enter a limit approved for the lab: `$<amount>`.
4. Add email alerts at 50%, 80%, and 100%.
5. Confirm the budget.

Outcome: unexpected spend produces early notifications. A budget is an alert,
not an automatic service shutdown.

Evidence:

- `[ ] 06-budget-thresholds.png`

### 0.4 CloudTrail baseline

1. Open **CloudTrail → Event history**.
2. Confirm recent management events are present.
3. Filter Event name by `ConsoleLogin`.
4. Open one event and inspect `userIdentity`, `eventTime`, `eventSource`, and
   `sourceIPAddress`.

CloudTrail Event history is enabled automatically and retains 90 days of
management events at no charge. If the supervisor requires the explicit creation
of a trail, create `sentiment-management-trail`, enable all-region management
events and log-file validation, and deliver to a dedicated S3 bucket. Do not
enable S3 object-level data events for every bucket unless required because those
events can add cost.

Evidence:

- `[ ] 07-cloudtrail-event-history.png`
- `[ ] 08-cloudtrail-console-login-event.png`

## Application production changes

- `backend/Dockerfile.ecs` bakes the model into the image for offline startup.
- `frontend/Dockerfile.ecs` uses an ECS-specific NGINX configuration that sends
  `/api` to the backend container over task-localhost.
- The backend creates the schema automatically on a new RDS database.
- The backend can perform an S3 `HeadObject` at startup to prove that its task
  role credentials work. Its task role will receive only `s3:GetObject` on one
  exact verification object.
- Database credentials are read from environment variables. In ECS,
  `DB_PASSWORD` must be injected from Secrets Manager by the task execution role;
  it must never be typed as a plain-text environment variable.

## Evidence log

For every later resource, capture:

1. The final configuration page with identifiers redacted.
2. The security or permissions page.
3. The successful outcome (healthy target, running task, metric, log, or query).
4. Any error page plus a short explanation of cause and resolution.

| Time | Step | Action and reason | Outcome | Screenshot |
|---|---|---|---|---|
| `<time>` | `<step>` | `<what and why>` | `<result>` | `<file>` |

## Cleanup checklist

After the supervisor review, delete paid resources in dependency order:

1. ECS service, then cluster.
2. ALB and target group.
3. RDS instance (choose final snapshot only if required).
4. Interface VPC endpoints.
5. ECR images and repositories.
6. CodeBuild project and build artifacts.
7. Secrets Manager secret (note its scheduled deletion).
8. CloudWatch log groups and alarms.
9. CloudTrail trail and its S3 objects/bucket if no retention is required.
10. VPC networking resources.

Do not delete the IAM administrator until another safe administrative identity
is confirmed.
