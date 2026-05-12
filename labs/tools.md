# Free Tools Reference — CompTIA CySA+ CS0-003 Labs

Every tool listed here is **100% free** (open-source, freeware, or free tier with no time limit).

Three categories:

1. **Inside Killercoda** — installed in the disposable Ubuntu VM via `apt` or `pip`. Nothing touches your own machine.
2. **External / Standalone** — downloaded onto your own PC/laptop, or used in a browser.
3. **Free web services** — sign up for free, no payment required.

Killercoda playground (free, no signup): https://killercoda.com/playgrounds/scenario/ubuntu

---

## Section A — Tools installed inside the Killercoda Ubuntu VM

### A1. Log ingestion, time sync, audit (Lab 1, 2, 5, 23)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `rsyslog` | pre-installed | Syslog daemon, central log collector | 1, 23 |
| `chrony` | `apt install chrony` | NTP / time sync | 1 |
| `auditd` | `apt install auditd` | Linux audit framework | 2, 5 |
| `lynis` | `apt install lynis` | System hardening scanner | 2, 18 |
| `journalctl` | pre-installed (systemd) | Query systemd journal | 5, 23 |

### A2. Packet capture & network analysis (Lab 4, 6)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `tcpdump` | `apt install tcpdump` | CLI packet capture | 4, 6 |
| `tshark` | `apt install tshark` | CLI Wireshark | 6 |
| `nmap` | `apt install nmap` | Port scanner, host discovery | 4, 11 |
| `iproute2` (`ip`, `ss`) | pre-installed | Sockets, routing, namespaces | 3, 4, 24 |

### A3. Network segmentation & containment (Lab 3, 24)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `iptables` | pre-installed | Stateful firewall | 3, 24 |
| `nftables` | `apt install nftables` | Modern firewall | 24 |
| `ip netns` (in iproute2) | pre-installed | Network namespaces (segmentation lab) | 3 |

### A4. Malware triage & file analysis (Lab 9)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `sha256sum`, `md5sum` | pre-installed (coreutils) | File hashing | 9, 21 |
| `strings` | `apt install binutils` | Extract ASCII strings from binaries | 9 |
| `file` | pre-installed | Magic-byte file type detection | 9 |
| `yara` | `apt install yara` | Pattern-based malware rules | 9 |

### A5. Threat intel / OSINT (Lab 10, 19)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `whois` | `apt install whois` | Domain/IP registration lookup | 10 |
| `curl` / `jq` | `apt install curl jq` | REST API queries (AbuseIPDB) | 10 |
| `dnsutils` (`dig`) | `apt install dnsutils` | DNS record lookup (SPF/DKIM/DMARC) | 8 |
| `theharvester` | `apt install theharvester` | Email / subdomain OSINT | 19 |
| `recon-ng` | `apt install recon-ng` | Modular OSINT framework | 19 |

### A6. Vulnerability assessment (Lab 13, 14, 15, 17)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `zaproxy` | `apt install zaproxy` | OWASP ZAP web app scanner | 13 |
| `nikto` | `apt install nikto` | Web server scanner | 14 |
| `sqlmap` | `apt install sqlmap` | SQL injection automation | 17 |
| `metasploit-framework` | `apt install metasploit-framework` | Exploit framework | 15 |

### A7. Forensics (Lab 21, 22)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `dd` | pre-installed | Bit-for-bit disk/memory copy | 21 |
| `volatility3` | `pip install volatility3` | Memory image analysis | 22 |
| `binwalk` | `apt install binwalk` | Embedded-file carver | 22 |

### A8. Patch & config management (Lab 18)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `unattended-upgrades` | `apt install unattended-upgrades` | Automatic security patching | 18 |
| `debsecan` | `apt install debsecan` | List unpatched CVEs on Debian/Ubuntu | 18 |

### A9. Reporting (Lab 26, 27, 28)
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| `pandoc` | `apt install pandoc` | Markdown → PDF/HTML report converter | 26, 27 |
| `python3` + `matplotlib` | `pip install matplotlib` | KPI dashboards / charts | 28 |

---

## Section B — External / Standalone Free Tools (download onto your own machine)

### B1. SIEM / log analysis platforms
| Tool | Type | Link |
|------|------|------|
| Splunk Free | Free 500 MB/day | https://www.splunk.com/en_us/download/splunk-enterprise.html |
| Elastic Stack (ELK) | Self-hosted | https://www.elastic.co/elastic-stack |
| Graylog Open | Self-hosted | https://graylog.org/products/source-available |
| Wazuh | XDR/SIEM open-source | https://wazuh.com |
| Security Onion | Free SOC distro | https://securityonionsolutions.com |

### B2. Vulnerability scanners
| Tool | Type | Link |
|------|------|------|
| Greenbone Community Edition (OpenVAS) | Free VM | https://www.greenbone.net/en/community-edition/ |
| Nessus Essentials | Free for 16 IPs | https://www.tenable.com/products/nessus/nessus-essentials |
| OpenSCAP | Compliance scanner | https://www.open-scap.org |

### B3. Web application testing
| Tool | Type | Link |
|------|------|------|
| Burp Suite Community | Free GUI Win/Mac/Linux | https://portswigger.net/burp/communitydownload |
| OWASP ZAP | Free GUI Win/Mac/Linux | https://www.zaproxy.org |
| DVWA (Damn Vulnerable Web App) | Practice target | https://github.com/digininja/DVWA |
| OWASP Juice Shop | Practice target | https://owasp.org/www-project-juice-shop |
| WebGoat | OWASP training app | https://owasp.org/www-project-webgoat |

### B4. Penetration testing distros
| Tool | Type | Link |
|------|------|------|
| Kali Linux | Free VM/ISO | https://www.kali.org |
| Parrot Security OS | Free VM/ISO | https://www.parrotsec.org |
| Metasploitable 2/3 | Vulnerable VM | https://github.com/rapid7/metasploitable3 |
| Commando VM | Windows pentest distro | https://github.com/mandiant/commando-vm |

### B5. Packet capture / forensics
| Tool | Type | Link |
|------|------|------|
| Wireshark | GUI Win/Mac/Linux | https://www.wireshark.org |
| NetworkMiner Free | Win/Mono | https://www.netresec.com/?page=NetworkMiner |
| Autopsy | Disk forensics GUI | https://www.autopsy.com |
| FTK Imager Free | Disk imaging | https://www.exterro.com/ftk-imager |
| Volatility 3 | Memory forensics | https://volatilityfoundation.org |
| CyberChef | Browser-based decoder/encoder | https://gchq.github.io/CyberChef |

### B6. Malware sandboxes (local)
| Tool | Type | Link |
|------|------|------|
| Cuckoo Sandbox | Self-hosted | https://cuckoosandbox.org |
| REMnux | Reverse-engineering distro | https://remnux.org |
| FLARE-VM | Windows analysis distro | https://github.com/mandiant/flare-vm |

### B7. Endpoint / EDR (free tier)
| Tool | Type | Link |
|------|------|------|
| OSSEC | Open-source HIDS | https://www.ossec.net |
| Wazuh agent | EDR | https://wazuh.com |
| Sysmon (Windows) | Event tracing | https://learn.microsoft.com/sysinternals/downloads/sysmon |
| osquery | SQL endpoint queries | https://osquery.io |
| Velociraptor | DFIR endpoint tool | https://docs.velociraptor.app |

### B8. Firewalls / IDS / IPS
| Tool | Type | Link |
|------|------|------|
| pfSense CE | Free firewall distro | https://www.pfsense.org |
| OPNsense | Free firewall distro | https://opnsense.org |
| Suricata | Open-source IDS/IPS | https://suricata.io |
| Snort 3 | Open-source IDS | https://www.snort.org |
| Zeek (Bro) | Network security monitor | https://zeek.org |

---

## Section C — Free Web Services

### C1. Threat intelligence
| Service | Purpose | Link |
|---------|---------|------|
| VirusTotal | Multi-AV hash/file/URL scan | https://www.virustotal.com |
| AbuseIPDB | IP reputation, abuse reports | https://www.abuseipdb.com |
| URLhaus | Malicious URL database | https://urlhaus.abuse.ch |
| MalwareBazaar | Malware sample sharing | https://bazaar.abuse.ch |
| AlienVault OTX | Threat exchange | https://otx.alienvault.com |
| Shodan (free tier) | Internet device search | https://www.shodan.io |
| Censys (free tier) | Internet scan data | https://search.censys.io |
| ThreatFox | IOC feed | https://threatfox.abuse.ch |

### C2. Email security / OSINT
| Service | Purpose | Link |
|---------|---------|------|
| MXToolbox | DNS / SPF / DKIM / DMARC / blacklist | https://mxtoolbox.com |
| Google Admin Toolbox — Messageheader | Email header parser | https://toolbox.googleapps.com/apps/messageheader |
| Have I Been Pwned | Breach lookup | https://haveibeenpwned.com |
| DNSDumpster | Subdomain recon | https://dnsdumpster.com |
| crt.sh | Certificate transparency search | https://crt.sh |

### C3. Vulnerability data & CVSS
| Service | Purpose | Link |
|---------|---------|------|
| NVD (NIST) | CVE database | https://nvd.nist.gov |
| MITRE CVE | Authoritative CVE list | https://cve.mitre.org |
| FIRST CVSS v3.1 Calculator | Score CVEs | https://www.first.org/cvss/calculator/3.1 |
| Exploit-DB | Public exploits | https://www.exploit-db.com |
| CISA KEV Catalog | Known exploited vulns | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |

### C4. Adversary frameworks
| Service | Purpose | Link |
|---------|---------|------|
| MITRE ATT&CK | TTP knowledge base | https://attack.mitre.org |
| MITRE ATT&CK Navigator | Layer/heatmap tool | https://mitre-attack.github.io/attack-navigator/ |
| MITRE D3FEND | Defensive countermeasures | https://d3fend.mitre.org |
| Lockheed Cyber Kill Chain | Methodology | https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html |
| OWASP Top 10 | Web app risks | https://owasp.org/Top10 |

### C5. Sandboxes (online malware)
| Service | Purpose | Link |
|---------|---------|------|
| Any.Run (free) | Interactive sandbox | https://any.run |
| Hybrid Analysis | Free sandbox | https://www.hybrid-analysis.com |
| Joe Sandbox Cloud Basic | Free tier | https://www.joesandbox.com |
| Triage (Hatching) | Free tier | https://tria.ge |

### C6. Compliance / framework references
| Service | Purpose | Link |
|---------|---------|------|
| CIS Benchmarks | Hardening guides | https://www.cisecurity.org/cis-benchmarks |
| NIST CSF | Framework reference | https://www.nist.gov/cyberframework |
| PCI DSS Library | Standard docs | https://www.pcisecuritystandards.org |
| ISO 27001 (overview) | ISMS standard | https://www.iso.org/isoiec-27001-information-security.html |
| OWASP Testing Guide | Web app test methodology | https://owasp.org/www-project-web-security-testing-guide |
| OSSTMM | Security testing methodology | https://www.isecom.org/OSSTMM.3.pdf |

---

## Lab → Primary Tool Quick Map

| Lab | Headline tool(s) |
|-----|------------------|
| 1 | rsyslog, chrony |
| 2 | lynis, auditd |
| 3 | ip netns, iptables |
| 4 | tcpdump, nmap |
| 5 | auditd, ps, journalctl |
| 6 | tcpdump, tshark |
| 7 | grep, awk, jq |
| 8 | dig, MXToolbox |
| 9 | sha256sum, strings, yara, VirusTotal |
| 10 | whois, AbuseIPDB, ATT&CK Navigator |
| 11 | nmap |
| 12 | Greenbone CE / OpenVAS |
| 13 | OWASP ZAP, DVWA |
| 14 | Nikto, Burp Suite Community |
| 15 | metasploit-framework |
| 16 | FIRST CVSS Calculator |
| 17 | sqlmap, DVWA |
| 18 | unattended-upgrades, debsecan, lynis |
| 19 | theHarvester, recon-ng |
| 20 | MITRE ATT&CK Navigator |
| 21 | dd, sha256sum |
| 22 | Volatility 3 |
| 23 | journalctl, grep |
| 24 | iptables / nftables |
| 25 | tabletop scenario |
| 26 | pandoc |
| 27 | pandoc |
| 28 | python3, matplotlib |
| 29 | CIS / PCI / ISO references |
| 30 | post-incident template |

---

All tools above are free of charge. The Killercoda VM is also free and disposable, so you can run most labs without spending or installing anything on your own machine — except the optional GUI tools in Section B and the free web services in Section C.
