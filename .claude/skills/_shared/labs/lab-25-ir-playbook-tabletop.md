# Lab 25 — Incident Response Playbook and Tabletop

In this lab you will draft a NIST-aligned **incident response plan**, a one-page **playbook**, and run a 45-minute **tabletop exercise** against the scenario from Lab 20. This maps to CySA+ 3.3 (Preparation — IR plan, Tools, Playbooks, Tabletop, Training, BC/DR; Post-incident — Forensic analysis, Root cause, Lessons learned).

Most of this lab is written/spoken work — no shell required.

---

## Step 1 — The NIST 800-61 incident-response life cycle

```
┌──────────────┐    ┌────────────────┐    ┌─────────────────────┐    ┌────────────────┐
│ Preparation  │ -> │ Detection &    │ -> │ Containment,        │ -> │ Post-incident  │
│              │    │ Analysis       │    │ Eradication,        │    │ Activity       │
│              │    │                │    │ & Recovery          │    │                │
└──────────────┘    └────────────────┘    └─────────────────────┘    └────────────────┘
        ▲                                                                      │
        └──────────────────────────────────────────────────────────────────────┘
                                  Feedback (Lessons Learned)
```

CySA+ 3.3 is exactly this loop with two of its four phases broken out.

---

## Step 2 — Author the high-level IR plan

```bash
mkdir -p /tmp/lab25 && cd /tmp/lab25
cat > ir_plan.md <<'EOF'
# Incident Response Plan v1.0

## 1. Purpose & scope
Covers all production systems and customer data. Aligned to NIST 800-61.

## 2. Roles (RACI)
- **Incident Commander (IC)** — Senior SOC lead. Decides comms and escalation.
- **Lead Analyst** — Runs detection, analysis, evidence.
- **Engineering** — Containment / eradication / recovery.
- **Comms** — Customer + media + regulator (Lab 30).
- **Legal** — Privilege, law enforcement, regulatory.
- **Executive sponsor** — CISO; signs the closure.

## 3. Severity classification
| Sev | Definition                            | SLA to declare | Notify |
|-----|---------------------------------------|----------------|--------|
| 1   | Confirmed data exfil / system-wide    | 15 min         | CISO, CEO, Legal |
| 2   | Confirmed compromise, contained scope | 30 min         | CISO   |
| 3   | Suspicious activity, unverified       | 1 hr           | SOC mgr |
| 4   | Informational                         | next biz day   | none   |

## 4. Communication channels
- War room: #incident-NNN (Slack)
- Bridge: conference URL (link)
- Out-of-band: pre-shared Signal group (in case primary IdP is compromised)

## 5. Tooling list (Preparation)
- SIEM, EDR, NDR, SOAR, ticket system
- Forensic kit: write-blocker, FTK Imager, Volatility, KAPE
- Threat-intel: MISP, AbuseIPDB, VirusTotal Premium
- Comms templates: pre-approved exec, customer, regulator messages

## 6. Authority matrix
- IC may shut down a production system.
- IC may not talk to media without Comms approval.
- Legal may invoke a legal hold (Lab 21).

## 7. Business continuity / disaster recovery hand-off
If RTO of an isolated system is breached, invoke BC/DR plan ABC-DR-007.
EOF
```

---

## Step 3 — Author a one-page phishing playbook

```bash
cat > playbook_phishing.md <<'EOF'
# Playbook — Phishing email reported by user

## Trigger
User report or DMARC failure alert.

## Step 1 — Triage (≤ 15 min)
- Pull headers (Lab 8). Verify SPF/DKIM/DMARC.
- Extract URLs / attachments. Hash any attachment (Lab 9).
- VirusTotal + AbuseIPDB on every IOC (Lab 10).

## Step 2 — Scope (≤ 30 min)
- Query mail gateway: who else received the message? Block or quarantine.
- Query SIEM: any user click on the URL? (Web proxy logs.)
- Query EDR: any process spawned from the attachment?

## Step 3 — Contain (≤ 60 min)
- Block sender, URL, hash in email/web/EDR.
- For clickers: isolate host (Lab 24), force password reset, invalidate sessions.

## Step 4 — Eradicate / Recover
- Remove every copy from mailboxes (mass purge).
- Re-image clicked hosts if RCE confirmed.

## Step 5 — Post-incident
- Log IOCs to threat-intel.
- Update awareness training with the lure (Lab 30).
EOF
```

---

## Step 4 — Run a 45-minute tabletop exercise

**Scenario (read aloud at T = 0):**
> "08:00 — A finance user reports an invoice email looked off but opened it. Outlook closed unexpectedly. At 08:15 EDR alerts on `powershell.exe → curl → 185.220.101.45`. The user's password was used at 08:30 to log into the file share."

Run the clock in **5-minute injects**. At each inject the facilitator throws a curveball; the team must say **who** does **what** and **with which playbook step**.

| T+min | Inject |
|---|---|
| 0   | Initial detect — open ticket, assign IC, declare severity |
| 5   | Press starts calling — Comms hat goes on |
| 10  | EDR isolation fails on legacy host — alternative containment? |
| 15  | Legal asks: is this notifiable? Which regulator? |
| 25  | Fresh DLP alert: 1 GB to Dropbox — exfiltration confirmed |
| 35  | Executive demands status — who briefs and with what template? |
| 40  | Eradication or re-image decision (Lab 24) |
| 45  | Hot wash: 3 things to fix this week, 1 thing to fix this quarter |

---

## Step 5 — Capture lessons learned (post-incident)

```bash
cat > hot_wash.md <<'EOF'
# Hot Wash — Tabletop Phishing Exercise

## What went well
- Triage time within SLA.
- Comms had the template ready.

## What went badly
- EDR isolation on legacy 2012 host failed.
- Out-of-band comms channel out of date.
- No regulator notification template available.

## Action items
| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Network-ACL isolation for legacy hosts | Platform | $(date -d '+14 days' -I) |
| 2 | Refresh OOB Signal group quarterly | SOC | $(date -d '+30 days' -I) |
| 3 | Build regulator notification template | Legal | $(date -d '+30 days' -I) |
EOF
```

These actions become the inputs to the next Preparation cycle — closing the NIST loop.

---

## Step 6 — Training (CySA+ 3.3 "Training")

Schedule four touches per year:

1. Q1 — All-hands phishing simulation.
2. Q2 — Tabletop (this lab).
3. Q3 — Red-team purple-team exercise.
4. Q4 — Full BC/DR simulated outage.

---

## What you learned
- The NIST 800-61 IR life cycle and how it maps to CySA+ 3.3.
- Draft a high-level IR plan with RACI, severity, and escalation.
- Author a one-page playbook for the most common incident type.
- Run a structured tabletop and capture lessons learned that feed back into preparation.
