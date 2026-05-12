# Lab 23 — Log Analysis for Incident Response

In this lab you will work an incident from a pile of `journalctl` and web-server logs: pivot from one IOC to the next, build a timeline, and produce the "Who, What, When, Where, Why" rows that feed the executive report. This maps to CySA+ 3.2 (Data and log analysis, IoC, Detection and analysis).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Seed a realistic log set

```bash
apt update && apt install -y jq
mkdir -p /tmp/lab23 && cd /tmp/lab23

cat > auth.log <<'EOF'
2026-05-13T08:00:01 host1 sshd[1001]: Failed password for root from 203.0.113.7 port 5001
2026-05-13T08:00:02 host1 sshd[1002]: Failed password for root from 203.0.113.7 port 5002
2026-05-13T08:00:03 host1 sshd[1003]: Failed password for root from 203.0.113.7 port 5003
2026-05-13T08:00:06 host1 sshd[1006]: Accepted password for root from 203.0.113.7 port 5006
2026-05-13T08:00:15 host1 sudo: root : COMMAND=/bin/bash
2026-05-13T08:02:01 host1 sshd[1100]: Accepted publickey for backup from 10.0.0.5 port 22
EOF

cat > web.log <<'EOF'
2026-05-13T08:00:08 203.0.113.7 GET /admin 200 1234
2026-05-13T08:00:09 203.0.113.7 POST /upload.php 200 9876
2026-05-13T08:00:11 203.0.113.7 GET /uploads/shell.php?cmd=id 200 18
2026-05-13T08:01:00 203.0.113.7 GET /uploads/shell.php?cmd=cat+/etc/shadow 200 2456
EOF

cat > netflow.log <<'EOF'
2026-05-13T08:00:08 203.0.113.7 -> 10.0.0.50 :80 1500
2026-05-13T08:00:11 203.0.113.7 -> 10.0.0.50 :80 2200
2026-05-13T08:10:00 10.0.0.50 -> 185.220.101.45 :443 1073741824
EOF
```

---

## Step 2 — Triage with simple greps

```bash
grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr
```

`5  203.0.113.7` flagged — the brute-force source. Same pattern as Lab 7.

---

## Step 3 — Pivot to the first success

```bash
grep "Accepted" auth.log | grep 203.0.113.7
```

`08:00:06 root from 203.0.113.7` — the brute-force succeeded after 5 tries in 5 seconds.

---

## Step 4 — Pivot to the web layer

```bash
grep 203.0.113.7 web.log
```

The same IP uploaded `shell.php` two seconds after login and immediately executed `id` and `cat /etc/shadow`. That confirms a **web shell** (CySA+ "Malicious processes", "Unauthorized software").

---

## Step 5 — Pivot to the data exfil

```bash
grep -E "[0-9]{9,}" netflow.log
```

A 1.07 GB flow from `10.0.0.50` to `185.220.101.45` at 08:10 — the exfiltration. The internal host is now confirmed compromised.

---

## Step 6 — Build the incident timeline

```bash
cat > timeline.md <<'EOF'
| Time (UTC)        | Source           | Event                                   | Evidence              |
|-------------------|------------------|------------------------------------------|------------------------|
| 08:00:01–08:00:05 | 203.0.113.7      | 5 failed root SSH attempts               | auth.log               |
| 08:00:06          | 203.0.113.7      | Accepted password root                   | auth.log               |
| 08:00:08          | 203.0.113.7      | GET /admin → 200                         | web.log                |
| 08:00:09          | 203.0.113.7      | POST /upload.php (web shell drop)        | web.log                |
| 08:00:11          | 203.0.113.7      | GET shell.php?cmd=id (RCE)               | web.log                |
| 08:01:00          | 203.0.113.7      | shell.php?cmd=cat /etc/shadow            | web.log                |
| 08:10:00          | 10.0.0.50 → 185.220.101.45 :443 | 1 GB outbound exfil       | netflow.log            |
EOF
cat timeline.md
```

This table is dropped straight into the executive incident report (Lab 27) under "Timeline".

---

## Step 7 — Use `journalctl` for live systems

On the real host, the same workflow against systemd:

```bash
journalctl _SYSTEMD_UNIT=ssh.service --since "2026-05-13 08:00" --until "2026-05-13 08:15"
journalctl -p err --since "1 hour ago"
journalctl --grep "Failed password|Accepted"
```

`-p err` filters by priority. `--grep` is a regex across all messages — invaluable when you do not know which unit logged the line.

---

## Step 8 — IoC list extracted from the analysis

```bash
cat > iocs.txt <<'EOF'
ip,203.0.113.7,brute-force source
ip,185.220.101.45,exfil destination
file,/var/www/html/uploads/shell.php,web shell
user,root,compromised local account
EOF
```

Feed this list into the Threat Intel pipeline (Lab 10) and the containment script (Lab 24).

---

## What you learned
- Pivot across auth, web, and netflow logs from a single starting IoC.
- Build an incident timeline that maps cleanly to the kill chain.
- Use `journalctl` to do the same on a live systemd host.
- Produce a structured IoC list ready for containment and reporting.
