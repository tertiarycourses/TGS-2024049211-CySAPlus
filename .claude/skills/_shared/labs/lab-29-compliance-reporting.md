# Lab 29 — Compliance Reporting (PCI DSS / ISO 27001 / NIST CSF)

In this lab you will produce a compliance crosswalk that maps your lab evidence to **PCI DSS**, **ISO 27001 Annex A**, **NIST CSF**, and **CIS Controls v8** — the four frameworks CySA+ 2.1 / 4.1 expects you to recognise. This is the lab the auditor reads.

No shell required — produce a single Markdown deliverable.

---

## Step 1 — Why a crosswalk?

Most organisations are subject to multiple frameworks. A crosswalk avoids re-running the same control three times under three names. You demonstrate **one** technical control once and reference it from each framework.

---

## Step 2 — Pull the framework primary sources (free)

- **PCI DSS v4.0** — https://www.pcisecuritystandards.org
- **ISO 27001:2022** (overview) — https://www.iso.org/isoiec-27001-information-security.html
- **NIST CSF 2.0** — https://www.nist.gov/cyberframework
- **CIS Controls v8** — https://www.cisecurity.org/controls

For internal training, the open OWASP, OSSTMM, and CIS Benchmarks are also useful (CySA+ 2.1 names them).

---

## Step 3 — Build the crosswalk

Save as `crosswalk.md`:

```markdown
# Control crosswalk — Lab evidence ↔ Frameworks

| Control area | Lab evidence | PCI DSS v4 | ISO 27001:2022 | NIST CSF 2.0 | CIS v8 |
|---|---|---|---|---|---|
| Asset inventory | Lab 11 (Nmap inventory) | 9.5, 12.5 | A.5.9 | ID.AM-1/2 | 1.1 |
| Vuln scanning | Lab 12 (OpenVAS) | 11.3.1/11.3.2 | A.8.8 | ID.RA-1, PR.IP-12 | 7.1, 7.6 |
| Web app scan | Lab 13 (ZAP) | 6.4.1 | A.8.29 | PR.IP-7, DE.CM-8 | 16.11 |
| Patch mgmt | Lab 18 | 6.3.3 | A.8.8 | PR.IP-12 | 7.4 |
| Hardening | Lab 2, Lab 18 (Lynis) | 2.2 | A.8.9 | PR.IP-1 | 4 |
| Log ingest + time | Lab 1 | 10.4, 10.6 | A.8.15, A.8.17 | DE.AE-3, PR.PT-1 | 8 |
| SIEM correlation | Lab 7 | 10.4, 10.6 | A.8.16 | DE.CM-1/3 | 8.11 |
| Email security | Lab 8 | 5.4.1 | A.5.34 | PR.DS-2 | 9.7 |
| Threat intel | Lab 10 | 6.3.1 | A.5.7 | ID.RA-2, ID.RA-3 | 13.1 |
| Network segmentation | Lab 3 | 1.4, 1.5 | A.8.22 | PR.AC-5 | 12 |
| Containment / isolation | Lab 24 | 12.10.5 | A.5.26 | RS.MI-1 | 17.5 |
| Forensics / chain of custody | Lab 21 | 12.10.4 | A.5.28 | RS.AN-1/3 | 17 |
| IR plan / tabletop | Lab 25 | 12.10.1, 12.10.2 | A.5.24, A.5.25 | RS.RP-1, RC.RP-1 | 17.4 |
| Reporting & metrics | Lab 26, 27, 28 | 12.10.7 | A.5.27 | RS.CO-2/3 | 17.6 |
```

---

## Step 4 — Generate compliance evidence files

For each control area, produce one **named** evidence file pointing at the underlying lab artefact:

| Evidence ID | Description | Source artefact |
|---|---|---|
| E-VM-2026Q2 | Quarterly vuln scan | `report.html` from Lab 26 |
| E-IR-CASE001 | Incident report | `incident_report.md` from Lab 27 |
| E-CoC-001 | Chain of custody | `chain_of_custody.md` from Lab 21 |
| E-LOG-RET | 12-month log retention | rsyslog config + sample rotation log (Lab 1) |
| E-HRD-LYN-05 | Hardening scan May 2026 | `/var/log/lynis.log` from Lab 18 |
| E-CSF-SEG | Segmentation diagram | Lab 3 namespace diagram |

Hash every file:

```bash
sha256sum *.md *.csv *.html > MANIFEST.sha256
```

---

## Step 5 — Compliance report skeleton

```markdown
# Compliance Report — Q2 2026

**Scope:** Cardholder data environment + customer PII systems
**Frameworks:** PCI DSS v4.0, ISO 27001:2022, NIST CSF 2.0, CIS v8
**Reporting period:** 2026-04-01 → 2026-06-30
**Author:** SOC Compliance Lead
**Approver:** CISO

## 1. Executive summary
All in-scope PCI controls were exercised in this period. Two ISO 27001 controls (A.5.30 ICT readiness, A.7.5 protecting against physical threats) have **observations** — see §5.

## 2. Control crosswalk
See `crosswalk.md`.

## 3. Evidence index
See `evidence-index.csv`.

## 4. Open audit findings
| Finding | Framework | Risk | Owner | Due |
|---------|-----------|------|-------|-----|
| Quarterly scan ran 4 days late in April | PCI 11.3.1 | Low | Platform | 2026-06-30 |
| BC/DR tabletop overdue | ISO A.5.30 | Med | CISO office | 2026-07-31 |

## 5. Risk acceptances
| Risk | Justification | Sign-off | Review date |
|------|---------------|----------|-------------|
| Legacy IIS 7.5 on legacy01 | Vendor MOU until 2026-12 | CISO 2026-05-13 | 2026-09 |

## 6. Stakeholder distribution
CISO, CFO (PCI), Legal (DPA), External auditor (read-only via secure share).
```

---

## Step 6 — The auditor's checklist

Before submission, verify:

- [ ] Every control row has an Evidence ID and the evidence file exists.
- [ ] Every evidence file is hashed and the hash is in MANIFEST.sha256.
- [ ] Open findings have an owner and a due date.
- [ ] Risk acceptances have an executive signoff and a review date.
- [ ] Distribution list is restricted; share via the auditor's secure portal, not email.

---

## Step 7 — Periodic regulatory scans (PCI DSS 11.3.2 — ASV)

PCI DSS specifically requires:

- **Internal** vulnerability scans: quarterly (Lab 12).
- **External** scans by an **Approved Scanning Vendor (ASV)**: quarterly (you cannot self-attest these).
- **Re-scans after significant change**: anytime.

Mark each scan on the calendar with a 7-day buffer for remediation before audit.

---

## What you learned
- Build a crosswalk that prevents duplicate control work across PCI/ISO/CSF/CIS.
- Index evidence per control with a unique ID and a hash.
- Author a quarterly compliance report skeleton.
- Recognise specific PCI DSS scanning obligations (internal vs ASV).
