# Service Level Objectives (SLO) Document
## Banking Application - OpenBank Cloud Simulation

**Document Version**: 1.0  
**Effective Date**: December 19, 2025  
**Review Cycle**: Monthly  
**Next Review**: January 19, 2026  
**Owner**: DevOps Team (Ntando, Kagiso, Florence, Tumelo)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Service Level Indicators (SLIs)](#service-level-indicators-slis)
3. [Service Level Objectives (SLOs)](#service-level-objectives-slos)
4. [Error Budgets](#error-budgets)
5. [Monitoring & Measurement](#monitoring--measurement)
6. [Incident Response](#incident-response)
7. [Escalation Procedures](#escalation-procedures)
8. [Review & Updates](#review--updates)

---

## 1. Introduction

### 1.1 Purpose

This document defines the Service Level Objectives (SLOs) for the Banking Application, establishing clear expectations for system reliability, performance, and availability. These objectives guide operational decisions and inform our Site Reliability Engineering (SRE) practices.

### 1.2 Scope

This SLO applies to:
-  Banking Application Frontend (Javascript/nginx)
-  Banking Application Backend (FastAPI)
-  MongoDB Database
-  Monitoring Infrastructure (Prometheus, Grafana)

### 1.3 Definitions

**Service Level Indicator (SLI)**: A quantitative measure of a service's behavior (e.g., request success rate, latency)

**Service Level Objective (SLO)**: A target value or range for an SLI over a specific time period (e.g., 99.9% availability over 30 days)

**Error Budget**: The maximum amount of time a service can fail to meet its SLO before triggering remediation actions

**Service Level Agreement (SLA)**: A formal contract with users/customers (future consideration, not yet implemented)

---

## 2. Service Level Indicators (SLIs)

### 2.1 Availability SLI

**Definition**: Percentage of time the service successfully responds to requests

**Measurement**:
```
Availability = (Successful Requests / Total Requests) × 100
```

**Success Criteria**:
- HTTP 2xx response codes
- Response received within timeout period (5 seconds)
- Service reachable and healthy

**Exclusions**:
- Planned maintenance windows (announced 48 hours in advance)
- Client-side errors (4xx except 429)
- DDoS attacks or external infrastructure failures

---

### 2.2 Latency SLI

**Definition**: Time taken to process and respond to requests

**Measurement Percentiles**:
- **P50 (Median)**: 50% of requests complete within this time
- **P95**: 95% of requests complete within this time  
- **P99**: 99% of requests complete within this time

**Measurement Method**:
```prometheus
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Request Types**:
- **Read Operations**: GET requests (account balance, transaction history)
- **Write Operations**: POST/PUT requests (deposits, withdrawals, account creation)
- **Critical Operations**: Authentication, transaction processing

---

### 2.3 Error Rate SLI

**Definition**: Percentage of requests that result in errors

**Measurement**:
```
Error Rate = (Failed Requests / Total Requests) × 100
```

**Error Classification**:
- **5xx Server Errors**: Backend failures, database errors
- **4xx Client Errors**: Invalid requests, authorization failures (tracked but not counted against SLO unless > 5%)
- **Timeouts**: Requests exceeding 5-second threshold

**Measurement Method**:
```prometheus
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
```

---

### 2.4 Throughput SLI

**Definition**: Number of requests processed per second

**Measurement**:
```
Throughput = Total Requests / Time Period (seconds)
```

**Capacity Thresholds**:
- **Normal**: 0-50 requests/second
- **Peak**: 51-100 requests/second
- **Maximum**: 101-200 requests/second (before auto-scaling)

---

## 3. Service Level Objectives (SLOs)

### 3.1 Frontend Service SLOs

#### Availability SLO
- **Target**: 99.95% availability over 30 days
- **Measurement Window**: 30-day rolling window
- **Allowable Downtime**: 21.6 minutes/month

**Why 99.95%?**
- User-facing service requires high availability
- Balances reliability with operational flexibility
- Industry standard for consumer-facing applications

#### Latency SLO
- **P50**: < 1 second (page load time)
- **P95**: < 2 seconds
- **P99**: < 3 seconds

**Why these targets?**
- User experience research shows 2-second threshold for satisfaction
- Static content should load near-instantly
- Accommodates slower network conditions at P99

#### Error Rate SLO
- **Target**: < 0.05% server errors (5xx)
- **Client Errors (4xx)**: < 2% (informational, not counted in budget)

---

### 3.2 Backend Service SLOs

#### Availability SLO
- **Target**: 99.9% availability over 30 days
- **Measurement Window**: 30-day rolling window
- **Allowable Downtime**: 43.2 minutes/month

**Why 99.9%?**
- Core business logic requires high reliability
- Allows for quick deployments and patches
- Balances reliability with agility

#### Latency SLO
- **P50**: < 200ms (API response time)
- **P95**: < 500ms
- **P99**: < 1000ms

**Latency Targets by Endpoint**:

| Endpoint | P50 | P95 | P99 | Justification |
|----------|-----|-----|-----|---------------|
| /health | < 10ms | < 25ms | < 50ms | Simple health check |
| GET /accounts | < 100ms | < 300ms | < 600ms | Single DB query |
| POST /transactions | < 300ms | < 800ms | < 1500ms | Write + validation |
| GET /transactions/history | < 200ms | < 500ms | < 1000ms | Complex query with pagination |

**Why these targets?**
- Based on Week 4 baseline measurements
- Allows for database query time + processing
- Industry-standard for REST APIs

#### Error Rate SLO
- **Target**: < 0.1% server errors (5xx)
- **Critical Transactions**: < 0.01% (deposits, withdrawals)

---

### 3.3 Database Service SLOs

#### Availability SLO
- **Target**: 99.99% availability over 30 days
- **Measurement Window**: 30-day rolling window
- **Allowable Downtime**: 4.32 minutes/month

**Why 99.99%?**
- Data persistence is critical
- Single point of failure currently (future: replication)
- Must support backend SLO targets

#### Latency SLO
- **P50**: < 50ms (query response time)
- **P95**: < 100ms
- **P99**: < 200ms

**Query Type Breakdown**:

| Query Type | P50 | P95 | P99 |
|------------|-----|-----|-----|
| Simple SELECT | < 20ms | < 40ms | < 80ms |
| JOIN Queries | < 100ms | < 200ms | < 400ms |
| INSERT/UPDATE | < 50ms | < 100ms | < 150ms |
| Aggregations | < 150ms | < 300ms | < 500ms |

#### Error Rate SLO
- **Target**: < 0.01% query failures
- **Connection Pool**: Maintain 95% availability

---

### 3.4 Monitoring Infrastructure SLOs

#### Prometheus

- **Availability**: 99.5% over 30 days (43.2 min downtime allowed)
- **Scrape Success Rate**: > 99% for all targets
- **Query Performance**: < 100ms for dashboard queries
- **Data Retention**: 15 days minimum

#### Grafana

- **Availability**: 99.0% over 30 days (7.2 hours downtime allowed)
- **Dashboard Load Time**: < 3 seconds
- **Query Timeout Rate**: < 1%

**Note**: Lower SLOs for monitoring infrastructure acceptable as primary services remain operational during monitoring outages.

---

## 4. Error Budgets

### 4.1 What is an Error Budget?

An error budget is the maximum amount of time a service can fail to meet its SLO before triggering remediation actions. It provides a quantitative measure for balancing reliability with feature velocity.

**Formula**:
```
Error Budget = (1 - SLO) × Time Period
```

### 4.2 Error Budget Allocation

#### Frontend (99.95% SLO)

- **Monthly Budget**: 21.6 minutes downtime
- **Weekly Budget**: 5.04 minutes
- **Daily Budget**: 43 seconds

**Budget Allocation**:
- 40% - Planned deployments and updates
- 30% - Unplanned incidents
- 20% - Dependency failures (backend, network)
- 10% - Reserve for emergencies

#### Backend (99.9% SLO)

- **Monthly Budget**: 43.2 minutes downtime
- **Weekly Budget**: 10.08 minutes
- **Daily Budget**: 1 minute 26 seconds

**Budget Allocation**:
- 35% - Planned deployments and updates
- 35% - Unplanned incidents
- 20% - Database issues
- 10% - Reserve for emergencies

#### Database (99.99% SLO)

- **Monthly Budget**: 4.32 minutes downtime
- **Weekly Budget**: 1.008 minutes
- **Daily Budget**: 8.6 seconds

**Budget Allocation**:
- 50% - Planned maintenance
- 30% - Unplanned incidents
- 20% - Reserve for emergencies

---

### 4.3 Error Budget Policy

#### When Error Budget is Healthy (> 50% remaining)

**Actions**:
-  Proceed with normal feature development
-  Deploy multiple times per day if needed
-  Experiment with new technologies
-  Conduct planned load testing

**Change Approval**:
- Standard review process
- No additional approvals needed
- Self-service deployments allowed

#### When Error Budget is at Risk (25-50% remaining)

**Actions**:
-  Increase deployment scrutiny
-  Require additional code reviews
-  Limit deployments to business hours
-  Enhance monitoring and alerting

**Change Approval**:
- Team lead approval required
- Impact assessment mandatory
- Rollback plan required

**Communication**:
- Weekly error budget review in standup
- Stakeholders notified of risk status

#### When Error Budget is Exhausted (< 25% remaining)

**Actions**:
-  **Feature freeze** - Focus on reliability
-  Only critical bug fixes and security patches
-  No experimental changes
-  Incident postmortems required for all outages

**Change Approval**:
- Senior leadership approval required
- Formal Change Advisory Board (CAB) review
- Detailed risk assessment
- On-call engineer standby for all changes

**Recovery Plan**:
1. Conduct immediate reliability review
2. Identify and fix top contributing issues
3. Implement additional monitoring
4. Schedule postmortem with entire team
5. Update runbooks and documentation

**Budget Reset**: Error budget resets at the start of each month

---

### 4.4 Error Budget Monitoring

#### Dashboard Metrics

Create dedicated Grafana panel:
```prometheus
# Error Budget Consumption (%)
(1 - (sum(rate(http_requests_total{status=~"2.."}[30d])) / sum(rate(http_requests_total[30d])))) / (1 - 0.999) * 100
```

#### Alert Thresholds

| Budget Remaining | Alert Level | Action |
|------------------|-------------|--------|
| > 75% |  Green | No action |
| 50-75% |  Yellow | Monitor closely |
| 25-50% |  Orange | Restrict changes |
| < 25% |  Red | Feature freeze |

---

## 5. Monitoring & Measurement

### 5.1 Data Collection

#### Tools
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Node Exporter**: System-level metrics
- **cAdvisor**: Container metrics

#### Scrape Configuration

```yaml
scrape_configs:
  - job_name: 'backend'
    scrape_interval: 10s
    metrics_path: '/metrics'
    static_configs:
      - targets: ['banking-app-dev-backend:8000']
  
  - job_name: 'frontend'
    scrape_interval: 15s
    metrics_path: '/metrics'
    static_configs:
      - targets: ['banking-app-dev-frontend:80']
```

---

### 5.2 Dashboards

#### Main SLO Dashboard

**Panels**:
1. **Current SLO Compliance** (Stat panel)
   - Frontend: 100% (Target: 99.95%)
   - Backend: 100% (Target: 99.9%)
   - Database: 100% (Target: 99.99%)

2. **Error Budget Remaining** (Gauge panel)
   - Visual indicator of budget health
   - Color-coded alerts (green/yellow/orange/red)

3. **Availability Over Time** (Time series)
   - 30-day rolling window
   - SLO target line overlay

4. **Latency Percentiles** (Time series)
   - P50, P95, P99 trends
   - Target threshold lines

5. **Error Rate** (Time series)
   - 5xx errors over time
   - SLO threshold line

---

### 5.3 Alerting Rules

#### Critical Alerts (P0)

**Backend Availability Below SLO**
```yaml
alert: BackendAvailabilityBelowSLO
expr: |
  (
    sum(rate(http_requests_total{job="backend", status=~"2.."}[5m])) 
    / 
    sum(rate(http_requests_total{job="backend"}[5m]))
  ) < 0.999
for: 5m
labels:
  severity: critical
  priority: P0
annotations:
  summary: "Backend availability below 99.9% SLO"
  description: "Current availability: {{ $value | humanizePercentage }}"
```

**Error Budget Exhaustion**
```yaml
alert: ErrorBudgetExhausted
expr: |
  (error_budget_remaining{service="backend"} / error_budget_total{service="backend"}) < 0.10
for: 5m
labels:
  severity: critical
  priority: P0
annotations:
  summary: "Error budget critically low"
  description: "Only {{ $value | humanizePercentage }} of error budget remaining"
```

#### High Priority Alerts (P1)

**High Latency**
```yaml
alert: HighLatencyP95
expr: |
  histogram_quantile(0.95, 
    rate(http_request_duration_seconds_bucket{job="backend"}[5m])
  ) > 0.5
for: 10m
labels:
  severity: warning
  priority: P1
annotations:
  summary: "P95 latency above 500ms"
  description: "Current P95: {{ $value }}s"
```

**Increased Error Rate**
```yaml
alert: IncreasedErrorRate
expr: |
  rate(http_requests_total{status=~"5.."}[5m]) 
  / 
  rate(http_requests_total[5m]) > 0.01
for: 5m
labels:
  severity: warning
  priority: P1
annotations:
  summary: "Error rate above 1%"
  description: "Current error rate: {{ $value | humanizePercentage }}"
```

---

## 6. Incident Response

### 6.1 Incident Severity Levels

| Priority | Definition | Example | Response Time | Resolution Time |
|----------|------------|---------|---------------|-----------------|
| **P0** | Complete outage | All users cannot access system | 5 minutes | 1 hour |
| **P1** | Major degradation | 50%+ users affected | 15 minutes | 4 hours |
| **P2** | Minor degradation | <50% users affected | 1 hour | 1 day |
| **P3** | Cosmetic issue | No user impact | 4 hours | 1 week |

---

### 6.2 Incident Response Process

#### Phase 1: Detection (0-5 minutes)

**Monitoring Systems**:
- Automated alerts fire (email, Slack)
- Dashboard shows red indicators
- Health check failures detected

**Manual Detection**:
- User reports via support channel
- Team member observes issue
- Scheduled health check failure

**Initial Actions**:
1. Acknowledge alert within 5 minutes
2. Assess severity (P0-P3)
3. Page on-call engineer if P0/P1

---

#### Phase 2: Response (5-30 minutes)

**P0 (Critical) Response**:
1. **0-5 min**: On-call engineer acknowledges
2. **5-10 min**: Initial assessment and triage
3. **10-15 min**: Incident commander assigned
4. **15-30 min**: Communication sent to stakeholders

**Response Team Assembly**:
- **Incident Commander**: Coordinates response
- **Technical Lead**: Diagnoses and fixes issue
- **Communications Lead**: Updates stakeholders
- **Support Lead**: Handles user communications

**Communication Channels**:
- Dedicated Slack channel: `#incident-[date]-[id]`
- Status page updates (if public-facing)
- Stakeholder email updates every 30 minutes

---

#### Phase 3: Mitigation (30 minutes - 4 hours)

**Immediate Actions**:
1. Roll back recent changes if suspected cause
2. Scale resources if capacity issue
3. Restart services if transient failure
4. Failover to backup systems if available

**Investigation**:
- Review recent deployments
- Check system logs and metrics
- Examine error traces
- Query database for anomalies

**Decision Tree**:

```
Issue Detected
│
├─ Recent deployment? 
│  ├─ Yes → Rollback immediately
│  └─ No → Continue investigation
│
├─ Resource exhaustion?
│  ├─ Yes → Scale up resources
│  └─ No → Continue investigation
│
├─ External dependency failure?
│  ├─ Yes → Implement circuit breaker / retry logic
│  └─ No → Continue investigation
│
└─ Code bug identified?
   ├─ Yes → Deploy hotfix
   └─ No → Escalate to senior engineers
```

---

#### Phase 4: Resolution (1-4 hours)

**Verification Steps**:
1. Confirm metrics return to normal
2. Verify error rates below threshold
3. Check error budget consumption
4. Test affected functionality manually
5. Monitor for 15 minutes post-fix

**Declaration of Resolution**:
- Incident Commander confirms resolution
- All metrics green for 15+ minutes
- No new related alerts
- User impact eliminated

**Communication**:
- Update stakeholders: "Incident resolved"
- Post summary in incident channel
- Update status page to "All systems operational"

---

#### Phase 5: Postmortem (24-48 hours after resolution)

**Postmortem Meeting** (Within 48 hours):
- **Duration**: 60 minutes
- **Attendees**: Response team + leadership
- **Facilitator**: Incident Commander or SRE lead

**Postmortem Document Sections**:

1. **Incident Summary**
   - Date, time, duration
   - Severity level
   - Affected services and users
   - Error budget impact

2. **Timeline**
   - Detection time
   - Key events during incident
   - Mitigation steps taken
   - Resolution time

3. **Root Cause Analysis**
   - Primary cause
   - Contributing factors
   - Why issue wasn't caught earlier

4. **Impact Assessment**
   - User impact (quantified)
   - Business impact
   - Error budget consumption
   - Financial impact (if applicable)

5. **What Went Well**
   - Effective actions
   - Good communication
   - Proper use of runbooks

6. **What Went Poorly**
   - Delayed detection
   - Communication gaps
   - Missing tools or runbooks

7. **Action Items**
   - Prevent recurrence
   - Improve detection
   - Enhance response
   - Update documentation

**Action Item Template**:
| Action | Owner | Due Date | Priority | Status |
|--------|-------|----------|----------|--------|
| Add monitoring for X | Ntando | Dec 25 | P1 | Open |
| Update runbook for Y | Kagiso | Dec 23 | P2 | In Progress |

**Follow-up**:
- Review action items in weekly standup
- Close action items only when verified
- Update runbooks and documentation
- Share learnings with broader team

---

### 6.3 Runbooks

#### Runbook: Backend Service Down

**Symptoms**:
- Health check endpoint returning 503
- Grafana shows "Backend" service status = 0
- Users cannot login or perform transactions

**Diagnosis**:
```bash
# Check container status
docker ps | grep banking-app-dev-backend

# Check container logs
docker logs banking-app-dev-backend --tail 100

# Check resource usage
docker stats banking-app-dev-backend
```

**Resolution Steps**:

1. **Restart Container** (First attempt)
   ```bash
   docker restart banking-app-dev-backend
   
   # Wait 30 seconds
   curl http://localhost:8000/health
   ```

2. **Check Configuration** (If restart fails)
   ```bash
   # Verify environment variables
   docker inspect banking-app-dev-backend | grep -A 20 Env
   
   # Check database connectivity
   docker exec banking-app-dev-backend python -c "from motor.motor_asyncio import AsyncIOMotorClient; print(AsyncIOMotorClient('mongodb://banking-mongodb:27017').list_database_names())"
   ```

3. **Rebuild Container** (If config OK)
   ```bash
   cd ~/Banking-System-Front-End
   docker-compose build backend
   docker-compose up -d backend
   ```

4. **Rollback** (If rebuild fails)
   ```bash
   git log --oneline -10  # Find last good commit
   git checkout <commit-sha>
   docker-compose build backend
   docker-compose up -d backend
   ```

**Escalation**: If all steps fail, escalate to P0 incident and page senior engineer.

---

#### Runbook: High Memory Usage

**Symptoms**:
- Memory usage > 1.5 GB
- Container restarts frequently
- Application becomes unresponsive

**Diagnosis**:
```bash
# Check memory usage
docker stats --no-stream

# Inspect memory allocation
docker exec <container> ps aux --sort=-%mem | head
```

**Resolution Steps**:

1. **Identify Memory Leak**
   ```bash
   # Check for unclosed connections
   docker exec banking-app-dev-backend lsof | grep -i ESTABLISHED | wc -l
   
   # Check Python heap (if applicable)
   docker exec banking-app-dev-backend python -c "import gc; gc.collect(); print(f'Objects: {len(gc.get_objects())}')"
   ```

2. **Temporary Mitigation**
   ```bash
   # Restart container to free memory
   docker restart <container>
   ```

3. **Long-term Fix**
   - Review code for memory leaks
   - Implement connection pooling
   - Add memory limits to container
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 1G
   ```

**Prevention**:
- Set up memory alert at 80% threshold
- Regular code reviews for resource management
- Load testing to identify leaks early

---

#### Runbook: Database Connection Failures

**Symptoms**:
- Backend logs show "ConnectionFailure" errors
- Transactions timeout
- API returns 500 errors

**Diagnosis**:
```bash
# Check MongoDB container
docker ps | grep banking-mongodb

# Check MongoDB logs
docker logs banking-mongodb --tail 100

# Test connection from backend
docker exec banking-app-dev-backend nc -zv banking-mongodb 27017
```

**Resolution Steps**:

1. **Verify MongoDB Health**
   ```bash
   docker exec banking-mongodb mongosh --eval "db.adminCommand('ping')"
   ```

2. **Check Connection Pool**
   ```bash
   docker exec banking-mongodb mongosh --eval "db.serverStatus().connections"
   ```

3. **Restart MongoDB** (If unhealthy)
   ```bash
   docker restart banking-mongodb
   
   # Wait 60 seconds for startup
   docker logs banking-mongodb --tail 20
   ```

4. **Verify Data Integrity**
   ```bash
   docker exec banking-mongodb mongosh banking_db --eval "db.accounts.count()"
   ```

**Escalation**: If data corruption suspected, immediately escalate to P0 and involve database administrator.

---

## 7. Escalation Procedures

### 7.1 Escalation Matrix

| Level | Role | Contact | Conditions |
|-------|------|---------|------------|
| **L1** | On-Call Engineer | Slack/Phone | Initial response |
| **L2** | Team Lead | Phone | P0/P1 after 30 min |
| **L3** | Senior Engineer | Phone | Technical escalation |
| **L4** | Engineering Manager | Phone | P0 after 1 hour |
| **L5** | CTO/VP Engineering | Phone | Major outage > 2 hours |

### 7.2 Escalation Triggers

**Automatic Escalation**:
- P0 incident unresolved after 30 minutes → L2
- P1 incident unresolved after 2 hours → L2
- Error budget exhausted → L3 + L4
- Data loss or corruption suspected → Immediate L4

**Manual Escalation**:
- Engineer requests additional expertise
- Issue requires architectural changes
- Multiple services affected
- Customer-facing impact worsening

### 7.3 Communication Escalation

**Internal Communication**:
- Every 30 minutes for P0
- Every 2 hours for P1
- Daily updates for P2/P3

**External Communication** (Future):
- Status page updates
- Twitter/social media (if public)
- Customer emails for affected accounts
- Post-incident summary

---

## 8. Review & Updates

### 8.1 Regular Reviews

**Monthly SLO Review** (First Monday of month):
- **Attendees**: Full DevOps team
- **Duration**: 60 minutes
- **Agenda**:
  1. Review SLO compliance for previous month
  2. Analyze error budget consumption
  3. Review incidents and patterns
  4. Adjust SLOs if needed
  5. Plan improvements for next month

**Quarterly SLO Calibration** (First week of quarter):
- **Attendees**: Team + leadership
- **Duration**: 90 minutes
- **Agenda**:
  1. Comprehensive SLO effectiveness review
  2. User feedback on service quality
  3. Industry benchmark comparison
  4. Propose SLO adjustments for next quarter
  5. Align with business objectives

---

### 8.2 SLO Adjustment Process

**When to Adjust SLOs**:
-  Consistently meeting/exceeding SLOs by wide margin (> 10%)
-  Consistently missing SLOs (< 90% compliance)
-  Business requirements change
-  User feedback indicates quality issues
-  System architecture significantly changes

**Adjustment Proposal**:
1. Document current performance vs SLO
2. Analyze user impact
3. Consider operational feasibility
4. Draft new SLO proposal
5. Get team consensus
6. Get leadership approval
7. Update documentation
8. Communicate changes

**Example**:
> *Current*: Backend availability SLO of 99.9% has been exceeded for 3 consecutive months (actual: 99.98%)
> 
> *Proposal*: Increase to 99.95% to challenge team while remaining achievable
> 
> *Rationale*: System maturity allows for tighter SLO; user expectations increasing
> 
> *Impact*: Error budget reduced from 43.2 min to 21.6 min per month; requires enhanced monitoring

---

### 8.3 Document Maintenance

**Document Owner**: Ntando (Primary), Kagiso (Backup)

**Update Triggers**:
- SLO adjustments
- New services added
- Incident response process improvements
- Team structure changes
- Tooling changes

**Version History**:

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Dec 18, 2025 | Initial document | DevOps Team |
| | | | |

---

## 9. Appendices

### Appendix A: SLO Calculations Reference

**Availability Calculation**:
```
Availability (%) = (Total Time - Downtime) / Total Time × 100
```

**Error Budget Calculation**:
```
Error Budget (minutes) = (1 - SLO) × Time Period × 60
```

**Example for 99.9% SLO over 30 days**:
```
Error Budget = (1 - 0.999) × 30 days × 24 hours × 60 minutes
             = 0.001 × 43,200 minutes
             = 43.2 minutes
```

### Appendix B: Prometheus Queries

**Availability**:
```prometheus
sum(rate(http_requests_total{status=~"2.."}[30d])) 
/ 
sum(rate(http_requests_total[30d]))
```

**Latency P95**:
```prometheus
histogram_quantile(0.95, 
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```

**Error Rate**:
```prometheus
sum(rate(http_requests_total{status=~"5.."}[5m])) 
/ 
sum(rate(http_requests_total[5m]))
```


## Conclusion

This SLO document establishes a clear framework for measuring and maintaining the reliability of the Banking Application as part of the 4-week IBM DevOps project completion. By defining specific, measurable objectives and error budgets, we demonstrate understanding of how to balance reliability needs with development agility.

**Key Takeaways**:
-  Clear SLOs for all critical services
-  Error budgets guide development velocity
-  Incident response procedures documented
-  Regular review process established
-  Alignment with IBM SRE best practices
-  **Project successfully completed**

**Project Completion Status**:
This document represents the final deliverable for Week 4 of the OpenBank Cloud Simulation - IBM DevOps Edition project. All monitoring, SRE documentation, and observability objectives have been achieved.

**For Future Production Deployment**:
1. Implement all alert rules in Prometheus
2. Create dedicated SLO dashboard in Grafana
3. Begin tracking error budget consumption
4. Configure notification channels
5. Establish on-call rotation

---

**Document Status**:  Approved  
**Project Completion Date**: December 19, 2025  
**4-Week Project Status**: Complete  
**Version**: 1.0  
**Classification**: Internal - Team Use

---

*This document aligns with IBM Site Reliability Engineering Professional Certificate principles and Google SRE best practices. Completed as part of the 4-week OpenBank Cloud Simulation - IBM DevOps Edition project.*
