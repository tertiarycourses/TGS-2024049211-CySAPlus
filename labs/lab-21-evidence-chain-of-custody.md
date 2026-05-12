# Lab 21 — Evidence Acquisition and Chain of Custody

In this lab you will perform a forensically sound image of a "compromised" disk and memory, generate hashes, fill in a chain-of-custody form, and verify integrity. This maps to CySA+ 3.2 (Evidence acquisitions — Chain of custody, Validating data integrity, Preservation, Legal hold).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Why order matters: order of volatility

Before touching the system, recall the volatility ladder (most-to-least volatile):

1. CPU registers, cache
2. Routing table, ARP cache, process table, kernel statistics, memory
3. Temporary file systems / swap
4. Disk
5. Remote logs
6. Backups / archival media

Capture in that order. Skip ahead and you destroy evidence you cannot recover.

---

## Step 2 — Create a controlled "evidence" target

```bash
mkdir -p /tmp/evidence /tmp/case_001
dd if=/dev/zero of=/tmp/evidence/suspect.img bs=1M count=8 2>/dev/null
mkfs.ext4 -F /tmp/evidence/suspect.img >/dev/null
mkdir -p /mnt/suspect
mount -o loop /tmp/evidence/suspect.img /mnt/suspect
echo "stolen_creds: admin/p@ssw0rd" > /mnt/suspect/secret.txt
echo "C2: 185.220.101.45" > /mnt/suspect/c2.txt
umount /mnt/suspect
```

You now have an 8 MB "disk" with two artefacts.

---

## Step 3 — Hash the source BEFORE imaging (preservation)

```bash
sha256sum /tmp/evidence/suspect.img | tee /tmp/case_001/source.sha256
md5sum    /tmp/evidence/suspect.img | tee -a /tmp/case_001/source.md5
```

Both hashes are recorded — MD5 for legacy compatibility, SHA-256 for cryptographic strength.

---

## Step 4 — Make a bit-for-bit image (acquisition)

```bash
dd if=/tmp/evidence/suspect.img of=/tmp/case_001/image.dd bs=1M status=progress conv=noerror,sync
```

Real engagements use a hardware write-blocker plus `dcfldd` or `dc3dd` (FTK Imager on Windows) — they hash on-the-fly and log every read error. The principle is the same: never write to the source.

---

## Step 5 — Verify integrity (validating data integrity)

```bash
sha256sum /tmp/case_001/image.dd | tee /tmp/case_001/image.sha256
diff /tmp/case_001/source.sha256 <(sed 's|image.dd|/tmp/evidence/suspect.img|' /tmp/case_001/image.sha256) \
  && echo "INTEGRITY OK" || echo "INTEGRITY FAILED"
```

If the hashes match, the image is admissible. If not, you start over.

---

## Step 6 — Capture volatile memory (memory acquisition)

In Linux the standard free tools are:

```bash
apt install -y avml 2>/dev/null || echo "avml may need manual install"
# AVML is Microsoft's free Linux memory acquirer:
# wget https://github.com/microsoft/avml/releases/latest/download/avml
# chmod +x ./avml && ./avml /tmp/case_001/memory.lime
```

On Windows the equivalent free tools are **WinPMEM**, **DumpIt**, or **Magnet RAM Capture**. Always hash the resulting `.lime` / `.raw` file the same way as the disk image.

---

## Step 7 — Build the chain-of-custody form

```bash
cat > /tmp/case_001/chain_of_custody.md <<EOF
# Chain of Custody — Case 001

| Item | Value |
|------|-------|
| Case ID | CASE-001 |
| Incident date | $(date -I) |
| Evidence ID | EV-001 |
| Description | 8 MB disk image, ext4, mounted /mnt/suspect at acquisition |
| Acquirer | Analyst A. Chan |
| Acquisition method | dd (bit-for-bit) |
| Source SHA-256 | $(awk '{print $1}' /tmp/case_001/source.sha256) |
| Image  SHA-256 | $(awk '{print $1}' /tmp/case_001/image.sha256) |
| Integrity | $(diff -q /tmp/case_001/source.sha256 <(sed 's|image.dd|/tmp/evidence/suspect.img|' /tmp/case_001/image.sha256) >/dev/null && echo MATCH || echo MISMATCH) |
| Storage location | Locked evidence safe, drawer 3 |

## Transfer log
| Datetime | From | To | Reason | Signature |
|----------|------|----|--------|-----------|
| $(date -Iseconds) | Analyst A. Chan | Evidence Locker | Initial seal | _________ |
EOF
cat /tmp/case_001/chain_of_custody.md
```

Every transfer of the evidence (analyst → locker → court) gets a new row. A gap in the log is enough to throw out the evidence in court.

---

## Step 8 — Legal hold

A **legal hold** suspends normal retention policies for evidence relevant to litigation or regulatory request. Once issued by legal counsel:
- No deletion, no rotation, no overwriting.
- All custodians notified in writing.
- Original media stored in a sealed evidence bag with the tag from Step 7.

In Linux that means moving the image to a write-protected store:

```bash
chmod -w /tmp/case_001/image.dd
ls -l /tmp/case_001/
```

---

## Step 9 — Working copies

You analyse the **working copy**, never the original.

```bash
cp /tmp/case_001/image.dd /tmp/case_001/working_copy.dd
sha256sum /tmp/case_001/working_copy.dd
```

If your analysis corrupts the working copy, you can always recreate it from the sealed original.

---

## What you learned
- The order of volatility and why it dictates acquisition sequence.
- How to image a disk with `dd` and verify with SHA-256.
- Where Linux/Windows memory acquisition tools live.
- How to fill a chain-of-custody form and apply a legal hold.
