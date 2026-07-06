# Lab 13 — Web App Scanning with OWASP ZAP

In this lab you will run **OWASP ZAP** against the deliberately vulnerable **DVWA** to surface XSS, SQLi, and CSRF findings. This is exam-blueprint CySA+ 2.2 (Web application scanners — ZAP, Burp, Arachni, Nikto).

Run inside the Killercoda playground (Docker is available there):
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install ZAP CLI and Docker

```bash
apt update && apt install -y zaproxy docker.io
systemctl start docker
```

---

## Step 2 — Start the DVWA vulnerable target

```bash
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
sleep 10
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/login.php
```

Browse to `http://127.0.0.1:8080` once with credentials `admin / password`, then **Setup → Create / Reset Database**.

---

## Step 3 — Run a ZAP baseline scan (passive, fast)

```bash
zap-baseline.py -t http://127.0.0.1:8080 -r /tmp/zap_baseline.html || true
ls -lh /tmp/zap_baseline.html
```

A baseline scan only **observes** traffic — it will not break the app. Look for:
- **WARN-NEW** rows — newly discovered issues
- Missing security headers (CSP, X-Frame-Options, HSTS)
- Cookies without `Secure`/`HttpOnly`

---

## Step 4 — Run a full active scan

```bash
zap-full-scan.py -t http://127.0.0.1:8080 -r /tmp/zap_full.html || true
```

The full scan actively injects payloads and is what you would run in a staging environment. Open `/tmp/zap_full.html` (download via Killercoda) — you should see DVWA's intentional XSS, SQLi, and command-injection flaws flagged.

---

## Step 5 — Map ZAP alerts to OWASP Top 10

Major ZAP alert classes:

| ZAP alert | OWASP Top 10 | CySA+ 2.4 |
|---|---|---|
| SQL Injection | A03 Injection | Injection flaws |
| Cross-Site Scripting | A03 Injection | XSS (Reflected/Persistent) |
| Path Traversal | A01 Broken Access Control | Directory traversal |
| CSRF | A01 Broken Access Control | Cross-site request forgery |
| Vulnerable JS lib | A06 Vulnerable Components | End-of-life/outdated |
| Server misconfig | A05 Security Misconfig | Security misconfiguration |

---

## Step 6 — Authenticated scan (deep coverage)

ZAP can log in for you and crawl behind auth. From the ZAP **desktop GUI** (or `-z` configs in CLI) you set:
1. A context with the login URL and form fields
2. A user with creds `admin / password`
3. A logged-in / logged-out indicator regex

Authenticated scans typically find 3–5× more issues than anonymous scans.

---

## Step 7 — Save evidence and tear down

```bash
sha256sum /tmp/zap_full.html
docker stop dvwa && docker rm dvwa
```

Always hash report files; they become evidence for the remediation team and auditors.

---

## What you learned
- Run a passive and an active OWASP ZAP scan against DVWA.
- Read ZAP HTML reports and map findings to OWASP Top 10.
- The difference between baseline (safe) and full (intrusive) scans.
- How authenticated scans surface deeper findings.
