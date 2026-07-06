# Lab 8 — Email Header Analysis (SPF/DKIM/DMARC)

In this lab you will analyse an email header for impersonation indicators and inspect the three authentication standards — SPF, DKIM, and DMARC — that determine whether a sender is forging the From address. These are exam-blueprint items under CySA+ 1.3 (Email analysis — Header, Impersonation, DKIM, DMARC, SPF, Embedded links).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install DNS tools

```bash
apt update && apt install -y dnsutils
```

---

## Step 2 — Look up an SPF record

SPF lists the IPs/hosts allowed to send mail for a domain. It is a DNS TXT record starting with `v=spf1`.

```bash
dig +short TXT google.com | grep spf1
dig +short TXT microsoft.com | grep spf1
```

Read a record like `v=spf1 include:_spf.google.com ~all`:
- `include:` — another SPF record to inherit
- `~all` — softfail anything else
- `-all` — hard reject anything else (stronger)

---

## Step 3 — Look up DKIM and DMARC

DKIM signatures live at a selector subdomain (e.g. `s1._domainkey.example.com`). DMARC policy lives at `_dmarc.example.com`:

```bash
dig +short TXT _dmarc.google.com
dig +short TXT _dmarc.paypal.com
```

Read a DMARC record like `v=DMARC1; p=reject; rua=mailto:...`:
- `p=none` — monitor only
- `p=quarantine` — junk folder
- `p=reject` — bounce the mail (strongest)

---

## Step 4 — Analyse a suspicious raw header

Save the following spear-phishing-style header:

```bash
cat > /tmp/header.eml <<'EOF'
Return-Path: <alerts@secur1ty-paypal.com>
Received: from mta-bad.example (mta-bad.example [203.0.113.99])
        by mx.gmail.com with ESMTPS
        Mon, 13 May 2026 08:00:00 +0000
Received: from desktop-pc (unknown [10.0.0.99])
        by mta-bad.example
        Mon, 13 May 2026 07:59:50 +0000
From: "PayPal Security" <service@paypal.com>
Reply-To: refund-team@secur1ty-paypal.com
To: victim@example.org
Subject: Urgent: Confirm your account
Authentication-Results: mx.gmail.com;
  spf=fail (sender IP is 203.0.113.99) smtp.mailfrom=secur1ty-paypal.com;
  dkim=none header.i=@paypal.com;
  dmarc=fail (p=REJECT sp=REJECT dis=NONE) header.from=paypal.com
EOF
```

Spot the indicators (CySA+ "Impersonation"):

```bash
grep -E '^(From|Return-Path|Reply-To|Received|Authentication-Results)' /tmp/header.eml
```

Red flags:
- **From** = `paypal.com` but **Return-Path** = `secur1ty-paypal.com` (homograph / lookalike).
- **Reply-To** points to the attacker domain, not the brand.
- **Received** chain starts at `desktop-pc` 10.0.0.99 — not a corporate MTA.
- **Authentication-Results** = `spf=fail`, `dkim=none`, `dmarc=fail`.

Each row in `Authentication-Results` is a separate verdict; all three failing is a confirmed forgery.

---

## Step 5 — Trace the `Received` chain to find the true origin

`Received` headers are stacked top-down; the **lowest** one is the original. Print them in order:

```bash
tac /tmp/header.eml | grep -E '^Received'
```

The earliest hop `desktop-pc [10.0.0.99]` is the actual sender — a residential PC, not PayPal infrastructure.

---

## Step 6 — Check embedded links (CySA+ "Obfuscated links")

Phish emails hide the real destination behind plausible link text. Pull every URL:

```bash
cat > /tmp/body.txt <<'EOF'
Click here to verify: https://paypa1.com.secur1ty-paypal.com/login?u=victim
Or: <a href="http://203.0.113.42/p">https://www.paypal.com</a>
EOF

grep -Eoi 'https?://[^"<>[:space:]]+' /tmp/body.txt
```

Inspect for:
- Lookalike domains (`paypa1` with a "1" instead of an "l")
- Anchor-text vs href mismatch (the second link **says** paypal.com but points to a raw IP)
- Punycode (`xn--...`) — paste suspicious URLs into a punycode decoder

---

## Step 7 — Validate against a public service

For real triage, paste the full header into:
- **MXToolbox Header Analyzer** — https://mxtoolbox.com/EmailHeaders.aspx
- **Google Messageheader** — https://toolbox.googleapps.com/apps/messageheader/

Both will visualise the hop chain and parse the SPF/DKIM/DMARC results in seconds.

---

## What you learned
- How to query SPF, DKIM, and DMARC records with `dig`.
- How to read the `Authentication-Results` header to confirm forgery.
- How to trace the `Received` chain to the true sender IP.
- How to spot obfuscated / lookalike links in the email body.
