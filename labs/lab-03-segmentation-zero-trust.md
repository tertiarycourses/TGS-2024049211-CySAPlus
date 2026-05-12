# Lab 3 — Network Segmentation and Zero Trust

In this lab you will build two isolated network "zones" using Linux network namespaces, then enforce a deny-by-default policy between them with `iptables`. This is a hands-on model of the segmentation, SDN, SASE, and Zero Trust concepts in CySA+ 1.1 (Network architecture, Segmentation, Zero trust).

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Why segmentation?

A flat network lets ransomware pivot from any compromised host to every other. Segmentation puts hosts in zones (DMZ, user, server, OT) and a firewall between each zone. **Zero Trust** goes further: every connection is authenticated and authorised even inside the perimeter — there is no "trusted internal".

---

## Step 2 — Create two zones with network namespaces

```bash
ip netns add zone-a
ip netns add zone-b
ip link add veth-a type veth peer name veth-b
ip link set veth-a netns zone-a
ip link set veth-b netns zone-b
ip -n zone-a addr add 10.10.1.1/24 dev veth-a
ip -n zone-b addr add 10.10.1.2/24 dev veth-b
ip -n zone-a link set veth-a up
ip -n zone-b link set veth-b up
ip -n zone-a link set lo up
ip -n zone-b link set lo up
```

Two isolated network stacks now share a wire. Test connectivity:

```bash
ip netns exec zone-a ping -c2 10.10.1.2
```

---

## Step 3 — Apply a deny-by-default policy in zone-b

```bash
ip netns exec zone-b iptables -P INPUT DROP
ip netns exec zone-b iptables -P OUTPUT DROP
ip netns exec zone-b iptables -A INPUT  -i lo -j ACCEPT
ip netns exec zone-b iptables -A OUTPUT -o lo -j ACCEPT
```

Re-test from zone-a:

```bash
ip netns exec zone-a ping -W2 -c2 10.10.1.2
```

All traffic is now blocked — this is the segmentation enforcement point.

---

## Step 4 — Allow only one explicit flow (Zero Trust style)

Permit only SSH (TCP/22) from zone-a, and only an established response:

```bash
ip netns exec zone-b iptables -A INPUT  -p tcp --dport 22 -s 10.10.1.1 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
ip netns exec zone-b iptables -A OUTPUT -p tcp --sport 22 -d 10.10.1.1 -m conntrack --ctstate ESTABLISHED -j ACCEPT
```

ICMP is still blocked, but a TCP probe to port 22 will reach the host:

```bash
apt install -y netcat-openbsd
ip netns exec zone-b nc -l -p 22 &
ip netns exec zone-a nc -zv 10.10.1.2 22
```

You now have one explicitly allowed flow and nothing else — the essence of Zero Trust segmentation.

---

## Step 5 — Map the model to CySA+ vocabulary

| CySA+ concept | What you built |
|---|---|
| On-premises | Both namespaces on local host |
| Network segmentation | Two namespaces with separate stacks |
| Zero Trust | Deny-by-default + per-flow allow rule |
| SASE / SDN | The policy is software-defined, not wired |
| Microsegmentation | Per-port allow at the workload edge |

---

## Step 6 — Clean up

```bash
ip netns del zone-a
ip netns del zone-b
```

---

## What you learned
- How to build two isolated network zones with `ip netns`.
- How `iptables` enforces a segmentation boundary.
- How a deny-by-default + per-flow allow list maps to Zero Trust.
- The CySA+ vocabulary (segmentation, SASE, SDN, ZTNA) in concrete commands.
