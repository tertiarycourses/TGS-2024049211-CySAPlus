# Lab 17 — Exploiting and Mitigating XSS and SQL Injection

In this lab you will exploit a reflected XSS, a stored XSS, and a SQL injection on DVWA — then implement the standard mitigations (input validation, output encoding, parameterised queries, prepared statements). This maps to CySA+ 2.4 (Cross-site scripting, Injection flaws) and the **Secure coding best practices** sub-list.

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Start DVWA

```bash
apt update && apt install -y docker.io sqlmap curl
systemctl start docker
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
sleep 10
```

Browse to `http://127.0.0.1:8080`, login `admin / password`, set **DVWA Security = low**, **Setup → Create / Reset Database**.

Capture your session cookie from the browser (DevTools → Application → Cookies). Save it:

```bash
COOKIE="PHPSESSID=<paste yours>; security=low"
```

---

## Step 2 — Reflected XSS (CySA+ "XSS — Reflected")

The DVWA endpoint `vulnerabilities/xss_r/?name=` echoes input straight into HTML.

```bash
curl -s -b "$COOKIE" "http://127.0.0.1:8080/vulnerabilities/xss_r/?name=<script>alert(1)</script>" | grep script
```

You will see your `<script>` tag in the response — the browser would execute it.

**Mitigation (output encoding):** the PHP fix replaces `echo $name` with `echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8')`. View the DVWA **impossible** source to compare.

---

## Step 3 — Stored XSS (CySA+ "XSS — Persistent")

`vulnerabilities/xss_s/` posts a guestbook message that is stored in MySQL and rendered to every visitor.

```bash
curl -s -b "$COOKIE" -d "txtName=mal&mtxMessage=<script>alert('stored')</script>&btnSign=Sign+Guestbook" \
  "http://127.0.0.1:8080/vulnerabilities/xss_s/"
curl -s -b "$COOKIE" "http://127.0.0.1:8080/vulnerabilities/xss_s/" | grep -i "stored"
```

Persistent XSS is graver: every viewer is compromised, not just the original target.

**Mitigation:** server-side **input validation** (allow-list of characters), **output encoding** on render, and a **Content-Security-Policy** header that disallows inline scripts.

---

## Step 4 — SQL Injection — manual

`vulnerabilities/sqli/?id=` builds a SQL query by concatenation. Classic auth-bypass payload:

```bash
curl -s -b "$COOKIE" "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1%27%20OR%20%271%27=%271&Submit=Submit" | grep -E 'First name|Surname'
```

URL-decoded payload: `1' OR '1'='1`. The query becomes `SELECT … WHERE id='1' OR '1'='1'` and returns every row.

---

## Step 5 — SQL Injection — automated with sqlmap

```bash
sqlmap -u "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="$COOKIE" --batch --dbs
```

sqlmap will:
1. Detect the injection point and DB engine.
2. Enumerate databases (you should see `dvwa`).
3. Dump tables on request (`--tables -D dvwa`, then `--dump -T users`).

This is exactly the workflow a red-team or scanner-validation analyst follows after seeing a scanner alert.

---

## Step 6 — Mitigation: parameterised queries

The **only** correct fix for SQLi is parameterised queries / prepared statements. PHP/PDO example DVWA uses on its **impossible** level:

```php
$stmt = $pdo->prepare('SELECT first_name, last_name FROM users WHERE user_id = ?');
$stmt->execute([$id]);
```

Note: input validation (whitelisting integers, etc.) is a useful **defence in depth**, but never the primary fix — it gets bypassed by encoding tricks.

---

## Step 7 — Map the lab to CySA+ 2.4 secure-coding bullets

| Step | Secure coding bullet |
|---|---|
| 2, 3 | Output encoding |
| 3 | Session management (`HttpOnly`, `SameSite` cookies stop XSS-driven session theft) |
| 4–6 | Parameterized queries |
| 6 | Input validation |
| All | Authentication (DVWA login) |
| 3 | Data protection (CSP, `Secure` cookies) |

---

## Step 8 — Tear down

```bash
docker stop dvwa && docker rm dvwa
```

---

## What you learned
- Trigger and recognise reflected XSS, stored XSS, and SQL injection.
- Use `curl` and `sqlmap` to validate scanner findings end-to-end.
- The correct primary mitigation for each class (encoding, validation, parameterisation).
- The link between the OWASP/DVWA exercises and CySA+ 2.4 secure-coding bullets.
