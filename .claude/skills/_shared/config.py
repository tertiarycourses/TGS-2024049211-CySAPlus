"""Shared course config for CySA+ courseware build."""

COURSE_TITLE = "CompTIA Cybersecurity Analyst (CySA+) Training"
COURSE_CODE = "TGS-2024049211"
TSC_TITLE = "Cyber Risk Management"
TSC_CODE = "ICT-SNA-4007-1.1"
VERSION_PPT = "6.0"
VERSION_DOC = "1.0"

KILLERCODA = "https://killercoda.com/playgrounds/scenario/ubuntu"

LEARNING_OUTCOMES = [
    "Identify cyber security risks, threats, and vulnerabilities, and assess their impact on the organization.",
    "Develop cyber risk assessments by consolidating insights from business to identify security gaps.",
    "Identify possible treatments for identified cyber risks, threats, and vulnerabilities.",
    "Implement endorsed treatment measures to address security gaps and ensure data protection.",
]

TSC_KNOWLEDGE = [
    "K1 Cyber risk assessment techniques",
    "K2 Security risks, threats and vulnerabilities",
    "K3 Possible treatments of security risks, threats and vulnerabilities",
    "K4 Required levels of confidentiality, integrity, privacy and personal data protection as well as privacy technologies",
]
TSC_ABILITIES = [
    "A1 Develop cyber risk assessment techniques to identify security loopholes and weaknesses in the business",
    "A2 Design cyber risk assessments by consolidating insights from the business and various functions",
    "A3 Identify cyber security risks, threats and vulnerabilities, and their impact on the organisation",
    "A4 Identify possible treatments for cyber risks, threats and vulnerabilities identified",
    "A5 Implement endorsed treatment and measures to address security gaps",
]

# Domain -> (name, exam weight %, lab numbers, "Topic N")
DOMAINS = [
    {"topic": "Topic 1", "name": "Security Operations", "weight": 33, "labs": list(range(1, 11)),
     "concepts": ["OS & software security", "Logging & log ingestion", "Network architecture & segmentation",
                  "Identity & access management", "Encryption & active defence", "Indicators of malicious activity",
                  "Packet & traffic analysis", "Email analysis", "Threat intelligence & MITRE ATT&CK"]},
    {"topic": "Topic 2", "name": "Vulnerability Management", "weight": 30, "labs": list(range(11, 20)),
     "concepts": ["Asset discovery & network mapping", "Vulnerability scanning (OpenVAS/ZAP/Nikto)",
                  "Analysing scan results", "CVSS scoring & prioritisation", "Web application vulnerabilities (XSS/SQLi)",
                  "Exploitation with Metasploit", "Patch management & hardening", "Attack surface reconnaissance"]},
    {"topic": "Topic 3", "name": "Incident Response and Management", "weight": 20, "labs": list(range(20, 26)),
     "concepts": ["Attack frameworks (Kill Chain, ATT&CK, Diamond)", "Evidence acquisition & chain of custody",
                  "Memory & host forensics", "Log analysis for IR", "Containment & isolation",
                  "IR playbooks & tabletop exercises"]},
    {"topic": "Topic 4", "name": "Reporting and Communication", "weight": 17, "labs": list(range(26, 31)),
     "concepts": ["Vulnerability management reporting", "Executive incident reporting",
                  "Security metrics (MTTD/MTTR)", "Compliance reporting (PCI DSS / ISO 27001 / NIST)",
                  "Stakeholder communication & lessons learned"]},
]

# Environment per lab number
ENV = {n: "Killercoda Ubuntu Playground" for n in range(1, 31)}
ENV.update({
    8: "Killercoda + Web (MXToolbox)",
    9: "Killercoda + Web (VirusTotal)",
    10: "Killercoda + Web (AbuseIPDB, ATT&CK Navigator)",
    12: "Local VM — Greenbone Community Edition (VirtualBox/VMware)",
    14: "Killercoda + Local (Burp Suite Community)",
    16: "Web — FIRST CVSS v3.1 Calculator",
    20: "Web — MITRE ATT&CK Navigator",
})

# Diagram map: lab number -> list of image filenames (from extracted images dir)
DIAGRAMS = {
    1:  ["img_48ab3be242.png"],            # Syslog
    3:  ["img_7c675dab12.png"],            # Jump box / segmentation
    5:  ["img_ac16252bcf.png"],            # Rootkit
    6:  ["img_aa80adb260.png"],            # Threat hunting process
    9:  ["img_e8186f7ac6.png"],            # Hashing
    10: ["img_7e5b2de820.png"],            # Intelligence cycle
    11: ["img_48dc89e0cb.png"],            # Scanning parameters
    12: ["img_d982d7766c.png", "img_df975392f0.png"],  # Nessus demo, Vulnerability identification
    17: ["img_acb9c172ac.png", "img_89d1b25ce1.png"],  # XSS, Session hijack
    15: ["img_2b6565e960.png"],            # Privilege escalation
    20: ["img_34df8d5619.png", "img_0605d5ac69.png"],  # Kill chain, Diamond model
    21: ["img_c9d66737d4.png", "img_fff1869550.png", "img_a056dc1946.png"],  # Acquisition, write blocker, dd demo
    22: ["img_5e96aa3087.png"],            # Windows utilities / memory
    23: ["img_6438df1292.png"],            # Linux forensics
    25: ["img_dc65adb904.png"],            # IR process key roles
}

CONTACT = {
    "web": "www.tertiarycourses.com.sg",
    "email": "enquiry@tertiaryinfotech.com",
    "tel": "+65 6100 0613",
}
