# Lab 1 — Log Ingestion and Time Synchronization

In this lab you will configure a centralised syslog collector with `rsyslog` and synchronise the system clock with `chrony`. Accurate timestamps and reliable log ingestion are the foundation of every SOC: if logs from two hosts disagree on time by 30 seconds, you cannot correlate an attack across them. By the end you will understand log levels, log forwarding, and how time drift is detected and corrected (CySA+ 1.1 — Log ingestion, Time synchronization, Logging levels).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install rsyslog and chrony

```bash
apt update && apt install -y rsyslog chrony
systemctl enable --now rsyslog chrony
```

`rsyslog` is the default Linux syslog daemon. `chrony` is the modern NTP client; it converges faster than `ntpd` and tolerates jittery virtual machines.

---

## Step 2 — Verify time synchronization

```bash
chronyc tracking
chronyc sources
```

The `Stratum` field tells you how many hops to a reference clock. `Last offset` is how far your clock was off at the last update. Anything bigger than 1 second is a SOC red flag — it can defeat Kerberos and log correlation.

Force an immediate sync:

```bash
chronyc makestep
```

---

## Step 3 — Inspect the rsyslog configuration

```bash
cat /etc/rsyslog.conf
ls /etc/rsyslog.d/
```

The main file routes messages by **facility** (auth, cron, kern, mail, daemon, local0–7) and **severity** (emerg, alert, crit, err, warning, notice, info, debug). These are the eight CySA+ "logging levels" you must memorise.

---

## Step 4 — Generate logs at each severity

```bash
logger -p user.info "lab1: info message"
logger -p user.warning "lab1: warning message"
logger -p user.err "lab1: error message"
logger -p auth.crit "lab1: simulated critical auth failure"
```

`logger` is the standard tool to inject a syslog message from the shell. Now read them back:

```bash
tail -n 20 /var/log/syslog
grep lab1 /var/log/syslog
```

---

## Step 5 — Configure a central collector (loopback test)

Edit `/etc/rsyslog.d/10-collector.conf`:

```bash
cat > /etc/rsyslog.d/10-collector.conf <<'EOF'
module(load="imudp")
input(type="imudp" port="514")
*.* /var/log/central.log
EOF
systemctl restart rsyslog
```

This loads the UDP input module and writes every received message to `/var/log/central.log`. Now forward local messages to ourselves over UDP:

```bash
echo '*.* @127.0.0.1:514' > /etc/rsyslog.d/20-forward.conf
systemctl restart rsyslog
logger -p local0.notice "lab1: forwarded test"
sleep 1
tail /var/log/central.log
```

You have just built a one-host SIEM ingestion pipeline.

---

## Step 6 — Confirm receiver is listening

```bash
ss -ulnp | grep :514
```

You should see `rsyslogd` bound to UDP/514.

---

## What you learned
- The 8 syslog severity levels and how to filter on them.
- How to inject messages with `logger` and follow them in `/var/log/syslog`.
- How to centralise logs over UDP/514 with `rsyslog`.
- Why time sync is required before correlation — and how to verify it with `chronyc`.
