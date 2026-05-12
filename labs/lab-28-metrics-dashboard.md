# Lab 28 — Security Metrics Dashboard (MTTD / MTTR)

In this lab you will compute and plot the three KPIs CySA+ 4.2 explicitly calls out — **Mean Time To Detect (MTTD)**, **Mean Time To Respond (MTTR)**, and **Mean Time To Remediate (MTTR-rem)** — plus alert volume. The output is a one-page PNG dashboard for the monthly CISO review.

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install Python + matplotlib

```bash
apt update && apt install -y python3-pip
pip3 install matplotlib --break-system-packages
```

---

## Step 2 — Seed last quarter's incident data

```bash
mkdir -p /tmp/lab28 && cd /tmp/lab28
cat > incidents.csv <<'EOF'
id,opened,first_alert,response_start,remediated,sev,alert_count
INC-101,2026-02-01T09:00,2026-02-01T08:55,2026-02-01T09:12,2026-02-01T13:00,2,18
INC-102,2026-02-08T11:00,2026-02-08T10:45,2026-02-08T11:08,2026-02-09T03:00,1,84
INC-103,2026-02-15T14:00,2026-02-15T13:30,2026-02-15T14:25,2026-02-15T16:00,3,7
INC-104,2026-03-02T08:00,2026-03-02T07:50,2026-03-02T08:09,2026-03-02T12:30,2,22
INC-105,2026-03-12T22:00,2026-03-12T21:55,2026-03-12T22:14,2026-03-13T02:00,2,11
INC-106,2026-04-01T16:00,2026-04-01T15:40,2026-04-01T16:05,2026-04-01T19:00,3,5
INC-107,2026-04-18T03:00,2026-04-18T02:50,2026-04-18T03:08,2026-04-18T05:30,2,14
INC-108,2026-05-13T08:15,2026-05-13T08:00,2026-05-13T08:30,2026-05-13T11:00,1,412
EOF
```

Columns map to CySA+ 4.2 KPIs:
- MTTD = `first_alert` → `opened` (analyst sees the alert)
- MTTR (respond) = `opened` → `response_start`
- MTTR (remediate) = `opened` → `remediated`
- Alert volume = `alert_count`

---

## Step 3 — Compute the KPIs

```bash
cat > kpis.py <<'EOF'
import csv, datetime as dt, statistics

rows=[]
with open("incidents.csv") as f:
    for r in csv.DictReader(f):
        for k in ("opened","first_alert","response_start","remediated"):
            r[k]=dt.datetime.fromisoformat(r[k])
        r["mttd_min"]=(r["opened"]-r["first_alert"]).total_seconds()/60
        r["mttr_resp_min"]=(r["response_start"]-r["opened"]).total_seconds()/60
        r["mttr_rem_min"]=(r["remediated"]-r["opened"]).total_seconds()/60
        rows.append(r)

print(f"Incidents: {len(rows)}")
print(f"MTTD          mean={statistics.mean(r['mttd_min'] for r in rows):.1f} min")
print(f"MTTR respond  mean={statistics.mean(r['mttr_resp_min'] for r in rows):.1f} min")
print(f"MTTR remed.   mean={statistics.mean(r['mttr_rem_min'] for r in rows):.1f} min")
print(f"Alert volume  total={sum(int(r['alert_count']) for r in rows)}")
EOF
python3 kpis.py
```

The CISO target is typically MTTD < 30 min and MTTR-respond < 60 min. You now know whether you hit it.

---

## Step 4 — Plot the dashboard

```bash
cat > dashboard.py <<'EOF'
import csv, datetime as dt, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows=[]
with open("incidents.csv") as f:
    for r in csv.DictReader(f):
        for k in ("opened","first_alert","response_start","remediated"):
            r[k]=dt.datetime.fromisoformat(r[k])
        rows.append(r)

rows.sort(key=lambda r:r["opened"])
ids   = [r["id"]                                          for r in rows]
mttd  = [(r["opened"]-r["first_alert"]).total_seconds()/60          for r in rows]
mtres = [(r["response_start"]-r["opened"]).total_seconds()/60       for r in rows]
mtrem = [(r["remediated"]-r["opened"]).total_seconds()/60           for r in rows]
vol   = [int(r["alert_count"])                                      for r in rows]

fig, ax = plt.subplots(2, 2, figsize=(12,8))
ax[0,0].bar(ids, mttd, color="#4477aa");  ax[0,0].set_title("MTTD (min)");          ax[0,0].axhline(30, color="r", ls="--")
ax[0,1].bar(ids, mtres, color="#66ccee"); ax[0,1].set_title("MTTR-respond (min)");   ax[0,1].axhline(60, color="r", ls="--")
ax[1,0].bar(ids, mtrem, color="#ee6677"); ax[1,0].set_title("MTTR-remediate (min)")
ax[1,1].bar(ids, vol,  color="#ccbb44");  ax[1,1].set_title("Alerts per incident")
for a in ax.flatten():
    a.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig("dashboard.png", dpi=120)
print("wrote dashboard.png")
EOF
python3 dashboard.py
ls -lh dashboard.png
```

Open `dashboard.png` from Killercoda's file browser. Red dashed lines mark SLO targets — any bar over the line is an incident that breached SLO.

---

## Step 5 — Identify trends (CySA+ "Trends")

```bash
python3 - <<'EOF'
import csv, datetime as dt
buckets={}
with open("incidents.csv") as f:
    for r in csv.DictReader(f):
        m=r["opened"][:7]            # YYYY-MM
        buckets.setdefault(m,[]).append(r)
for m in sorted(buckets):
    print(m, "incidents:", len(buckets[m]),
          "sev1:", sum(1 for r in buckets[m] if r["sev"]=="1"))
EOF
```

A spike in sev-1 month-over-month is the headline finding for the CISO slide.

---

## Step 6 — Critical vulnerabilities & zero-day exposure

CySA+ 4.1 names "Critical vulnerabilities and zero-days" as a top metric. Add a second feed (from Lab 26 `findings.csv`):

| Metric | This month | Target |
|--------|------------|--------|
| Open P1 (CVSS ≥ 9.0) | 2 | 0 |
| Zero-days with no vendor patch | 0 | 0 |
| KEV-catalog hits open > 7 d | 1 | 0 |

Stack-rank with the table above on the same dashboard page.

---

## Step 7 — SLO scorecard

CySA+ 4.1 / 4.2 "SLOs". A traffic-light board the executive can read in 5 seconds:

```bash
cat > slo.md <<'EOF'
| SLO | Target | Actual | Status |
|-----|--------|--------|--------|
| MTTD | < 30 min | 17 min | 🟢 |
| MTTR respond | < 60 min | 19 min | 🟢 |
| MTTR remediate (sev 1) | < 4 h | 3 h | 🟢 |
| P1 open > 7 d | 0 | 1 | 🔴 |
| Zero-days unpatched | 0 | 0 | 🟢 |
EOF
cat slo.md
```

---

## What you learned
- Compute MTTD, MTTR-respond, MTTR-remediate, and alert volume from raw incident data.
- Plot a single-page KPI dashboard with `matplotlib`.
- Identify monthly trends and SLO breaches.
- Combine vulnerability KPIs (P1, zero-day, KEV) with incident KPIs into an executive scorecard.
