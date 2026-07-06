# Lab 12 — Vulnerability Scanning with OpenVAS (Greenbone CE)

In this lab you will run a full credentialed vulnerability scan with **OpenVAS / Greenbone Community Edition**, the free alternative to Nessus and Qualys. This maps directly to CySA+ 2.2 (Vulnerability scanners — Nessus, OpenVAS) and 2.1 (Agent vs agentless, Credentialed vs non-credentialed, Industry frameworks).

> **Heads up:** Greenbone CE downloads a multi-GB feed and runs several services. It is too heavy for Killercoda. Run it on your own laptop in **VirtualBox or VMware** instead.

---

## Step 1 — Download the free Greenbone CE virtual appliance

Browser:
**https://www.greenbone.net/en/community-edition/**

Pick **Greenbone Community Edition (GCE) Virtual Appliance**. Alternative paths:
- Docker compose: https://greenbone.github.io/docs/latest/22.4/container/index.html
- Kali Linux: `sudo apt install gvm` + `sudo gvm-setup`

---

## Step 2 — Boot, set admin password, sign in

Import the OVA into VirtualBox, give it 4 GB RAM and a bridged adapter. On first boot:

1. Set the admin password at the console.
2. Wait for the feed sync to finish (`gvm-check-setup` shows OK).
3. Open `https://<vm-ip>:9392` in your browser — accept the self-signed cert.

---

## Step 3 — Add a target

In the Greenbone Security Assistant web UI:

1. **Configuration → Targets → New Target**
2. Name: `lab-target`
3. Hosts: `192.168.56.0/24` (or a single test IP)
4. Port List: **All IANA assigned TCP**
5. Save.

This is your scope. Always confirm written authorisation before scanning anything you do not own.

---

## Step 4 — (Optional) Add credentials — credentialed scan

1. **Configuration → Credentials → New Credential**
2. Type: **Username + SSH key** (or password)
3. Provide a low-privileged service account on the target.

A credentialed scan can read patch level, kernel version, and config files — finding 5–10× the issues of a network-only scan.

---

## Step 5 — Create and run a scan task

1. **Scans → Tasks → New Task**
2. Name: `lab-scan`
3. Scan target: `lab-target`
4. Scan config: **Full and fast** (or **Full and fast ultimate** for credentialed)
5. SSH/SMB credentials: select the one from Step 4 (if any)
6. Save, then click the green Start arrow.

Scan length depends on host count and scan config — a single VM completes in 10–30 min.

---

## Step 6 — Read the report

When the task says **Done**, click into the report:

- **Severity** bar — High / Medium / Low / Log
- **CVSS** column — base score (Lab 16 covers scoring in depth)
- **Solution** — patch ID, config change, or workaround
- **CVEs** — clickable to NVD

Export as **PDF** or **CSV** for inclusion in your vulnerability report (Lab 26).

---

## Step 7 — Agent vs agentless distinction (CySA+ 2.1)

| | Agentless (what you just did) | Agent-based |
|---|---|---|
| Install on target | No | Yes (Wazuh, OSSEC, vendor) |
| Network coverage | Reachable hosts only | Anywhere agent runs |
| Offline / cloud hosts | Misses them | Catches them |
| Latency to findings | Per scan window | Continuous |

Wazuh (free, Lab 18 references it) provides an agent-based alternative.

---

## Step 8 — Special considerations checklist

Before scheduling production scans, satisfy CySA+ 2.1's six items:

- **Scheduling** — outside business hours
- **Operations** — avoid printers, ICS/SCADA, brittle legacy hosts
- **Performance** — throttle scan threads
- **Sensitivity** — exclude PCI / PHI scopes you cannot legally touch
- **Segmentation** — scan from inside the segment, not through firewalls
- **Regulatory** — PCI DSS Req. 11.2 mandates quarterly external scans

---

## Step 9 — Industry frameworks crosswalk

Greenbone scan policies map to:
- **CIS Benchmarks** (host hardening)
- **PCI DSS** (network scans for cardholder environments)
- **ISO 27001 A.12.6** (technical vulnerability management)
- **OWASP** (web targets)

The right "scan config" depends on which framework you must demonstrate compliance with.

---

## What you learned
- Stand up Greenbone CE / OpenVAS as a free Nessus alternative.
- Create a target, add credentials, run a scan, and read the report.
- The agent-vs-agentless trade-offs.
- How scan configurations align to PCI, CIS, ISO, and OWASP frameworks.
