# Lab 27 — Executive Incident Report

In this lab you will write the executive incident report from the scenario walked in Labs 20, 23, 24. It will satisfy every CySA+ 4.2 bullet: executive summary, Who-What-When-Where-Why, recommendations, timeline, impact, scope, evidence, communications, root cause, lessons learned, metrics.

Most of this lab is writing — no shell required. The output is a single Markdown file rendered with `pandoc`.

---

## Step 1 — Tools

```bash
apt update && apt install -y pandoc
mkdir -p /tmp/lab27 && cd /tmp/lab27
```

---

## Step 2 — Use the canonical IR report template

```bash
cat > incident_report.md <<'EOF'
# Incident Report — CASE-001 (Finance Department Phishing → Data Exfiltration)

**Classification:** Internal — Confidential
**Date:** 2026-05-13
**Author:** SOC Lead Analyst
**Approver:** CISO

---

## 1. Executive summary
On 2026-05-13 at 08:00 UTC, a member of the Finance team opened a phishing email impersonating PayPal. The macro-laden attachment delivered a PowerShell downloader that established command-and-control with `185.220.101.45`. Within 10 minutes the attacker authenticated to the internal file share via stolen credentials and exfiltrated approximately **1 GB of data over HTTPS**. The compromised user account was disabled at 08:30, the host isolated at 08:45, and the second-stage payload eradicated by 11:00. There is **no evidence of further lateral movement**. Containment held.

## 2. Who, what, when, where, why
| Field | Value |
|-------|-------|
| **Who**  | Single Finance user (badge #FN-104); attacker IP 185.220.101.45 (TOR exit, Russia geo-tag) |
| **What** | Phishing → macro → PowerShell downloader → credential theft → 1 GB exfil |
| **When** | 2026-05-13 08:00 → 11:00 UTC (3 h to full eradication) |
| **Where**| Workstation `FN-WS-014` and File Server `FS01` |
| **Why**  | Macro execution was permitted by GPO; user not on phishing-resistant MFA |

## 3. Timeline (UTC)

| Time     | Event                                                  | Evidence            |
|----------|--------------------------------------------------------|---------------------|
| 08:00    | Phishing email delivered, opened                       | mail-gw, Lab 8      |
| 08:01    | Macro spawns PowerShell, downloads stage 2             | EDR alert           |
| 08:05    | C2 heartbeat begins to 185.220.101.45                  | Lab 4 beacon        |
| 08:15    | EDR alert raised; ticket INC-001 opened                | EDR, ticket system  |
| 08:20    | Brute-force noise observed on FS01 (Lab 7)             | auth.log            |
| 08:30    | Compromised account disabled at IdP                    | IdP audit log       |
| 08:30    | Outbound 1 GB flow to attacker domain                  | NetFlow             |
| 08:45    | FN-WS-014 network-isolated (Lab 24)                    | firewall log        |
| 09:30    | Memory + disk imaged for forensics (Lab 21)            | Chain of custody    |
| 11:00    | Workstation re-imaged; user retrained                  | Endpoint mgmt       |

## 4. Impact and scope
- **Confidentiality:** ~1 GB exfiltrated. Sample contains: 87 customer records (names, IBANs, emails). Falls under GDPR (notification within 72 h).
- **Integrity:** No evidence of modification on FS01.
- **Availability:** None. Production was not interrupted.
- **Scope:** 1 user, 1 workstation, 1 file share path `/finance/customers/`.

## 5. Evidence (CySA+ 4.2 "Evidence")
| ID | Item | Hash (SHA-256) | Custodian |
|----|------|----------------|-----------|
| EV-001 | FN-WS-014 disk image | `a1b2c3…` | Forensics (locker 3) |
| EV-002 | FN-WS-014 memory image | `d4e5f6…` | Forensics (locker 3) |
| EV-003 | Phishing email .eml | `070809…` | SOC archive |
| EV-004 | Outbound netflow window | `0a0b0c…` | SOC archive |

Chain of custody form: see CASE-001 chain_of_custody.md (Lab 21).

## 6. Root cause analysis (CySA+ 4.2 "Root cause analysis")
| Layer | Failure |
|-------|---------|
| **Email** | DMARC policy on receiving domain set to `none` — forgery passed quarantine. |
| **Endpoint** | Macros allowed from internet zone; PowerShell constrained-language mode disabled. |
| **Identity** | MFA was OTP, not phishing-resistant; reusable credential captured. |
| **Network** | Egress from finance VLAN to TOR exits was not blocked. |
| **Detection** | SIEM rule for beaconing existed but threshold too lenient (>30 s). |

## 7. Recommendations
| # | Recommendation | Owner | Target |
|---|----------------|-------|--------|
| 1 | Enforce DMARC `p=reject` on receiving gateway | Email Ops | 2026-05-31 |
| 2 | Block macros from internet zone via Group Policy | Endpoint | 2026-05-20 |
| 3 | Roll out FIDO2 keys for Finance + Exec | IdAM | 2026-07-01 |
| 4 | Egress filter: deny TOR exit nodes at perimeter | NetOps | 2026-05-22 |
| 5 | Tighten SIEM beaconing detection (<= 60 s, jitter aware) | Detection eng | 2026-06-10 |

## 8. Lessons learned (CySA+ 4.2 "Lessons learned")
- **Worked:** Tabletop muscle memory (Lab 25). IC named within 5 min.
- **Worked:** Pre-built isolation runbook applied cleanly (Lab 24).
- **Failed:** Out-of-band Signal group was 3 months out of date.
- **Failed:** No standing template for the regulator notification — Legal had to draft from scratch under pressure.

## 9. Metrics and KPIs
| Metric | Value | Target |
|--------|-------|--------|
| Mean time to **detect** (MTTD) | 15 min | < 30 min |
| Mean time to **respond** (MTTR-r) | 45 min | < 1 h |
| Mean time to **remediate** (MTTR-m) | 3 h | < 4 h |
| Alert volume (24 h) | 412 → 1 incident | n/a |

## 10. Communications (CySA+ 4.2 "Communications")
| Audience | Channel | Sender | Sent |
|----------|---------|--------|------|
| Executive | Email + bridge | CISO | 09:00 |
| Affected customers | Templated email | Comms | 13:00 |
| Regulator (GDPR DPA) | Web form + signed letter | Legal | within 72 h |
| Law enforcement (cybercrime unit) | Phone + signed referral | Legal | 14:00 |
| Public relations / media | Holding statement only | Comms | as needed |

## 11. Incident declaration & escalation
- Sev: **1**
- Declared by: SOC Lead Analyst
- Time declared: 08:30 UTC
- Escalation: CISO @ 08:35, CEO @ 09:00, Legal @ 09:15

## 12. Stakeholder identification (CySA+ 4.2)
CISO; CEO; CFO (because Finance scope); Legal; Comms; Engineering platform; Affected customers; Supervisory Authority (regulator); Cyber-insurance carrier.

---

*End of report.*
EOF
```

---

## Step 3 — Render and seal

```bash
pandoc incident_report.md -s -o incident_report.html
sha256sum incident_report.* > MANIFEST.sha256
ls -lh
```

The hash is the seal — once distributed, any edit changes the hash and breaks the audit trail.

---

## Step 4 — Map every section to CySA+ 4.2

| Section | CySA+ 4.2 bullet |
|---|---|
| 1 Exec summary | Executive summary |
| 2 W/W/W/W/W | Who, what, when, where, and why |
| 3 Timeline | Timeline |
| 4 Impact / scope | Impact, Scope |
| 5 Evidence | Evidence |
| 6 RCA | Root cause analysis |
| 7 Recommendations | Recommendations |
| 8 Lessons learned | Lessons learned |
| 9 Metrics | Metrics and KPIs (MTTD/MTTR/Alert volume) |
| 10 Communications | Communications (Legal, PR, Customer, Media, Regulatory, LE) |
| 11 Declaration | Incident declaration and escalation |
| 12 Stakeholders | Stakeholder identification and communication |

---

## What you learned
- Author a complete executive incident report that satisfies every CySA+ 4.2 bullet.
- Cleanly link evidence to chain-of-custody (Lab 21).
- Capture lessons learned and KPIs that feed the next preparation cycle.
- Render and seal a report with `pandoc` + SHA-256.
