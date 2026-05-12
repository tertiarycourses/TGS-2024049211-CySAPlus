# Lab 7 — SIEM Log Correlation

In this lab you will play the role of a SIEM: ingesting raw logs from multiple sources, normalising them, and correlating fields to detect a brute-force-then-success login pattern. You will use the universal Unix data-pipeline trio — `grep`, `awk`, `jq` — which is enough to prototype any SOAR / SIEM rule before deploying it to Splunk or Elastic. (CySA+ 1.3 — SIEM, SOAR, Log analysis/correlation.)

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install tools and seed sample logs

```bash
apt update && apt install -y jq
mkdir -p /tmp/lab7 && cd /tmp/lab7

cat > auth.log <<'EOF'
2026-05-13T08:00:01 host1 sshd[1001]: Failed password for root from 203.0.113.7 port 5001 ssh2
2026-05-13T08:00:02 host1 sshd[1002]: Failed password for root from 203.0.113.7 port 5002 ssh2
2026-05-13T08:00:03 host1 sshd[1003]: Failed password for root from 203.0.113.7 port 5003 ssh2
2026-05-13T08:00:04 host1 sshd[1004]: Failed password for root from 203.0.113.7 port 5004 ssh2
2026-05-13T08:00:05 host1 sshd[1005]: Failed password for root from 203.0.113.7 port 5005 ssh2
2026-05-13T08:00:06 host1 sshd[1006]: Accepted password for root from 203.0.113.7 port 5006 ssh2
2026-05-13T08:00:30 host1 sshd[1010]: Failed password for alice from 198.51.100.4 port 6001 ssh2
EOF

cat > web.log <<'EOF'
2026-05-13T08:00:07 203.0.113.7 GET /admin 200
2026-05-13T08:00:08 203.0.113.7 POST /upload.php 200
2026-05-13T08:01:00 198.51.100.4 GET / 200
EOF
```

---

## Step 2 — Extract structured fields with awk (parsing)

```bash
awk '/Failed password/ {print $1, $(NF-3)}' auth.log
```

Output: timestamp + source IP. This is the **parsing** layer of any SIEM — turning unstructured text into fields.

---

## Step 3 — Count failures per IP (aggregation)

```bash
grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr
```

This is the core SIEM aggregation: `5  203.0.113.7`, `1  198.51.100.4`. Anything above your threshold (e.g. 5 in 60 s) becomes a candidate alert.

---

## Step 4 — Correlate failed brute-force with successful login (rule logic)

```bash
bad_ip=$(grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | awk '$1>=5{print $2}')
echo "Suspect IP: $bad_ip"
grep "Accepted" auth.log | grep "$bad_ip"
```

If the same IP that produced ≥ 5 failures ever produces an `Accepted` — that is a confirmed credential-stuffing success. This is exactly how Splunk/Elastic correlation rules work.

---

## Step 5 — Pivot to a second data source (web logs)

```bash
grep "$bad_ip" web.log
```

We now know the attacker authenticated and immediately hit `/admin` and uploaded a file — likely a web shell.

---

## Step 6 — Work with structured JSON logs (jq)

Suricata, Zeek, AWS CloudTrail, and most modern tools emit JSON. Try `jq`:

```bash
cat > events.json <<'EOF'
{"ts":"2026-05-13T08:00:01","src":"203.0.113.7","event":"ssh_fail","user":"root"}
{"ts":"2026-05-13T08:00:06","src":"203.0.113.7","event":"ssh_success","user":"root"}
{"ts":"2026-05-13T08:00:30","src":"198.51.100.4","event":"ssh_fail","user":"alice"}
EOF

jq -r 'select(.event=="ssh_fail") | .src' events.json | sort | uniq -c
jq -r 'select(.event=="ssh_success") | "\(.ts) \(.src) \(.user)"' events.json
```

---

## Step 7 — Build a one-line "detection rule"

```bash
join -1 1 -2 1 \
  <(jq -r 'select(.event=="ssh_fail") | .src' events.json | sort -u) \
  <(jq -r 'select(.event=="ssh_success") | .src' events.json | sort -u)
```

Any IP printed is on **both** sides — failed AND succeeded. That is a brute-force-success in one shell line.

---

## What you learned
- Parse, aggregate, and correlate logs across multiple sources.
- Build a brute-force-then-success detection by hand — the algorithm under every SIEM "use case".
- Work with both unstructured syslog and structured JSON events.
- Move from raw log to actionable alert without leaving the shell.
