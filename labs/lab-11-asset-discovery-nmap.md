# Lab 11 — Asset Discovery with Nmap

In this lab you will use Nmap as both an asset-discovery tool and a passive/active fingerprinter. Asset inventory is the first step of every vulnerability management program — you cannot patch what you do not know exists. This maps to CySA+ 2.1 (Asset discovery — Map scans, Device fingerprinting; Internal vs external scanning; Active vs passive).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install Nmap

```bash
apt update && apt install -y nmap
```

---

## Step 2 — Host discovery (a "map scan")

A map scan answers "what is alive on this subnet?" without a port scan.

```bash
nmap -sn 127.0.0.0/29
nmap -sn -PE -PS22,80,443 scanme.nmap.org
```

- `-sn` — no port scan, ping sweep only
- `-PE` — ICMP echo
- `-PS22,80,443` — TCP SYN ping on those ports (useful when ICMP is blocked)

---

## Step 3 — Internal vs external scanning

Run the same scan against:

- **Internal**: `127.0.0.1` (anything in your private space)
- **External**: `scanme.nmap.org` (a host the Nmap project lets you probe)

Notice the difference: internal scans see open management ports (22, 5985, 3389), external scans usually see only web/edge services. CySA+ tests you on this distinction — vulnerability scope is very different for each.

---

## Step 4 — Active service / version detection (fingerprinting)

```bash
nmap -sV -Pn -T4 scanme.nmap.org -p 22,80,443
```

`-sV` probes each open port to identify the service banner. The output identifies SSH version, web server, etc. — feeding the CVE matching step later.

---

## Step 5 — OS fingerprinting (active)

```bash
nmap -O -Pn scanme.nmap.org
```

`-O` sends crafted probes and matches TCP/IP stack quirks against its OS database. Note: requires root inside the VM (Killercoda gives root).

---

## Step 6 — Passive fingerprinting (alternative)

Active scans are noisy and can trip IDS rules. Passive fingerprinting sniffs existing traffic instead:

```bash
apt install -y p0f tcpdump
p0f -i any -o /tmp/p0f.log &
curl -s https://example.com > /dev/null
sleep 2
kill %1
grep -m5 . /tmp/p0f.log
```

`p0f` infers the remote OS from TCP options without sending a packet — exam-blueprint **passive** scanning.

---

## Step 7 — Credentialed vs non-credentialed (concept)

Nmap is non-credentialed. To get a credentialed view you would use:
- `nmap --script ssh-auth-methods` (limited)
- A scanner like **OpenVAS** or **Nessus** with SSH/SMB credentials (see Lab 12)

Credentialed scans find missing patches, weak configs, and local CVEs invisible to network probes. Non-credentialed scans see only what an attacker on the wire would see.

---

## Step 8 — Output formats for the inventory pipeline

```bash
nmap -sV -Pn scanme.nmap.org -p 80,443 -oA /tmp/scan_inventory
ls /tmp/scan_inventory.*
```

`-oA` saves three formats simultaneously:
- `.nmap` — human-readable
- `.gnmap` — grep-friendly
- `.xml` — machine-readable for SIEM / CMDB ingestion

Parse the XML:

```bash
apt install -y libxml2-utils
xmllint --xpath '//host/address/@addr | //port/service/@product' /tmp/scan_inventory.xml | head
```

---

## Step 9 — Schedule a recurring scan (Special considerations)

CySA+ 2.1 lists "Scheduling, Operations, Performance, Sensitivity, Segmentation, Regulatory" as scan considerations. A simple cron entry:

```bash
echo "0 2 * * * root nmap -sn 10.0.0.0/24 -oG /var/log/asset-inventory-\$(date +\\%F).gnmap" > /etc/cron.d/asset_inventory
cat /etc/cron.d/asset_inventory
```

Scan at 02:00 — outside business hours to respect **operations** and **performance**.

---

## What you learned
- Run a ping-sweep map scan and version/OS fingerprint with Nmap.
- The difference between active (Nmap) and passive (p0f) fingerprinting.
- Internal vs external scan scope.
- How to output Nmap data for pipeline consumption and schedule it.
