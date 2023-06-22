from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass(kw_only=True, frozen=True)
class File:
    """Dataclass for file."""
    path: Path
    created_at: date | None = None


@dataclass(kw_only=True)
class DuplicatesData:
    """Dataclass contains duplicates of files."""
    files: list[File] = field(default_factory=list)
    size: int = 0


@dataclass(kw_only=True)
class ScannerResponse:
    """Scanner result response."""
    path_to_dir: Path

    files_scanned: int = 0
    folders_scanned: int = 0
    duplicates_found: int = 0

    duplicates: list[DuplicatesData] = field(default_factory=list)
