# Lab 10 — Threat Intelligence and MITRE ATT&CK

In this lab you will enrich a suspicious IP with `whois`, AbuseIPDB, and Shodan, then map an observed behaviour to a MITRE ATT&CK technique using the free Navigator. You will also script a tiny SOAR-style automation. This covers CySA+ 1.4 (Threat actors, TTP, Collection methods, Threat-intelligence sharing, Active defense) and 1.5 (SOAR, automation, API).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install tools

```bash
apt update && apt install -y whois curl jq
```

---

## Step 2 — WHOIS lookup (Collection methods — Open source)

```bash
whois 8.8.8.8 | grep -Ei 'orgname|country|netrange|cidr'
whois example.com | grep -Ei 'registrar|country|creation|expir'
```

Things to look for in incident triage:
- Recently registered domain (`Creation Date` < 7 days) is highly suspicious.
- Bullet-proof / privacy-protected registrar.
- Country mismatch versus the user base.

---

## Step 3 — AbuseIPDB API enrichment

AbuseIPDB gives an abuse-confidence score 0–100 for any IP. Sign up free at https://www.abuseipdb.com/account/api — paste your key when prompted, or skip with a dry-run:

```bash
read -p "AbuseIPDB API key (or press Enter to skip): " ABUSE_KEY
if [ -n "$ABUSE_KEY" ]; then
  curl -s -G https://api.abuseipdb.com/api/v2/check \
    --data-urlencode "ipAddress=185.220.101.45" \
    -H "Key: $ABUSE_KEY" -H "Accept: application/json" | jq
fi
```

`abuseConfidenceScore` ≥ 75 is the classic "block now" threshold. `usageType=hosting` + high score is a typical scanner/C2.

---

## Step 4 — Build a small enrichment script (SOAR primitive)

```bash
cat > /tmp/enrich.sh <<'EOF'
#!/bin/sh
IP="$1"
echo "=== Enrichment for $IP ==="
echo "[whois country]"; whois "$IP" 2>/dev/null | grep -i country | head -1
echo "[reverse DNS]";   dig +short -x "$IP" || echo "(none)"
echo "[port:80 HTTP banner]"
curl -m 5 -s -o /dev/null -w "%{http_code} %{remote_ip}\n" "http://$IP" 2>/dev/null
EOF
chmod +x /tmp/enrich.sh
/tmp/enrich.sh 8.8.8.8
```

This is a SOAR playbook in miniature: one IOC in, multiple sources queried, structured output ready to feed a ticket.

---

## Step 5 — Map a behaviour to MITRE ATT&CK

Open the **MITRE ATT&CK Navigator** in your browser:
**https://mitre-attack.github.io/attack-navigator/**

Suppose your SIEM detected: *"PowerShell downloaded a remote script and ran it in memory."*

1. In the search box type `Ingress Tool Transfer` → technique **T1105**.
2. Type `PowerShell` → technique **T1059.001** (Command and Scripting Interpreter: PowerShell).
3. Type `Process Injection` → technique **T1055**.

Each technique page lists:
- Detection guidance
- Mitigations
- Procedure examples (Real APT groups that use it — e.g. APT29)
- Data sources to monitor

This is your threat-hunting hypothesis library.

---

## Step 6 — Recognise threat-actor categories (CySA+ 1.4 vocab)

| Category | Motivation | Example artefact |
|---|---|---|
| APT (nation-state) | Espionage, long-dwell | Custom tooling, supply-chain compromise |
| Organised crime | Money | Ransomware, banking trojans |
| Hacktivist | Ideology | Defacements, doxing |
| Script kiddie | Notoriety | Off-the-shelf tools, loud scanning |
| Insider | Various | Bulk data access, after-hours login |
| Supply chain | Indirect | Trojanised dependency |

Match an IOC to the most likely actor before you decide containment urgency.

---

## Step 7 — Threat-intelligence sharing formats

```bash
echo "203.0.113.99,malicious,c2,2026-05-13" >> /tmp/iocs.csv
echo '{"indicator":"203.0.113.99","type":"ipv4-addr","tlp":"amber"}' | jq
```

Real-world feeds use **STIX/TAXII**; the indicators travel between CERT, CSIRT, ISACs, and commercial paid feeds. Free public sources:
- abuse.ch (URLhaus, MalwareBazaar, ThreatFox)
- AlienVault OTX
- Spamhaus DROP list
- CISA AIS

---

## Step 8 — Active defense and honeypots

The defensive end of threat intelligence is **deception**. Spin up a quick fake SSH listener:

```bash
apt install -y netcat-openbsd
nc -lk -p 2222 -e /bin/false &
ss -ltnp | grep 2222
kill %1
```

A real honeypot (e.g. Cowrie) logs every credential the attacker types — feeding back into your IOC pipeline.

---

## What you learned
- Enrich an IP with WHOIS, AbuseIPDB, and reverse DNS.
- Build a one-shot SOAR enrichment script.
- Map observed behaviour to MITRE ATT&CK techniques.
- Categorise threat actors and recognise the major sharing feeds and formats.
