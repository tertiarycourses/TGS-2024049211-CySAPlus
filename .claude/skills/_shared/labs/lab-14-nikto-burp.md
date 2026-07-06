# Lab 14 — Web Recon with Nikto and Burp Suite

In this lab you will perform web-server reconnaissance with **Nikto** and intercept/replay requests with **Burp Suite Community**. Together they cover CySA+ 2.2 (Web application scanners — Burp Suite, Nikto) and reinforce 2.4 (Recommended controls).

Run Nikto in the Killercoda playground; run Burp Suite Community on your own laptop.

---

## Step 1 — Install Nikto and start a target

```bash
apt update && apt install -y nikto docker.io
systemctl start docker
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
sleep 10
```

---

## Step 2 — Run a Nikto scan

```bash
nikto -h http://127.0.0.1:8080 -o /tmp/nikto.txt
head -40 /tmp/nikto.txt
```

Typical Nikto findings on DVWA:
- Outdated Apache version (CVE links)
- Backup files left in webroot (`config.bak`)
- Server signature disclosure
- TRACE method enabled (XST risk)
- Default admin interfaces (`/phpmyadmin/`)

---

## Step 3 — Tune Nikto with plugins and tuning options

```bash
nikto -h http://127.0.0.1:8080 -Tuning 4 -Plugins "headers"
nikto -List-plugins | head -20
```

`-Tuning` numbers from the man page:
- 1: Interesting files
- 4: Injection (XSS, etc.)
- 6: Denial of service (use with caution)
- 9: SQL injection

---

## Step 4 — Install Burp Suite Community on your own laptop

Download:
**https://portswigger.net/burp/communitydownload**

(Windows / macOS / Linux). It is a Java GUI — install Java 17+ if missing.

---

## Step 5 — Configure your browser to use Burp's proxy

1. Launch Burp → **Temporary project** → **Use Burp defaults**.
2. **Proxy → Proxy Settings** → confirm listener on `127.0.0.1:8080` (or change to 8081 to avoid clashing with DVWA).
3. In Firefox / Chrome, point HTTP and HTTPS proxy to `127.0.0.1:8081`.
4. Visit `http://burp` and install the Burp CA so HTTPS interception works.

---

## Step 6 — Intercept and modify a request (the killer Burp workflow)

1. **Proxy → Intercept ON**.
2. Browse to DVWA's login page and submit `admin / wrong`.
3. The captured request appears in Burp. **Right-click → Send to Repeater**.
4. In Repeater change the password to `password` and click **Send**.
5. You see the auth response without retyping anything.

This intercept/modify/replay loop is how analysts manually verify XSS, SQLi, IDOR, and CSRF findings flagged by automated scanners.

---

## Step 7 — Send to Intruder for fuzzing (Community is rate-limited but functional)

1. **Right-click a request → Send to Intruder.**
2. Mark a parameter (e.g. the `id` of a product page) as the **payload position**.
3. **Payloads → Simple list** → paste `1, 2, 3, ' OR 1=1--, <script>alert(1)</script>`.
4. **Start attack** — Burp replays each payload and shows length/status differences.

Differences in response length are the classic signal of a successful injection.

---

## Step 8 — Combine Nikto + Burp into a single workflow

| Phase | Tool |
|---|---|
| Quick automated baseline | Nikto |
| Deep crawl + scanner | OWASP ZAP (Lab 13) |
| Manual verification & exploit | Burp Suite Repeater / Intruder |
| Report writeup | Markdown → Lab 26 |

---

## Step 9 — Tear down

```bash
docker stop dvwa && docker rm dvwa
```

---

## What you learned
- Run a Nikto scan and read its prefixed OSVDB/CVE references.
- Install Burp Suite Community and route browser traffic through it.
- Intercept, modify, and replay HTTP requests with Repeater.
- Fuzz a parameter with Intruder and interpret length/status diff.
