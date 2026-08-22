from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.database.models import Alert, IOC, ThreatSource, User
from app.services.risk_service import calculate_risk_score, determine_severity
from app.services.threat_service import save_ioc


def _datetime_days_ago(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def seed_users(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    db.add_all(
        [
            User(full_name="Administrator", email="admin@cti.local", hashed_password=get_password_hash("Admin@123"), role="Administrator"),
            User(full_name="Analyst", email="analyst@cti.local", hashed_password=get_password_hash("Analyst@123"), role="Analyst"),
        ]
    )
    db.commit()


def seed_sources(db: Session) -> None:
    if db.query(ThreatSource).count() > 0:
        return

    db.add_all(
        [
            ThreatSource(source_name="InternetDB", reliability_weight=78, api_endpoint="https://internetdb.shodan.io/{ip}"),
            ThreatSource(source_name="VirusTotal", reliability_weight=86, api_endpoint="https://www.virustotal.com/"),
            ThreatSource(source_name="AbuseIPDB", reliability_weight=82, api_endpoint="https://api.abuseipdb.com/"),
            ThreatSource(source_name="AlienVault OTX", reliability_weight=74, api_endpoint="https://otx.alienvault.com/"),
        ]
    )
    db.commit()


def _demo_ioc_records() -> list[dict]:
    today = datetime.now(timezone.utc)
    return [
        {"ioc_type": "IP", "ioc_value": "185.220.101.1", "source": "AbuseIPDB", "confidence": 95, "description": "Tor exit node observed in threat intel feeds.", "first_seen": today - timedelta(days=18), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["AbuseIPDB", "InternetDB"], "ports": [22, 80, 443], "vulnerabilities": ["CVE-2024-3094"]}},
        {"ioc_type": "IP", "ioc_value": "45.133.1.15", "source": "VirusTotal", "confidence": 88, "description": "Suspicious scanning host.", "first_seen": today - timedelta(days=16), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["VirusTotal"], "ports": [21, 445], "tags": ["scanner"]}},
        {"ioc_type": "IP", "ioc_value": "102.130.115.231", "source": "InternetDB", "confidence": 84, "description": "Exposed host with open RDP.", "first_seen": today - timedelta(days=21), "last_seen": today - timedelta(days=3), "raw_metadata": {"sources": ["InternetDB"], "ports": [3389], "tags": ["rdp"]}},
        {"ioc_type": "IP", "ioc_value": "104.248.63.15", "source": "AlienVault OTX", "confidence": 91, "description": "Known malicious infrastructure.", "first_seen": today - timedelta(days=15), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["AlienVault OTX", "VirusTotal"], "ports": [80, 8080], "vulnerabilities": ["CVE-2023-1389", "CVE-2024-21762"]}},
        {"ioc_type": "IP", "ioc_value": "91.92.109.126", "source": "AbuseIPDB", "confidence": 89, "description": "Frequent brute-force source.", "first_seen": today - timedelta(days=14), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["AbuseIPDB"], "ports": [23, 80], "tags": ["bruteforce"]}},
        {"ioc_type": "IP", "ioc_value": "45.141.87.12", "source": "InternetDB", "confidence": 76, "description": "Open services and known exposure.", "first_seen": today - timedelta(days=11), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["InternetDB"], "ports": [25, 110, 443], "tags": ["mail"]}},
        {"ioc_type": "Domain", "ioc_value": "secure-login-verification.net", "source": "VirusTotal", "confidence": 93, "description": "Phishing domain impersonating login portals.", "first_seen": today - timedelta(days=27), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["VirusTotal", "AlienVault OTX"], "tags": ["phishing", "credential-theft"]}},
        {"ioc_type": "Domain", "ioc_value": "cloud-update-service.org", "source": "AlienVault OTX", "confidence": 87, "description": "Suspicious domain linked to malware delivery.", "first_seen": today - timedelta(days=19), "last_seen": today - timedelta(days=4), "raw_metadata": {"sources": ["AlienVault OTX"], "tags": ["malware"]}},
        {"ioc_type": "Domain", "ioc_value": "mfa-reset-center.com", "source": "AbuseIPDB", "confidence": 79, "description": "Lookalike domain used for account takeovers.", "first_seen": today - timedelta(days=13), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["AbuseIPDB"], "tags": ["phishing"]}},
        {"ioc_type": "Domain", "ioc_value": "cdn-security-check.biz", "source": "VirusTotal", "confidence": 81, "description": "Suspicious CDN impersonation domain.", "first_seen": today - timedelta(days=10), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["VirusTotal"], "tags": ["malspam"]}},
        {"ioc_type": "URL", "ioc_value": "http://secure-login-verification.net/portal", "source": "VirusTotal", "confidence": 92, "description": "Credential harvesting landing page.", "first_seen": today - timedelta(days=23), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["VirusTotal"], "tags": ["phishing", "login"]}},
        {"ioc_type": "URL", "ioc_value": "http://cloud-update-service.org/download.exe", "source": "AlienVault OTX", "confidence": 90, "description": "Malware delivery URL.", "first_seen": today - timedelta(days=20), "last_seen": today - timedelta(days=3), "raw_metadata": {"sources": ["AlienVault OTX", "VirusTotal"], "tags": ["malware", "dropper"]}},
        {"ioc_type": "URL", "ioc_value": "https://mfa-reset-center.com/auth", "source": "AbuseIPDB", "confidence": 84, "description": "Phishing authentication page.", "first_seen": today - timedelta(days=8), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["AbuseIPDB"], "tags": ["phishing"]}},
        {"ioc_type": "URL", "ioc_value": "http://cdn-security-check.biz/update", "source": "VirusTotal", "confidence": 80, "description": "Suspicious software update lure.", "first_seen": today - timedelta(days=12), "last_seen": today - timedelta(days=5), "raw_metadata": {"sources": ["VirusTotal"], "tags": ["malware"]}},
        {"ioc_type": "Hash", "ioc_value": "44d88612fea8a8f36de82e1278abb02f", "source": "VirusTotal", "confidence": 98, "description": "Known malicious sample hash.", "first_seen": today - timedelta(days=35), "last_seen": today - timedelta(days=5), "raw_metadata": {"sources": ["VirusTotal", "AlienVault OTX"], "tags": ["malware", "trojan"]}},
        {"ioc_type": "Hash", "ioc_value": "e2fc714c4727ee9395f324cd2e7f331f", "source": "AlienVault OTX", "confidence": 86, "description": "Suspicious executable hash.", "first_seen": today - timedelta(days=29), "last_seen": today - timedelta(days=4), "raw_metadata": {"sources": ["AlienVault OTX"], "tags": ["malware"]}},
        {"ioc_type": "Hash", "ioc_value": "a7b7c8d9e0f112233445566778899abc", "source": "AbuseIPDB", "confidence": 74, "description": "Hash observed in suspicious attachment campaign.", "first_seen": today - timedelta(days=17), "last_seen": today - timedelta(days=3), "raw_metadata": {"sources": ["AbuseIPDB"], "tags": ["spam"]}},
        {"ioc_type": "Hash", "ioc_value": "0123456789abcdef0123456789abcdef01234567", "source": "InternetDB", "confidence": 77, "description": "SHA1 sample associated with unwanted software.", "first_seen": today - timedelta(days=22), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["InternetDB"], "tags": ["pua"]}},
        {"ioc_type": "IP", "ioc_value": "193.32.162.7", "source": "VirusTotal", "confidence": 88, "description": "High risk IP from mixed reporting.", "first_seen": today - timedelta(days=7), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["VirusTotal", "AbuseIPDB"], "ports": [80, 443], "vulnerabilities": ["CVE-2022-1388"]}},
        {"ioc_type": "IP", "ioc_value": "89.248.172.90", "source": "AlienVault OTX", "confidence": 85, "description": "Botnet command and control node.", "first_seen": today - timedelta(days=28), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["AlienVault OTX"], "ports": [53, 8080], "tags": ["c2"]}},
        {"ioc_type": "IP", "ioc_value": "5.188.86.123", "source": "AbuseIPDB", "confidence": 83, "description": "Proxy network node frequently reported.", "first_seen": today - timedelta(days=6), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["AbuseIPDB", "InternetDB"], "ports": [3128], "tags": ["proxy"]}},
        {"ioc_type": "Domain", "ioc_value": "support-desk-auth.com", "source": "VirusTotal", "confidence": 88, "description": "Fake support portal used in phishing campaigns.", "first_seen": today - timedelta(days=9), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["VirusTotal"], "tags": ["phishing"]}},
        {"ioc_type": "Domain", "ioc_value": "windows-security-patch.org", "source": "AbuseIPDB", "confidence": 82, "description": "Malvertising domain masquerading as a patch page.", "first_seen": today - timedelta(days=14), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["AbuseIPDB", "VirusTotal"], "tags": ["malvertising"]}},
        {"ioc_type": "Domain", "ioc_value": "invoice-sync-service.net", "source": "AlienVault OTX", "confidence": 80, "description": "Threat actor infrastructure for document lures.", "first_seen": today - timedelta(days=18), "last_seen": today - timedelta(days=4), "raw_metadata": {"sources": ["AlienVault OTX"], "tags": ["malware"]}},
        {"ioc_type": "URL", "ioc_value": "https://support-desk-auth.com/session", "source": "VirusTotal", "confidence": 91, "description": "Credential theft endpoint.", "first_seen": today - timedelta(days=11), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["VirusTotal"], "tags": ["phishing"]}},
        {"ioc_type": "URL", "ioc_value": "https://windows-security-patch.org/update", "source": "AbuseIPDB", "confidence": 85, "description": "Fake update download page.", "first_seen": today - timedelta(days=9), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["AbuseIPDB"], "tags": ["malware"]}},
        {"ioc_type": "URL", "ioc_value": "http://invoice-sync-service.net/doc.exe", "source": "AlienVault OTX", "confidence": 89, "description": "Executable download from malicious site.", "first_seen": today - timedelta(days=5), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["AlienVault OTX", "VirusTotal"], "tags": ["dropper"]}},
        {"ioc_type": "Hash", "ioc_value": "d41d8cd98f00b204e9800998ecf8427e", "source": "VirusTotal", "confidence": 71, "description": "Potentially suspicious empty-sample indicator.", "first_seen": today - timedelta(days=24), "last_seen": today - timedelta(days=8), "raw_metadata": {"sources": ["VirusTotal"], "tags": ["suspicious"]}},
        {"ioc_type": "Hash", "ioc_value": "8f14e45fceea167a5a36dedd4bea2543", "source": "AbuseIPDB", "confidence": 78, "description": "Suspicious hash from spam campaign.", "first_seen": today - timedelta(days=32), "last_seen": today - timedelta(days=10), "raw_metadata": {"sources": ["AbuseIPDB"], "tags": ["spam"]}},
        {"ioc_type": "Hash", "ioc_value": "1679091c5a880faf6fb5e6087eb1b2dc", "source": "AlienVault OTX", "confidence": 84, "description": "File hash associated with trojanized installer.", "first_seen": today - timedelta(days=30), "last_seen": today - timedelta(days=6), "raw_metadata": {"sources": ["AlienVault OTX", "InternetDB"], "tags": ["trojan"]}},
        {"ioc_type": "IP", "ioc_value": "141.95.0.67", "source": "InternetDB", "confidence": 79, "description": "Host with multiple open services and exposure.", "first_seen": today - timedelta(days=17), "last_seen": today - timedelta(days=2), "raw_metadata": {"sources": ["InternetDB"], "ports": [21, 80, 443], "vulnerabilities": ["CVE-2021-41773"]}},
        {"ioc_type": "IP", "ioc_value": "198.54.117.210", "source": "VirusTotal", "confidence": 92, "description": "Very high confidence malicious IP.", "first_seen": today - timedelta(days=15), "last_seen": today - timedelta(days=1), "raw_metadata": {"sources": ["VirusTotal", "AbuseIPDB", "InternetDB"], "ports": [25, 80, 443], "vulnerabilities": ["CVE-2023-38831", "CVE-2022-47966"]}},
    ]


def seed_iocs(db: Session) -> None:
    if db.query(IOC).count() >= 30:
        return

    records = _demo_ioc_records()
    for record in records:
        source_name = record["source"]
        source = db.query(ThreatSource).filter(ThreatSource.source_name == source_name).one_or_none()
        reliability = source.reliability_weight if source else 50.0
        corroborating_sources = len(record.get("raw_metadata", {}).get("sources", [source_name]))
        vulnerability_count = len(record.get("raw_metadata", {}).get("vulnerabilities", []))
        score = calculate_risk_score(record["confidence"], reliability, corroborating_sources, vulnerability_count)
        payload = {
            "ioc_type": record["ioc_type"],
            "ioc_value": record["ioc_value"],
            "source": source_name,
            "first_seen": record["first_seen"],
            "last_seen": record["last_seen"],
            "confidence": record["confidence"],
            "risk_score": score,
            "severity": determine_severity(score),
            "description": record["description"],
            "raw_metadata": record["raw_metadata"],
        }
        save_ioc(db, payload)


def seed_alerts(db: Session) -> None:
    if db.query(Alert).count() > 0:
        return

    target_iocs = db.query(IOC).filter(IOC.severity.in_(["High", "Critical"])).order_by(IOC.risk_score.desc()).all()
    for ioc in target_iocs[:18]:
        db.add(Alert(ioc_id=ioc.id, severity=ioc.severity, status="New", triggered_at=ioc.last_seen))
    db.commit()


def seed_all(db: Session) -> None:
    seed_users(db)
    seed_sources(db)
    seed_iocs(db)
    seed_alerts(db)
