import enum
from dataclasses import dataclass
from typing import Any


class FileType(enum.Enum):
    UNKNOWN = 0
    FINANCE = 1
    INFO = 2


@dataclass
class FileSummary:
    id: Any
    type: FileType
    summary: str
