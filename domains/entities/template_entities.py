from dataclasses import dataclass

@dataclass
class TemplateTitle:
    id: str
    title: dict[str, str]