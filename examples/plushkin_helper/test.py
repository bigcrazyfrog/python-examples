from pathlib import Path

import duplicate_scanner
import pytest
from _pytest.monkeypatch import MonkeyPatch
from entities import DuplicatesData, ScannerResponse
from plushkin import Plushkin
from pytest_lazyfixture import lazy_fixture


@pytest.fixture
def without_duplicate(tmp_path: Path) -> Path:
    """Fixture file system without duplicates."""
    folder = tmp_path / "path"
    folder.mkdir()

    file = folder / "file 1.txt"
    file.write_text("text")
    file = folder / "file 2.txt"
    file.write_text("other text")

    folder /= "dir"
    folder.mkdir()
    file = folder / "file 3.txt"
    file.write_text("some text")

    return folder


@pytest.fixture
def two_duplicates(tmp_path: Path) -> Path:
    """Fixture file system with two duplicates."""
    folder = tmp_path / "path"
    folder.mkdir()

    file = folder / "file 1.txt"
    file.write_text("same text")
    file = folder / "file 2.txt"
    file.write_text("same text")

    folder /= "empty dir"
    folder.mkdir()

    folder = tmp_path / "path" / "dir"
    folder.mkdir()
    file = folder / "file 1.txt"
    file.write_text("same file name")

    return folder


def test_get_file_hash(tmp_path: Path) -> None:
    """Test get file hash function."""
    file = tmp_path / "file 1.txt"
    file.write_text("same text")
    first_hash = duplicate_scanner.get_file_hash(file)

    file = tmp_path / "file 2.txt"
    file.write_text("same text")
    second_hash = duplicate_scanner.get_file_hash(file)

    file = tmp_path / "file 2.txt"
    file.write_text("other text")
    third_hash = duplicate_scanner.get_file_hash(file)

    assert first_hash == second_hash
    assert third_hash != first_hash
    assert third_hash != second_hash


@pytest.mark.parametrize(
    ["file_system", "expected"],
    [
        [
            lazy_fixture("without_duplicate"),
            ScannerResponse(
                path_to_dir="path",
                files_scanned=3,
                folders_scanned=3,
                duplicates_found=0,
                duplicates=[],
            ),
        ],
        [
            lazy_fixture("two_duplicates"),
            ScannerResponse(
                path_to_dir="path",
                files_scanned=3,
                folders_scanned=4,
                duplicates_found=1,
                duplicates=[DuplicatesData(size=9)],
            ),
        ],
    ],
)
def test_scan_directory(
    tmp_path: Path,
    file_system: Path,
    expected: ScannerResponse,
) -> None:
    """Test scanning directory."""
    response = duplicate_scanner.scan_dir(tmp_path)

    assert response.files_scanned == expected.files_scanned
    assert response.folders_scanned == expected.folders_scanned
    assert response.duplicates_found == expected.duplicates_found

    for dupl, expected_dupl in zip(response.duplicates, expected.duplicates):
        assert dupl.size == expected_dupl.size


def test_scan_directory_with_removing(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    two_duplicates: Path,
) -> None:
    """Test scanning directory with removing."""
    expected = ScannerResponse(
        path_to_dir=tmp_path,
        files_scanned=2,
        folders_scanned=4,
        duplicates_found=0,
        duplicates=[],
    )
    monkeypatch.setattr(
        "plushkin.Plushkin._get_valid_user_input",
        lambda *args, **kwargs: 1,
    )
    monkeypatch.setattr(
        "builtins.print",
        lambda *args, **kwargs: None,
    )

    plushkin = Plushkin()
    plushkin.scan_with_removing(tmp_path)

    response = duplicate_scanner.scan_dir(tmp_path)
    assert response == expected
