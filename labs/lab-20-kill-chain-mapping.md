# Lab 20 — Cyber Kill Chain and ATT&CK Mapping

In this lab you will walk a single intrusion scenario through Lockheed Martin's **Cyber Kill Chain**, then map the same scenario to the **MITRE ATT&CK Navigator** and the **Diamond Model**. This maps to CySA+ 3.1 (Cyber kill chains, Diamond Model of Intrusion Analysis, MITRE ATT&CK, OSSTMM, OWASP Testing Guide).

This lab runs in the browser plus a small markdown file — no shell required.

---

## Step 1 — The scenario

> A finance department user opens an invoice attachment from `alerts@secur1ty-paypal.com` (Lab 8). A macro spawns PowerShell, which downloads a second stage from `185.220.101.45`. The second stage establishes a 60-second heartbeat to the same IP. Over the next 48 hours the attacker dumps credentials with Mimikatz, pivots via SMB to a file server, and exfiltrates 1 GB over HTTPS to a Dropbox-style domain.

---

## Step 2 — Map to the 7 stages of the Lockheed Cyber Kill Chain

| Stage | What happened | IOC / artefact |
|---|---|---|
| 1. Reconnaissance | Attacker harvested LinkedIn finance contacts | OSINT (Lab 19) |
| 2. Weaponisation | Excel macro + downloader built | Hash of `.xlsm` |
| 3. Delivery | Phishing email | From / Return-Path mismatch (Lab 8) |
| 4. Exploitation | Macro runs PowerShell on click | Office → PowerShell parent/child |
| 5. Installation | Second stage persists via scheduled task | New entry in `schtasks` |
| 6. Command & Control | 60 s beacon to 185.220.101.45 | Beaconing pattern (Lab 4) |
| 7. Actions on Objectives | Credential theft + 1 GB exfil | Mimikatz IOCs, traffic spike |

Pick **one stage** as the earliest detection opportunity — that becomes the "earliest kill" recommendation in the incident report (Lab 27).

---

## Step 3 — Open MITRE ATT&CK Navigator

Browser:
**https://mitre-attack.github.io/attack-navigator/**

Click **Create New Layer → Enterprise**.

---

## Step 4 — Tag the techniques used in the scenario

In the search box, find and **select** each of these. For each, click the technique → set **Score = 1** and **Comment = scenario step**:

| ATT&CK ID | Technique | Scenario step |
|---|---|---|
| T1566.001 | Phishing: Spearphishing Attachment | 3. Delivery |
| T1204.002 | User Execution: Malicious File | 4. Exploitation |
| T1059.001 | Command and Scripting Interpreter: PowerShell | 4. Exploitation |
| T1105 | Ingress Tool Transfer | 4–5 |
| T1053.005 | Scheduled Task/Job: Windows | 5. Installation |
| T1071.001 | App Layer Protocol: Web | 6. C2 |
| T1003.001 | OS Credential Dumping: LSASS Memory | 7. Actions |
| T1021.002 | Remote Services: SMB | 7. Lateral Movement |
| T1041 | Exfiltration Over C2 Channel | 7. Exfil |

Use the **Background colour** scale to heat-map the layer. Export with **Download as JSON** or **SVG** and attach to the incident report.

---

## Step 5 — Diamond Model of Intrusion Analysis

Fill in the four corners of the diamond:

```
                  ┌────────────┐
                  │ Adversary  │  TA505-like cluster (TTPs match)
                  └────────────┘
                        △
        ┌───────────────┴────────────────┐
        │                                │
┌───────┴───────┐               ┌────────┴───────┐
│ Capability    │               │ Infrastructure │
│ Macro+PoShell │               │ 185.220.101.45 │
│ Mimikatz      │               │ paypa1-domain   │
└───────────────┘               └────────────────┘
        │                                │
        └───────────────┬────────────────┘
                        ▽
                  ┌────────────┐
                  │   Victim   │  Finance dept, 1 user, file server
                  └────────────┘
```

Each pivot (Adversary, Capability, Infrastructure, Victim) is a query you can run against your SIEM and threat-intel sources.

---

## Step 6 — Compare frameworks

| Framework | Strength | When to use |
|---|---|---|
| Cyber Kill Chain | Simple 7-stage narrative | Exec briefing |
| MITRE ATT&CK | Rich TTP taxonomy with detections | Hunt + detect engineering |
| Diamond Model | Pivots across actor/infra/victim | Threat-intel analysis |
| OWASP Testing Guide | Web app pentest methodology | App-sec engagements |
| OSSTMM | Holistic security testing methodology | Comprehensive audits |

CySA+ expects you to know what each framework is for — pick the right one for the audience.

---

## Step 7 — Save artefacts

```bash
mkdir -p /tmp/lab20
echo "{ /* exported ATT&CK Navigator JSON pasted here */ }" > /tmp/lab20/attack_layer.json
```

These artefacts feed into the incident report deliverable (Lab 27).

---

## What you learned
- Walk a realistic intrusion through the 7-stage Cyber Kill Chain.
- Build an ATT&CK Navigator layer by mapping each scenario step to a technique ID.
- Apply the Diamond Model to enumerate pivot opportunities.
- Choose the right framework for the analytic question at hand.
