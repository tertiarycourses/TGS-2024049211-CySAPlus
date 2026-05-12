# CompTIA CySA+ CS0-003 — Lab Index

All labs run on the free Killercoda Ubuntu Playground:
**https://killercoda.com/playgrounds/scenario/ubuntu**

No installs required on your own machine for the Killercoda labs — every package is pulled with `apt` inside the throw-away VM. The few labs that need software on your **own** PC/laptop (or free web accounts) are flagged with **🖥 Local download** or **🌐 Web account** below.

---

## Domain 1 — Security Operations (33%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 1 | [Log Ingestion and Time Synchronization](lab-01-log-ingestion-time-sync.md) | `rsyslog`, `chrony` (apt) |
| 2 | [OS Hardening and System Process Inspection](lab-02-os-hardening.md) | `lynis`, `auditd` (apt) |
| 3 | [Network Segmentation and Zero Trust](lab-03-segmentation-zero-trust.md) | `iproute2`, `iptables` (apt) |
| 4 | [Detecting Malicious Network Activity](lab-04-malicious-network-activity.md) | `tcpdump`, `nmap` (apt) |
| 5 | [Host-Based IOC Hunting](lab-05-host-ioc-hunting.md) | `auditd`, `psmisc`, `procps` (apt) |
| 6 | [Packet Capture for Threat Hunting](lab-06-packet-capture-threat-hunting.md) | `tcpdump`, `tshark` (apt) |
| 7 | [SIEM Log Correlation](lab-07-siem-log-correlation.md) | `grep`, `awk`, `jq` (apt) |
| 8 | [Email Header Analysis (SPF/DKIM/DMARC)](lab-08-email-header-analysis.md) | `dnsutils` (apt). 🌐 **Web** — MXToolbox |
| 9 | [Malware Triage with Hashing and VirusTotal](lab-09-malware-triage.md) | `coreutils`, `binutils`, `yara` (apt). 🌐 **Web** — VirusTotal |
| 10 | [Threat Intelligence and MITRE ATT&CK](lab-10-threat-intel-mitre.md) | `whois`, `curl` (apt). 🌐 **Web** — AbuseIPDB, ATT&CK Navigator |

## Domain 2 — Vulnerability Management (30%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 11 | [Asset Discovery with Nmap](lab-11-asset-discovery-nmap.md) | `nmap` (apt) |
| 12 | [Vulnerability Scanning with OpenVAS](lab-12-openvas-scanning.md) | 🖥 **Local download** — Greenbone CE VM |
| 13 | [Web App Scanning with OWASP ZAP](lab-13-owasp-zap.md) | `zaproxy` (apt) + DVWA container |
| 14 | [Web Recon with Nikto and Burp Suite](lab-14-nikto-burp.md) | `nikto` (apt). 🖥 **Local** — Burp Suite Community |
| 15 | [Metasploit Framework Basics](lab-15-metasploit-basics.md) | `metasploit-framework` (apt) |
| 16 | [CVSS Scoring and Prioritization](lab-16-cvss-prioritization.md) | 🌐 **Web** — FIRST CVSS Calculator |
| 17 | [Exploiting and Mitigating XSS and SQL Injection](lab-17-xss-sqli.md) | DVWA container, `sqlmap` (apt) |
| 18 | [Patch Management and Hardening](lab-18-patch-hardening.md) | `unattended-upgrades`, `lynis` (apt) |
| 19 | [Attack Surface Reconnaissance](lab-19-attack-surface-recon.md) | `theharvester`, `recon-ng` (apt) |

## Domain 3 — Incident Response and Management (20%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 20 | [Cyber Kill Chain and ATT&CK Mapping](lab-20-kill-chain-mapping.md) | 🌐 **Web** — MITRE ATT&CK Navigator |
| 21 | [Evidence Acquisition and Chain of Custody](lab-21-evidence-chain-of-custody.md) | `coreutils` (`dd`, `sha256sum`) |
| 22 | [Memory Forensics with Volatility](lab-22-memory-forensics.md) | `volatility3` (pip) |
| 23 | [Log Analysis for Incident Response](lab-23-ir-log-analysis.md) | `grep`, `awk`, `journalctl` |
| 24 | [Containment with Host Isolation](lab-24-containment-isolation.md) | `iptables`, `nftables` (apt) |
| 25 | [IR Playbook and Tabletop Exercise](lab-25-ir-playbook-tabletop.md) | none extra |

## Domain 4 — Reporting and Communication (17%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 26 | [Vulnerability Management Report](lab-26-vuln-report.md) | `pandoc` (apt) |
| 27 | [Executive Incident Report](lab-27-executive-incident-report.md) | `pandoc` (apt) |
| 28 | [Security Metrics Dashboard (MTTD/MTTR)](lab-28-metrics-dashboard.md) | `python3`, `matplotlib` (pip) |
| 29 | [Compliance Reporting (PCI DSS / ISO 27001)](lab-29-compliance-reporting.md) | none extra |
| 30 | [Stakeholder Communication and Lessons Learned](lab-30-stakeholder-lessons-learned.md) | none extra |

---

## Labs that require downloading free software onto your **own** machine

Most labs run entirely inside the disposable Killercoda VM. The exceptions:

1. **Lab 12 — OpenVAS** — Greenbone Community Edition VM (https://www.greenbone.net/en/community-edition/) is too heavy for Killercoda. Run in VirtualBox/VMware.
2. **Lab 14 — Burp Suite Community** — https://portswigger.net/burp/communitydownload (Win/Mac/Linux GUI).
3. **Lab 20 — ATT&CK Navigator** — free web app at https://mitre-attack.github.io/attack-navigator/.

---

## Suggested order

Work through Domain 1 → 2 → 3 → 4 in numeric order. Each lab is self-contained; reset the Killercoda playground between labs that change firewall, routing, or install heavy services (OpenVAS, Metasploit) to avoid carry-over.
