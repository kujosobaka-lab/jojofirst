from dataclasses import dataclass

@dataclass
class CreationRule:
    regex: str | None = None
    # value_range: tuple[int, int] | None = None