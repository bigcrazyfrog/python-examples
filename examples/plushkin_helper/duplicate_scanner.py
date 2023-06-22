import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from entities import DuplicatesData, File, ScannerResponse


def scan_dir(path: Path) -> ScannerResponse:
    """Provide to find duplicates in directory.

    It scan directory tree and find duplicated files. It use md5 hash
    algorithm for mark the same files faster.

    Args:
        path: Path to directories

    """
    hashed_files: dict[str, list[Path]] = defaultdict(list)

    response = _recursion_scan(
        path,
        ScannerResponse(path_to_dir=path),
        hashed_files,
    )

    for files in hashed_files.values():
        if len(files) <= 1:
            continue
        response.duplicates_found += len(files) - 1

        duplicates = DuplicatesData()
        duplicates.size = files[0].stat().st_size

        for file_path in files:
            ctime = file_path.stat().st_ctime
            created_at = datetime.fromtimestamp(ctime).date()
            file = File(path=file_path, created_at=created_at)
            duplicates.files.append(file)
        response.duplicates.append(duplicates)

    return response


def _recursion_scan(
    current_dir: Path,
    response: ScannerResponse,
    hashed_files: dict[str, list[Path]],
) -> ScannerResponse:
    """Recursive scanning directories."""
    response.folders_scanned += 1

    for path in current_dir.iterdir():
        if path.is_file():
            current_hash = get_file_hash(path)
            hashed_files[current_hash].append(path)

            response.files_scanned += 1
        else:
            response = _recursion_scan(
                path,
                response,
                hashed_files,
            )

    return response


def get_file_hash(path: Path, batch_size: int = 2**20) -> str:
    """Hash file by md5 hashing."""
    hashed_file = hashlib.md5()
    with open(path, "rb") as file:
        while buffer := file.read(batch_size):
            hashed_file.update(buffer)

    return hashed_file.hexdigest()
