from dataclasses import dataclass

@dataclass
class Session:
    access_token: str
    refresh_token: str