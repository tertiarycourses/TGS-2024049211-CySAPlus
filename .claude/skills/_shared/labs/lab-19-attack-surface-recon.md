# Lab 19 — Attack Surface Reconnaissance

In this lab you will enumerate the external attack surface of a target organisation using **theHarvester** and **recon-ng**, plus free web services like crt.sh, DNSDumpster, and Shodan. This maps to CySA+ 2.5 (Attack surface management — Edge discovery, Passive discovery, Penetration testing, Bug bounty) and 2.2 (Multipurpose — Recon-ng).

Run on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

> **Scope:** Only enumerate domains you own or have written permission for. The example uses `example.com` (IANA reserved).

---

## Step 1 — Install tools

```bash
apt update && apt install -y theharvester recon-ng curl whois dnsutils jq
```

---

## Step 2 — Passive discovery with theHarvester

```bash
theHarvester -d example.com -b duckduckgo,crtsh,bing -l 100
```

`-b` selects sources. Free, passive sources usable without keys: `crtsh`, `duckduckgo`, `bing`, `anubis`, `hackertarget`. Output includes:
- Subdomains
- Email addresses
- Linked IPs

---

## Step 3 — Certificate-transparency search (edge discovery)

Certificate Transparency logs are the **single best** free subdomain discovery source — every TLS cert ever issued is public.

```bash
curl -s 'https://crt.sh/?q=%25.example.com&output=json' | jq -r '.[].name_value' | sort -u | head
```

Subdomains nobody links to in the navigation (`vpn.`, `admin.`, `dev.`, `staging.`) often show up here.

---

## Step 4 — Recon-ng modular framework

```bash
recon-ng
```

Inside the recon-ng shell:

```
[recon-ng][default] > workspaces create cysa_lab19
[recon-ng][cysa_lab19] > marketplace search hackertarget
[recon-ng][cysa_lab19] > marketplace install recon/domains-hosts/hackertarget
[recon-ng][cysa_lab19] > modules load recon/domains-hosts/hackertarget
[recon-ng][cysa_lab19][hackertarget] > options set SOURCE example.com
[recon-ng][cysa_lab19][hackertarget] > run
[recon-ng][cysa_lab19][hackertarget] > show hosts
```

`hackertarget` is keyless and free. Other useful modules:
- `recon/domains-hosts/hackertarget`
- `recon/companies-contacts/whois_pocs`
- `recon/hosts-hosts/resolve`
- `reporting/csv` / `reporting/html`

Export the dataset:

```
[recon-ng][cysa_lab19] > modules load reporting/csv
[recon-ng][cysa_lab19][csv] > options set FILENAME /tmp/recon.csv
[recon-ng][cysa_lab19][csv] > run
```

---

## Step 5 — DNS enumeration

```bash
for sub in www mail vpn admin api dev staging test mx ftp; do
  ip=$(dig +short $sub.example.com)
  [ -n "$ip" ] && echo "$sub.example.com -> $ip"
done

dig axfr @ns.example.com example.com 2>/dev/null
```

The second command attempts a zone transfer. A successful AXFR from an external client is a misconfiguration — instant report finding.

---

## Step 6 — Shodan-style passive port discovery (browser)

Free tier (sign up required):
- **Shodan** — https://www.shodan.io/search?query=org%3A%22Example+Inc%22
- **Censys** — https://search.censys.io

Search by organisation name, ASN, or domain. You will see open ports, banner versions, certs, and geolocation — all without sending a packet from your IP.

---

## Step 7 — Inventory the findings

```bash
mkdir -p /tmp/lab19
cat > /tmp/lab19/inventory.md <<EOF
# External attack surface: example.com (snapshot $(date -I))

| Asset | Port | Service | Source | Risk note |
|-------|------|---------|--------|-----------|
| www.example.com | 443 | nginx | crt.sh, dig | TLS expiring soon |
| api.example.com | 443 | api gateway | crt.sh | Public, monitor |
| admin.example.com | 8443 | admin panel | crt.sh | Should be VPN-only |
EOF
cat /tmp/lab19/inventory.md
```

This is the deliverable a SOC analyst hands to the vulnerability-management team.

---

## Step 8 — Map the lab to CySA+ 2.5 bullet points

| Lab step | CySA+ 2.5 vocab |
|---|---|
| theHarvester / crt.sh / DNS | **Edge discovery**, **Passive discovery** |
| Recon-ng hackertarget | **Passive discovery** |
| Shodan / Censys | **Passive discovery** |
| Nmap (Lab 11) on these hosts | **Security controls testing** |
| Metasploit (Lab 15) `check` | **Penetration testing**, **Adversary emulation** |
| Public program | **Bug bounty** |

---

## What you learned
- Use theHarvester and crt.sh for passive subdomain discovery.
- Drive Recon-ng's workspace/module model and export reports.
- Combine DNS, certificate transparency, and Shodan-style services into a single external inventory.
- Map enumeration techniques to CySA+ attack-surface-management vocabulary.
