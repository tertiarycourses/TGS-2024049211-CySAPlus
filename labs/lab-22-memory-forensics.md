# Lab 22 — Memory Forensics with Volatility

In this lab you will analyse a memory image with **Volatility 3** — listing processes, network connections, command lines, and pulling DLLs / injected code. Memory forensics finds artefacts that never touched disk (Cobalt Strike beacons, in-memory shellcode). This maps to CySA+ 3.2 (Data and log analysis, Evidence acquisitions — Preservation).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install Volatility 3

```bash
apt update && apt install -y python3-pip git
pip3 install volatility3 --break-system-packages
vol -h | head
```

Volatility 3 is a complete rewrite in Python 3 with built-in symbol management — no manual profile required.

---

## Step 2 — Obtain a sample memory image

Public training images are large but free. Two reliable sources:

- **Volatility Foundation sample memory** — https://github.com/volatilityfoundation/volatility/wiki/Memory-Samples
- **MalwareTech BlueKeep sample** — search for `cridex.vmem` / `xp-laptop-2005.img`

```bash
# Example download (~30 MB):
wget -q -O /tmp/cridex.vmem \
  https://downloads.volatilityfoundation.org/releases/Tutorial/cridex.vmem 2>/dev/null \
  || echo "Mirror may be down — provide your own image"
ls -lh /tmp/cridex.vmem 2>/dev/null
```

If the mirror is unavailable, any `.vmem` / `.lime` / `.raw` image works — including one captured in Lab 21.

---

## Step 3 — Identify the image

```bash
vol -f /tmp/cridex.vmem windows.info
```

Output identifies the OS, build, and addresses Volatility will use for the analysis.

---

## Step 4 — List processes

```bash
vol -f /tmp/cridex.vmem windows.pslist
vol -f /tmp/cridex.vmem windows.pstree
```

Look for:
- Orphans (PPID = 0 or pointing to a dead parent)
- Office app spawning `cmd.exe` / `powershell.exe`
- Multiple `svchost.exe` outside `services.exe`

---

## Step 5 — Hunt hidden processes

```bash
vol -f /tmp/cridex.vmem windows.psscan       # scans pool, finds unlinked PIDs
vol -f /tmp/cridex.vmem windows.psxview      # diff between listing methods
```

A row that appears in `psscan` but not `pslist` is a rootkit-hidden process.

---

## Step 6 — Recover command lines

```bash
vol -f /tmp/cridex.vmem windows.cmdline
```

The command line of a malicious process often contains the C2 URL, base64 payload, or `-NoProfile -EncodedCommand …` — your fastest IOC.

---

## Step 7 — Network connections at time of capture

```bash
vol -f /tmp/cridex.vmem windows.netscan
```

Maps PID → local IP:port → remote IP:port. Cross-reference remote IPs against threat-intel (Lab 10).

---

## Step 8 — DLL injection / code injection

```bash
vol -f /tmp/cridex.vmem windows.dlllist --pid <SUSPECT_PID>
vol -f /tmp/cridex.vmem windows.malfind
```

`malfind` looks for memory regions marked **RWX** with PE headers or shellcode — a textbook process-injection indicator.

---

## Step 9 — Dump a suspect process and triage it

```bash
mkdir -p /tmp/dump
vol -f /tmp/cridex.vmem -o /tmp/dump windows.dumpfiles --pid <SUSPECT_PID>
ls /tmp/dump | head
# Then run the file through Lab 9 (strings, yara, VirusTotal hash)
sha256sum /tmp/dump/*
```

You now have a static artefact for AV/sandbox submission — derived from RAM only.

---

## Step 10 — Linux memory images

For Lab 21's AVML output, the equivalent plugins live under `linux.*`:

```bash
vol -f /tmp/case_001/memory.lime linux.pslist
vol -f /tmp/case_001/memory.lime linux.bash    # recover shell history
```

`linux.bash` is gold for incident response — it shows the attacker's typed commands.

---

## What you learned
- Install and orient Volatility 3 against a memory image.
- Enumerate processes, hidden processes, command lines, and live connections.
- Detect injected code with `malfind`.
- Dump processes to disk and feed them into Lab 9's static triage workflow.
