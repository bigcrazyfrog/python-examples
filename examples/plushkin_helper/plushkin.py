import argparse
from pathlib import Path

import duplicate_scanner
from entities import DuplicatesData, ScannerResponse


class Plushkin:
    """Command line parser for scanner module.

    Attributes:
        parse: Parse argument from command line.

    """

    SEP_LINE = "-" * 57
    CLEANING_STARTED = f"CLEANING started\n{SEP_LINE}"
    CLEANING_END = f"CLEANING finished\n{SEP_LINE}\n"
    INPUT_FOR_DELETE = (
        "Choose a file to keep by entering its number or press"
        "enter to skip it \n>>> "
    )
    FILE_WAS_KEPT = "File {} was kept"
    DELETING_REPORT = (
        "File removed: {removed_files}\n"
        "Errors: {errors}\n"
        "Size cleaned: {cleaned_size} bytes\n"
    )
    WRONG_INPUT = "Enter correct number."
    ERROR = "*--- ERROR ---*"

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
            prog="Plushkins Helper",
            description="Find duplications of files in your file system.",
        )
        self._parser.add_argument(
            "path",
            type=str,
            nargs="+",
            help="path to dir",
        )
        self._parser.add_argument(
            "-d",
            dest="accumulate",
            action="store_const",
            const=self.scan_with_removing,
            default=self.scan,
            help="searching with deleting",
        )

    def _print_general_info(self, scan_result: ScannerResponse) -> None:
        """Print general info from result of scanning."""
        print(
            f"Scan report for folder: {scan_result.path_to_dir}\n"
            f"Files scanned: {scan_result.files_scanned}\n"
            f"Folders scanned: {scan_result.folders_scanned}\n"
            f"Duplications found: {scan_result.duplicates_found}\n"
            f"{self.SEP_LINE}",
        )

    def _print_duplicates(self, duplicate: DuplicatesData) -> None:
        """Print info about duplicates from result of scanning."""
        print(f"Size: {duplicate.size} bytes\n")

        for file_index, file in enumerate(duplicate.files, start=1):
            print(
                f"[{file_index}]: {file.path}  "
                f"(Created: {file.created_at})\n",
                end="",
            )

    def _remove_duplicate(self, path: Path) -> bool:
        """Remove duplicate of file.

        True if file was remove, False in other.

        """
        try:
            path.unlink()
            print(self.FILE_WAS_KEPT.format(path))
            return True
        except OSError as error:
            print(self.ERROR)
            print(error)
            return False

    def _get_valid_user_input(self, max_number: int) -> str:
        """Get valid input from user, that index file to remove."""
        while user_input := input(self.INPUT_FOR_DELETE):
            try:
                if 0 < int(user_input) <= max_number:
                    break
            except ValueError:
                print(self.WRONG_INPUT)

        return user_input

    def scan_with_removing(self, path: Path) -> None:
        """Scan directory with deleting duplicates."""
        scan_result = duplicate_scanner.scan_dir(path)

        self._print_general_info(scan_result)
        print(self.CLEANING_STARTED)

        removed_files = 0
        errors = 0
        cleaned_size = 0

        for duplicate in scan_result.duplicates:
            self._print_duplicates(duplicate)

            max_number = len(duplicate.files)
            user_input = self._get_valid_user_input(max_number)

            if user_input == "":
                print(self.SEP_LINE)
                continue

            file_index = int(user_input) - 1
            path_to_file = duplicate.files[file_index].path

            if self._remove_duplicate(path_to_file):
                removed_files += 1
                cleaned_size += duplicate.size
            else:
                errors += 1

            print(self.SEP_LINE)

        print(self.CLEANING_END)
        print(self.DELETING_REPORT.format(
            removed_files=removed_files,
            errors=errors,
            cleaned_size=cleaned_size,
        ))

    def scan(self, path: Path) -> None:
        """Scan directory."""
        scan_result = duplicate_scanner.scan_dir(path)

        self._print_general_info(scan_result)
        for duplicate in scan_result.duplicates:
            self._print_duplicates(duplicate)
            print(self.SEP_LINE)

    def parse(self) -> None:
        """Parse attribute from command line."""
        args = self._parser.parse_args()

        path = Path(args.path[0])
        args.accumulate(path)


if __name__ == "__main__":
    plushkin = Plushkin()
    plushkin.parse()
