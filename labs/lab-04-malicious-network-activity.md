# Lab 4 — Detecting Malicious Network Activity

In this lab you will generate and detect several network-based indicators of compromise: port scans, beaconing, unusual traffic spikes, and activity on unexpected ports. These are exam-blueprint items under CySA+ 1.2 (Network-related indicators of malicious activity).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install tools

```bash
apt update && apt install -y tcpdump nmap netcat-openbsd curl
```

---

## Step 2 — Detect a port scan (scans/sweeps)

In terminal 1, start a capture:

```bash
tcpdump -i any -nn 'tcp[tcpflags] & (tcp-syn) != 0 and not tcp[tcpflags] & tcp-ack != 0' -c 30 &
```

This BPF filter shows only SYN packets without ACK — the signature of a TCP connect or SYN scan.

In the same terminal, run an Nmap scan against localhost:

```bash
nmap -sS -p 1-1000 127.0.0.1
```

You will see dozens of SYN attempts in the capture — the smoking gun of a scan.

---

## Step 3 — Detect beaconing (regular C2 callbacks)

Beaconing is malware checking in with its command-and-control server on a regular cadence. Simulate it:

```bash
for i in {1..6}; do curl -s -o /dev/null http://example.com; sleep 5; done &
```

Capture every connection to port 80 and time-stamp it:

```bash
tcpdump -i any -nn -ttt 'tcp port 80 and tcp[tcpflags] & tcp-syn != 0' -c 6
```

`-ttt` prints the delta between packets. A perfectly periodic interval (every 5.000 s here) is the classic beaconing pattern. Real C2 jitters the interval, but the average is still detectable.

---

## Step 4 — Detect activity on an unexpected port

Spawn a listener on an unusual port:

```bash
nc -l -p 31337 &
nc -zv 127.0.0.1 31337
```

Find it from a baseline-deviation viewpoint:

```bash
ss -tulnp | grep -vE ':(22|53|80|443|123)\s'
```

Anything not on a sanctioned port is a candidate for investigation. Port 31337 is a well-known "elite" attacker port and the canonical example of "activity on unexpected ports".

---

## Step 5 — Detect a traffic spike (bandwidth consumption)

Generate a burst of traffic:

```bash
for i in {1..100}; do curl -s -o /dev/null http://example.com & done; wait
```

Measure per-interface bytes:

```bash
cat /proc/net/dev | column -t
```

In production a NetFlow collector or `iftop`/`nethogs` reveals top talkers; a sudden 10× jump on one host is a data-exfiltration red flag.

---

## Step 6 — Detect irregular peer-to-peer / rogue device patterns

ARP sweeps reveal rogue devices and lateral-movement reconnaissance:

```bash
ip neigh
arp -n 2>/dev/null
```

Repeated ARP queries for the entire /24 from one source is a host enumeration attempt.

---

## Step 7 — Clean up background jobs

```bash
kill %1 %2 2>/dev/null; jobs
```

---

## What you learned
- BPF filters for SYN-only packets → detecting scans.
- Using `tcpdump -ttt` to spot **beaconing** intervals.
- Identifying activity on **unexpected ports** with `ss`.
- Recognising **bandwidth spikes** and ARP-based **rogue device** indicators.
