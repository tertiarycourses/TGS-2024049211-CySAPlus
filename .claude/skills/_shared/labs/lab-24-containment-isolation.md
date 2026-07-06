# Lab 24 — Containment with Host Isolation

In this lab you will isolate a compromised host with `iptables` / `nftables`, apply compensating controls, and verify that the box can still reach the SOC analyst workstation but nothing else. This maps to CySA+ 3.2 (Containment, eradication, and recovery — Scope, Impact, Isolation, Remediation, Re-imaging, Compensating controls).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install tools

```bash
apt update && apt install -y iptables nftables iproute2
```

---

## Step 2 — Snapshot current connectivity (scope of impact)

```bash
ip addr | grep -A1 'state UP'
ss -tunap | head
iptables -S
```

Record what is talking to what — this is the "Scope" and "Impact" assessment.

---

## Step 3 — Define the SOC bastion (your management channel)

```bash
SOC_IP=10.10.0.10      # your analyst workstation / EDR console
SOC_PORTS=22           # leave only the channel you trust
```

Containment that locks **you** out is useless. Always allow your own management path explicitly.

---

## Step 4 — Apply a "network isolation" policy

```bash
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

iptables -A INPUT  -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT  -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT  -s $SOC_IP -p tcp --dport $SOC_PORTS -j ACCEPT
iptables -A OUTPUT -d $SOC_IP -p tcp --sport $SOC_PORTS -j ACCEPT

iptables -S
```

The host is now reachable **only** from the SOC bastion on port 22 — every other connection (including the attacker's C2) is dead.

---

## Step 5 — Save the rules so isolation survives reboot

```bash
apt install -y iptables-persistent
netfilter-persistent save
```

Without this, a reboot during eradication accidentally unisolates the host.

---

## Step 6 — Kill active malicious connections (eradication start)

```bash
# Find the suspect process (Lab 5)
ss -tunap | grep -E ':4444|185.220.101.45' 2>/dev/null

# Then terminate
# pkill -KILL -f shell.php
# kill -9 <PID>
```

Killing connections **before** isolation lets them re-establish; after isolation they cannot.

---

## Step 7 — Apply compensating controls (CySA+ "Compensating controls")

While the team eradicates, mitigate continued risk on neighbouring systems:

- Push an updated **WAF rule** blocking the IOCs.
- Push an updated **EDR / Yara rule** for the dropper hash (Lab 9).
- Add the IOCs to the **threat-intel platform** for everyone else.
- Force a **password reset** for users that were logged into the box.
- Disable the **compromised account** at the IdP (CySA+ "Identification and authentication failures" mitigation).

---

## Step 8 — Re-imaging vs cleanup decision

| Situation | Recommend |
|---|---|
| Kernel rootkit / MBR malware | **Re-image** |
| Unknown extent of compromise | **Re-image** |
| Web shell, single file, known scope | Clean + monitor |
| Admin tier-0 system | **Re-image**, no exceptions |
| Critical legacy system that can't be re-imaged | Compensating controls + segmentation (Lab 3) |

Re-imaging is the only deterministic way to remove unknown unknowns.

---

## Step 9 — Verify isolation worked

```bash
# From the host (Killercoda terminal):
curl --max-time 3 https://example.com || echo "blocked (expected)"
ping -W2 -c1 1.1.1.1 || echo "blocked (expected)"
```

Both should fail. SSH from the SOC bastion should still succeed.

---

## Step 10 — Document containment for the report

```bash
cat > /tmp/containment.md <<EOF
# Containment record — Case 001

| Item | Value |
|------|-------|
| Time isolated (UTC) | $(date -u +%FT%TZ) |
| Method | iptables default-DROP + SOC allowlist |
| Allow-listed source | $SOC_IP:$SOC_PORTS |
| Compensating controls | WAF block, EDR yara push, IdP account disable |
| Re-image decision | Yes — root-level compromise |
| Eradication owner | Platform team |
| Recovery target | $(date -d '+24 hours' -u +%FT%TZ) |
EOF
cat /tmp/containment.md
```

Drop this straight into Lab 27's incident report.

---

## What you learned
- Isolate a host with default-DROP firewall while keeping a management channel.
- Distinguish containment, eradication, and recovery.
- Decide between cleanup and re-imaging.
- Apply compensating controls during the cleanup window.
