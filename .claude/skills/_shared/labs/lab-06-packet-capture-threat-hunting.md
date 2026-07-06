# Lab 6 — Packet Capture for Threat Hunting

In this lab you will capture live traffic with `tcpdump`, then perform analyst-level extraction with `tshark`: pulling HTTP host headers, DNS queries, and TLS SNI fields out of a pcap. These are exam-blueprint skills under CySA+ 1.3 (Packet capture — Wireshark, tcpdump).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Install tools

```bash
apt update && apt install -y tcpdump tshark curl dnsutils
```

When prompted by tshark, answer "No" — non-root packet capture is not needed inside Killercoda.

---

## Step 2 — Capture a known-traffic sample to a pcap

```bash
tcpdump -i any -nn -w /tmp/sample.pcap -G 10 -W 1 &
sleep 1
curl -s https://example.com > /dev/null
dig +short google.com
curl -s http://neverssl.com > /dev/null
wait
ls -lh /tmp/sample.pcap
```

`-w` writes a pcap, `-G 10 -W 1` rotates after 10 seconds and stops.

---

## Step 3 — Extract DNS queries from the pcap

```bash
tshark -r /tmp/sample.pcap -Y 'dns.flags.response==0' -T fields -e dns.qry.name | sort -u
```

In a threat hunt this is how you spot DGA-style randomised domains, DNS tunnelling, or queries to known-bad domains.

---

## Step 4 — Extract HTTP host headers and URIs

```bash
tshark -r /tmp/sample.pcap -Y http.request -T fields -e http.host -e http.request.uri
```

Cleartext HTTP requests reveal command-and-control URLs, downloaded second stages, and exfiltration endpoints.

---

## Step 5 — Extract TLS SNI (server name indicator)

```bash
tshark -r /tmp/sample.pcap -Y 'tls.handshake.type==1' -T fields -e tls.handshake.extensions_server_name
```

Even when payloads are encrypted, the SNI in the ClientHello tells you which host the client tried to reach — the single most useful field for TLS-era hunting.

---

## Step 6 — Top talkers / conversations

```bash
tshark -r /tmp/sample.pcap -q -z conv,ip | head -20
```

The output ranks IP pairs by bytes. A workstation talking 500 MB to an unfamiliar IP is a candidate exfiltration channel.

---

## Step 7 — Apply a display filter while sniffing live

```bash
tshark -i any -Y 'dns and ip.dst==8.8.8.8' -c 5
```

Display filters (Wireshark-style) are richer than BPF; they can match application-layer fields like `http.user_agent` or `dns.qry.name contains "tor"`.

---

## Step 8 — Hunt a specific IOC across a pcap

Imagine your threat-intel feed flags `93.184.216.34`:

```bash
tshark -r /tmp/sample.pcap -Y 'ip.addr==93.184.216.34' -T fields -e frame.time -e ip.src -e ip.dst -e _ws.col.Protocol
```

You now have every packet, every protocol, every timestamp touching that IP — directly feeding the incident timeline (Lab 27).

---

## What you learned
- How to capture to a rotating pcap with `tcpdump`.
- How to extract DNS, HTTP, and TLS SNI fields with `tshark`.
- How to rank top talkers and pivot on a specific IOC.
- The CySA+ 1.3 muscle memory for any packet-capture exam question.
