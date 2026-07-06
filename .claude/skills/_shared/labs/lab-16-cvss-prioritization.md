# Lab 16 — CVSS Scoring and Prioritization

In this lab you will score three vulnerabilities with the FIRST CVSS v3.1 calculator, apply environmental context, and produce a prioritised remediation list. This is exam-blueprint CySA+ 2.3 (CVSS interpretation, Context awareness, Asset value, Zero-day).

The work is done in the browser plus a small CSV — no shell required.

---

## Step 1 — Open the CVSS v3.1 calculator

Browser:
**https://www.first.org/cvss/calculator/3.1**

The calculator has three sections:
1. **Base** — intrinsic properties of the vuln
2. **Temporal** — exploit code maturity, remediation level
3. **Environmental** — your context (asset value, mitigations)

---

## Step 2 — Memorise the eight Base metrics

| Metric | Options | What it means |
|---|---|---|
| **AV** Attack Vector | N / A / L / P | Network / Adjacent / Local / Physical |
| **AC** Attack Complexity | L / H | Low / High |
| **PR** Privileges Required | N / L / H | None / Low / High |
| **UI** User Interaction | N / R | None / Required |
| **S** Scope | U / C | Unchanged / Changed |
| **C** Confidentiality | N / L / H | impact |
| **I** Integrity | N / L / H | impact |
| **A** Availability | N / L / H | impact |

These are CySA+ 2.3's bullet points: Attack vectors, Attack complexity, Privileges required, User interaction, Scope, Impact (C/I/A).

---

## Step 3 — Score Vuln #1 — Unauthenticated RCE on a public web server

Settings: `AV:N / AC:L / PR:N / UI:N / S:U / C:H / I:H / A:H`

Base score: **9.8 Critical**

Vector string copied from the calculator:
```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```

---

## Step 4 — Score Vuln #2 — Local privilege escalation on a workstation

Settings: `AV:L / AC:L / PR:L / UI:N / S:U / C:H / I:H / A:H`

Base score: **7.8 High**

---

## Step 5 — Score Vuln #3 — Reflected XSS that requires a click

Settings: `AV:N / AC:L / PR:N / UI:R / S:C / C:L / I:L / A:N`

Base score: **6.1 Medium**

---

## Step 6 — Apply Environmental metrics (context awareness)

CySA+ 2.3 calls out **internal / external / isolated** and **asset value**. The Environmental section lets you push or pull the score:

- Vuln #1 lives on an **internet-facing payment server** → set Confidentiality Requirement = **High** → modified score stays Critical.
- Vuln #2 lives on an **isolated air-gapped lab VM** → Confidentiality Req = **Low**, Modified Attack Vector = **Physical** → score drops to ~4.0.
- Vuln #3 lives on a **public marketing site** with no PII → score effectively low.

The environmental score is the one you use for **prioritization** — never the raw base score.

---

## Step 7 — Build the prioritised list

Save as `/tmp/prio.csv` (open a shell on Killercoda or your laptop):

| Rank | CVE / Vuln | Base | Env | Exploit known? | Asset value | Final priority |
|---|---|---|---|---|---|---|
| 1 | Public RCE | 9.8 | 9.8 | Yes (Exploit-DB) | Critical (revenue) | **Patch within 24 h** |
| 2 | Local privesc | 7.8 | 4.0 | PoC only | Low (air-gapped) | Patch in maintenance window |
| 3 | Reflected XSS | 6.1 | 5.0 | Yes | Medium (brand) | Patch next sprint |

---

## Step 8 — Handle zero-days and exploitability

**Zero-day** = no patch exists yet. CVSS Base still applies but the Temporal score caps you (Remediation Level = **Unavailable**). Mitigations to recommend until a patch ships:
- Compensating control (Lab 24 isolation)
- Virtual patching at WAF / IPS
- Configuration workaround

Confirm exploit maturity on:
- **CISA KEV** — https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **Exploit-DB** — https://www.exploit-db.com
- **EPSS** — https://www.first.org/epss (predicted exploit probability)

---

## Step 9 — Validation (CySA+ 2.3 — true/false positive/negative)

A scanner finding may be:
- **True positive** — vuln exists and is exploitable (Lab 15 `check`)
- **False positive** — version banner matched but patch backported
- **True negative** — correctly silent
- **False negative** — scanner missed it (the worst kind)

Always re-test high-severity findings manually before committing to a patch SLA.

---

## What you learned
- Score a Base CVSS vector for three realistic vulnerabilities.
- Apply environmental context to demote or promote a score.
- Cross-reference exploit databases for weaponisation status.
- Produce a defensible, business-aware remediation priority list.
