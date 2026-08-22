from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    secret_key: str = os.getenv("SECRET_KEY", "YO6C$o$VUlV8Hq@cTmtPCP0IPlOvREVJn%pw")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./cyber_threat_intel.db")
    virus_total_api_key: str = os.getenv("VIRUSTOTAL_API_KEY", "")
    abuse_ipdb_api_key: str = os.getenv("ABUSEIPDB_API_KEY", "")
    otx_api_key: str = os.getenv("OTX_API_KEY", "")
    app_name: str = "Cyber Threat Intelligence Dashboard"


settings = Settings()
