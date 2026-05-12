# Lab 26 — Vulnerability Management Report

In this lab you will turn raw OpenVAS / Nmap output into a stakeholder-ready vulnerability report with a risk score, affected hosts, mitigations, and an action plan. This maps to CySA+ 4.1 (Vulnerability management reporting — Vulnerabilities, Affected hosts, Risk score, Mitigation, Recurrence, Prioritization; Compliance reports; Action plans; Inhibitors to remediation).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install report tooling

```bash
apt update && apt install -y pandoc texlive-latex-base texlive-fonts-recommended 2>/dev/null
```

`pandoc` converts Markdown → PDF / HTML / DOCX with one command. The TeX packages are large; if Killercoda is slow, skip them and render to HTML instead.

---

## Step 2 — Seed input data (pretend it came from OpenVAS)

```bash
mkdir -p /tmp/lab26 && cd /tmp/lab26
cat > findings.csv <<'EOF'
CVE,Host,Service,CVSS,EPSS,KEV,FirstSeen,Status
CVE-2024-1234,web01.example,nginx 1.18,9.8,0.97,Yes,2026-05-01,Open
CVE-2024-2222,web01.example,openssl 1.1.1,7.5,0.21,No,2026-05-01,Open
CVE-2023-9999,db01.example,mysql 5.7,8.2,0.45,No,2026-04-15,Open-Recurring
CVE-2022-1111,jump01.example,openssh 7.6,6.5,0.10,No,2026-05-12,Open
CVE-2021-5555,legacy01.example,iis 7.5,9.8,0.88,Yes,2026-01-01,Accepted-Risk
EOF
```

The columns map directly to CySA+ 4.1's bullet list: Vulnerabilities, Affected hosts, Risk score, Recurrence.

---

## Step 3 — Compute the prioritisation column

```bash
awk -F, 'NR==1 {print $0",Priority"; next}
  {
    score = $4 + 0
    if ($6 == "Yes" || score >= 9.0) p="P1"
    else if (score >= 7.0)            p="P2"
    else if (score >= 4.0)            p="P3"
    else                              p="P4"
    print $0","p
  }' findings.csv > prioritised.csv
column -ts, prioritised.csv
```

Prioritisation logic mirrors CySA+ 2.3 + 4.1: KEV catalog hits and CVSS ≥ 9 are always P1.

---

## Step 4 — Build the executive summary

```bash
cat > report.md <<'EOF'
# Monthly Vulnerability Management Report — May 2026

**Audience:** CISO, Engineering leads
**Prepared by:** SOC Vulnerability Management Team
**Reporting period:** 2026-05-01 → 2026-05-13

## Executive summary

This month we identified **5 open vulnerabilities** across 4 hosts. Two are on the CISA Known Exploited Vulnerabilities (KEV) catalog and require P1 action. One issue is **recurring** on `db01` — patch reverted by a configuration rollback on 2026-05-08 (root cause: change-management gap).

| Metric (KPI) | This period | Last period | Δ |
|---|---|---|---|
| Total open | 5 | 4 | +1 |
| P1 critical | 2 | 1 | +1 |
| Mean time to remediate (MTTR) | 18 days | 22 days | −4 |
| % patched within SLA | 78% | 71% | +7 |
| Recurring findings | 1 | 0 | +1 |

## Top 10 vulnerabilities (CySA+ 4.1 "Top 10")

| # | CVE | Host | CVSS | KEV | Priority |
|---|-----|------|------|-----|----------|
| 1 | CVE-2024-1234 | web01 | 9.8 | Yes | P1 |
| 2 | CVE-2021-5555 | legacy01 | 9.8 | Yes | P1 (Risk Accepted) |
| 3 | CVE-2023-9999 | db01 | 8.2 | No | P2 (Recurring) |
| 4 | CVE-2024-2222 | web01 | 7.5 | No | P2 |
| 5 | CVE-2022-1111 | jump01 | 6.5 | No | P3 |

## Action plan

| # | Action | Owner | Due | Type |
|---|--------|-------|-----|------|
| 1 | Patch nginx 1.18 → 1.26 on web01 | Platform | 2026-05-15 | Patching |
| 2 | Investigate db01 patch reversion; freeze config drift | DBA + Change | 2026-05-17 | Configuration management |
| 3 | Compensating control on legacy01: WAF rule + segmentation | NetOps | 2026-05-20 | Compensating control |
| 4 | Refresh OpenSSH on jump01 next maintenance window | Platform | 2026-05-31 | Patching |

## Inhibitors to remediation (CySA+ 4.1)

| Inhibitor | Affected item | Mitigation |
|---|---|---|
| MOU with partner pins legacy01 to IIS 7.5 | #2 | WAF + segmentation, document risk acceptance |
| SLA window only allows monthly DB patching | #2 | Move db01 to weekly patch cadence |
| Business process interruption risk on web01 | #1 | Schedule blue-green deploy |
| Legacy system (IIS 7.5) | #2 | Plan retirement Q3 2026 |

## Compliance posture

- **PCI DSS 11.3** quarterly external scan: PASS, last run 2026-05-05.
- **ISO 27001 A.12.6** technical vulnerability management: documented, evidence in this report.
- **Internal SLA**: P1 = 7 d, P2 = 30 d, P3 = 90 d.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| CISO | Risk score trend, KEV exposure |
| Engineering leads | Action items, owners, due dates |
| Audit | Compliance posture, evidence pointers |
| Business owners | Inhibitors, accepted risks |
EOF
```

---

## Step 5 — Render to HTML and (optionally) PDF

```bash
pandoc report.md -s -o report.html
ls -lh report.html
# pandoc report.md -o report.pdf      # uncomment if TeX is installed
```

Open `report.html` in a browser to verify formatting before mailing.

---

## Step 6 — Hash and archive

```bash
sha256sum report.md report.html prioritised.csv > MANIFEST.sha256
ls -lh
```

Reports are evidence; hashes prove integrity (and the auditor will check).

---

## Step 7 — Map every section to a CySA+ 4.1 bullet

| Section | CySA+ 4.1 bullet |
|---|---|
| KPI table | Metrics and KPIs (Trends, Top 10, SLOs) |
| Top 10 | Top 10 |
| Action plan | Action plans (Configuration management, Patching) |
| Inhibitors table | Inhibitors to remediation (MOU, SLA, Org governance, Business process interruption, Legacy systems) |
| Compliance posture | Compliance reports |
| Stakeholders | Stakeholder identification and communication |
| Recurrence row | Recurrence |

---

## What you learned
- Prioritise vulnerabilities with KEV + CVSS.
- Author a stakeholder-grade vulnerability report with executive summary, Top 10, action plan, inhibitors, and compliance posture.
- Render Markdown to HTML/PDF with `pandoc`.
- Map every section back to the CySA+ 4.1 exam blueprint.
