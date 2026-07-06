# Lab 18 — Patch Management and Hardening

In this lab you will configure automated patching, list every unpatched CVE on the host, validate a patch with a smoke-test rollback path, and re-score with `lynis`. This maps to CySA+ 2.5 (Patching and configuration management — Testing / Implementation / Rollback / Validation, Maintenance windows, Attack surface reduction).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install patching tools

```bash
apt update && apt install -y unattended-upgrades debsecan lynis needrestart
```

---

## Step 2 — List every unpatched CVE on the host

```bash
debsecan --suite=$(lsb_release -cs) --format=summary | head -30
debsecan --suite=$(lsb_release -cs) --only-fixed | wc -l
```

`debsecan` reads Debian / Ubuntu security tracker data and prints unfixed CVEs by package. `--only-fixed` shows just the ones that have an available patch — your immediate priority list.

---

## Step 3 — Enable unattended security upgrades

```bash
dpkg-reconfigure -plow unattended-upgrades 2>/dev/null || true
cat /etc/apt/apt.conf.d/50unattended-upgrades | head -20
cat /etc/apt/apt.conf.d/20auto-upgrades 2>/dev/null
```

If `20auto-upgrades` does not exist, create it:

```bash
cat > /etc/apt/apt.conf.d/20auto-upgrades <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
EOF
```

This installs security patches every day automatically — the table-stakes **Implementation** control.

---

## Step 4 — Test before patching (CySA+ "Testing")

Patches break things. The CySA+ blueprint expects a staging step. Snapshot the relevant config and a smoke test:

```bash
sha256sum /etc/ssh/sshd_config > /tmp/preupdate.hash
ssh -V 2>&1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:80 2>/dev/null
```

Capture working state. Now apply patches with a dry-run first:

```bash
apt -s upgrade | head -20
```

`-s` simulates. If the simulation lists packages you depend on, schedule a maintenance window first.

---

## Step 5 — Apply the patch (CySA+ "Implementation")

```bash
DEBIAN_FRONTEND=noninteractive apt -y upgrade
```

Inside a real maintenance window you would post-notify stakeholders, then move on.

---

## Step 6 — Validate the patch (CySA+ "Validation")

```bash
debsecan --suite=$(lsb_release -cs) --only-fixed | wc -l   # should drop
needrestart -r l                                            # services needing restart
ssh -V; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:80 2>/dev/null
sha256sum /etc/ssh/sshd_config
diff <(sha256sum /etc/ssh/sshd_config) /tmp/preupdate.hash || echo "config changed"
```

If a critical service is broken, you trigger the rollback plan.

---

## Step 7 — Rollback plan (CySA+ "Rollback")

A real rollback strategy:

| Layer | Mechanism |
|---|---|
| Single binary | `apt install <pkg>=<old-version>` |
| Config drift | restore from git (Lab 19 of N+ analogue) or backup |
| Full VM | revert to snapshot |
| Container | redeploy previous image tag |
| Cloud / AMI | swap launch template / deployment |

Test the rollback path **before** prod — a rollback you have never run is a rollback that does not work.

---

## Step 8 — Attack surface reduction (CySA+ 2.5)

A patch closes a single vuln. Reducing the attack surface eliminates entire classes:

```bash
apt list --installed 2>/dev/null | wc -l
systemctl list-unit-files --state=enabled --no-pager | head
systemctl disable --now cups 2>/dev/null
apt purge -y telnet rsh-client 2>/dev/null
```

Each removed package or disabled service is one less thing to patch.

---

## Step 9 — Re-score with lynis (CySA+ "Compensating control")

```bash
lynis audit system --quick --quiet | tail -20
grep "Hardening index" /var/log/lynis.log
```

Compare against the score from Lab 2. The hardening index should improve after patches + service disablement.

---

## Step 10 — Maintenance window playbook

A template you can drop into Lab 25:

1. Notify stakeholders T-7 days, T-1 day, T-1 hour.
2. Snapshot / backup at T-30 min.
3. Apply patches during the window.
4. Run smoke tests.
5. If any test fails → rollback within 15 min, schedule re-attempt.
6. Send the "all clear" with the new patch level and hardening index.

---

## What you learned
- List unpatched CVEs with `debsecan` and prioritise.
- Enable Ubuntu **unattended security upgrades**.
- Run the Test → Implement → Validate → Rollback sequence.
- Reduce attack surface by removing unused packages and services.
- Use `lynis` to demonstrate a measurable hardening improvement.
