# Lab 2 — OS Hardening and System Process Inspection

In this lab you will audit a Linux host with `lynis`, enable kernel-level auditing with `auditd`, and inspect running processes, kernel modules, and hardware to spot deviations from a baseline. These are exam-blueprint skills under CySA+ 1.1 (Operating system concepts — system hardening, system processes, hardware architecture, file structure).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install hardening and audit tools

```bash
apt update && apt install -y lynis auditd
```

`lynis` is a free CIS-style hardening scanner. `auditd` is the Linux audit subsystem that records syscall-level events.

---

## Step 2 — Inspect the file structure and configuration locations

```bash
ls /etc | head
ls /var/log
ls /proc/sys/kernel | head
```

Cyber analysts must know **where configuration lives**:
- `/etc` — system configuration files
- `/var/log` — log files
- `/proc/sys` and `/sys` — kernel tunables
- `~/.ssh`, `~/.bash_history` — per-user artefacts

---

## Step 3 — Enumerate processes (CySA+ "system processes")

```bash
ps -ef --forest | head -30
ps -eo pid,user,%cpu,%mem,etime,cmd --sort=-%cpu | head
```

Look for unexpected parents — e.g. `bash` spawned by `httpd` is a classic web-shell indicator.

List open network sockets and which process owns them:

```bash
ss -tulnp
```

---

## Step 4 — Inspect the hardware architecture

```bash
lscpu
lsmem 2>/dev/null || free -h
lspci 2>/dev/null | head
uname -a
```

CySA+ expects you to know `x86_64` vs ARM, CPU virtualization flags, and how to read `uname` for kernel version (which CVEs depend on).

---

## Step 5 — Run a Lynis hardening audit

```bash
lynis audit system --quick
```

When it finishes, scroll to **Suggestions** and **Hardening index**. Common findings:
- SSH `PermitRootLogin` should be `no`
- Disable unused filesystems (cramfs, freevxfs)
- Enable process accounting

Read the full report:

```bash
less /var/log/lynis.log
```

---

## Step 6 — Enable auditd and watch a sensitive file

```bash
systemctl enable --now auditd
auditctl -w /etc/passwd -p wa -k passwd_changes
```

`-w` adds a watch, `-p wa` records writes and attribute changes, `-k` tags events with a key. Now trigger an event:

```bash
echo "# test" >> /etc/passwd
ausearch -k passwd_changes -i | tail
```

You should see who, when, and which syscall touched the file.

---

## Step 7 — Apply a quick hardening control

Disable an unused service and verify:

```bash
systemctl list-unit-files --state=enabled | head
systemctl disable --now cron 2>/dev/null
systemctl status cron
```

In production you would also: enable a host firewall (Lab 24), set `umask 027`, and configure `/etc/login.defs` password policy.

---

## What you learned
- Where Linux configuration, logs, and kernel tunables live.
- How to enumerate processes, sockets, hardware, and kernel.
- How to run a free CIS-style audit with `lynis`.
- How to write an `auditd` rule and read the resulting events with `ausearch`.
