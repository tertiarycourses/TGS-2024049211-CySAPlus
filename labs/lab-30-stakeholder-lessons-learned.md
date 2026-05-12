# Lab 30 — Stakeholder Communication and Lessons Learned

In this lab you will draft the four canonical post-incident communications — **executive**, **customer**, **regulator**, **public/media** — and close the incident with a structured **lessons learned** and **root cause analysis** that feeds the next preparation cycle. This maps to CySA+ 4.2 (Communications — Legal, Public relations, Customer comms, Media, Regulatory reporting, Law enforcement; Root cause analysis; Lessons learned; Stakeholder identification).

This lab is writing-heavy. Output: four templates plus a 5-Whys analysis.

---

## Step 1 — Identify every stakeholder for CASE-001

Carry the CASE-001 scenario from Lab 27. Tabulate stakeholders by influence and interest:

| Stakeholder | Role | Notify? | Channel | Owner |
|---|---|---|---|---|
| CEO | Decision authority | Yes (sev 1) | Phone + email | CISO |
| CISO | IR sponsor | Yes | War room | IC |
| CFO | Finance scope owner | Yes | Email | CISO |
| Legal counsel | Privilege, hold, regulator | Yes (immediately) | Phone | IC |
| Comms / PR | Public messaging | Yes (sev 1) | War room | CISO |
| Affected customers | Subjects of breach | Yes (within 72 h) | Templated email | Comms |
| Supervisory Authority (GDPR DPA) | Regulator | Yes (within 72 h) | Web form + letter | Legal |
| Cyber-insurance carrier | Coverage trigger | Yes | Phone | Legal |
| Law enforcement | Investigation | Optional | Phone referral | Legal |
| Employees | Confidence + awareness | After containment | Townhall | CEO/CISO |
| Media | Public statement | If asked | Holding statement | Comms |

CySA+ 4.2 names this list explicitly — never skip Legal and Regulatory.

---

## Step 2 — Executive briefing template

```markdown
**To:** CEO, CFO, General Counsel
**From:** CISO
**Subject:** Sev-1 incident CASE-001 — interim update [TIME UTC]

**Bottom line up front:** ~1 GB of customer data exfiltrated from finance file share via phishing → credential theft. Host isolated. No further movement.

**Status:** Contained. Eradication in progress.
**Customer impact:** 87 records (names + IBAN). GDPR-notifiable.
**Press exposure:** Low so far; holding statement ready.
**Decisions needed from you:** (1) Authorise customer notification draft. (2) Approve law-enforcement referral.

Next update in 60 min.
```

Keep ≤ 1 screen. Bullets, not paragraphs. Decisions called out.

---

## Step 3 — Customer notification template (GDPR-style)

```markdown
**Subject:** Important security notice about your data

Dear [Name],

On 13 May 2026, we discovered unauthorised access to a file containing your name and bank account (IBAN). We acted within minutes to stop the access and have no evidence the data has been used. Your password and online banking access are not affected.

**What we are doing**
- Engaged independent forensic specialists
- Notified the supervisory authority and law enforcement
- Strengthened the controls that allowed this incident

**What you should do**
- Watch your bank statements for any unusual debit and report to your bank
- Be alert to phishing emails or phone calls referencing this notice — we will never ask for your password
- Free guidance: [link to advice page]

If you have questions, contact our dedicated team at [email] / [phone] (24×7 for the next 30 days).

We are sorry this happened.

[Signed, Data Protection Officer]
```

Plain language. No jargon. Concrete actions. Apology.

---

## Step 4 — Regulator notification (GDPR Art. 33 template)

```markdown
**Notification of personal data breach — Art. 33 GDPR**

| Field | Value |
|-------|-------|
| Controller | [Company name + DPA registration #] |
| Date/time of discovery | 2026-05-13 08:30 UTC |
| Nature of breach | Confidentiality breach (unauthorised exfiltration) |
| Categories of data | Name + IBAN |
| Number of records | ~87 |
| Likely consequences | Financial fraud risk; reputational |
| Measures taken | Host isolated; account disabled; MFA review; customer notification within 72 h |
| DPO contact | dpo@example.com / +XX phone |
```

Submit via the supervisory authority's web portal. Many EU DPAs have a 72-hour clock that starts at **awareness**, not at containment.

---

## Step 5 — Public / media holding statement

```markdown
We recently identified a cybersecurity incident affecting a limited number of customer records in our finance system. We acted quickly to contain it, engaged independent specialists, and notified the relevant authorities. Affected customers are being contacted directly with specific advice. We continue to monitor and we are sorry for any concern this may cause.

For more information, please contact press@example.com.
```

Keep ≤ 100 words. No specifics that contradict customer notification or compromise the investigation.

---

## Step 6 — Law enforcement referral checklist

- Make the call **after** Legal authorises and **only** through the pre-agreed contact (national cybercrime unit).
- Bring: incident report, IOC list, chain-of-custody form, evidence hashes.
- Do **not** alter or "clean up" evidence on the way.
- Agree what may be shared with the regulator vs the public during the open investigation.

---

## Step 7 — Root cause analysis — 5 Whys

```markdown
1. **Why** did the attacker exfiltrate 1 GB? → They had valid credentials and unrestricted egress.
2. **Why** did they have valid credentials? → User entered creds into a phishing page.
3. **Why** did the user fall for the phish? → Email passed DMARC checks at the gateway.
4. **Why** did it pass DMARC? → Receiving policy was `p=none` (monitor only).
5. **Why** was the policy still `p=none`? → No owner; left over from initial rollout 18 months ago.

**Root cause:** Absent operational ownership of DMARC enforcement — not user error.
```

This phrasing matters: blaming the user generates fear, not improvement. Blaming the process generates a fix (Lab 25's action items).

---

## Step 8 — Lessons learned register

```markdown
# Lessons Learned — CASE-001

## Keep doing
- Tabletop muscle memory; IC named in 5 min.
- Pre-built isolation runbook applied cleanly.

## Start doing
- Quarterly review of DMARC and DKIM enforcement levels.
- Maintain regulator notification template ready to fill in.

## Stop doing
- Treating phishing simulations as a checkbox training metric.

## Actions (with owners + due dates)
1. DMARC reject everywhere — Email Ops — 2026-05-31
2. FIDO2 rollout (Finance, Exec) — IdAM — 2026-07-01
3. Quarterly OOB comms test — SOC — recurring
4. Pre-draft regulator + customer templates — Legal + Comms — 2026-06-15
```

The output of this register is the input to next quarter's **Preparation** phase — closing the NIST loop one more time.

---

## Step 9 — Stakeholder map → CySA+ 4.2 final crosswalk

| Step | CySA+ 4.2 bullet |
|---|---|
| 1 stakeholder map | Stakeholder identification and communication |
| 2 executive template | Communications — internal / executive |
| 3 customer template | Communications — Customer communication |
| 4 regulator template | Communications — Regulatory reporting |
| 5 media template | Communications — Public relations, Media |
| 6 law enforcement | Communications — Law enforcement |
| 7 5-Whys | Root cause analysis |
| 8 lessons learned | Lessons learned |

---

## What you learned
- Identify every stakeholder for a sev-1 incident and pick the right channel for each.
- Draft executive, customer, regulator, and media communications.
- Run a 5-Whys RCA that targets process, not people.
- Close the incident with a structured Lessons Learned register that feeds back into the IR life cycle.
