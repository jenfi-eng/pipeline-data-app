# Exit program
import sys


def exit_not_applicable(self, message: str) -> None:
    """Exits the program early and puts status `not_applicable`"""

    result_with_metadata = self._add_run_metadata(
        self.STATUS_NOT_APPLICABLE, message=message
    )

    self._write_result(result_with_metadata)

    sys.exit(0)


def exit_insufficient_data(self, message: str) -> None:
    """Exits the program early and puts status `insufficient_data`"""
    # Write output

    result_with_metadata = self._add_run_metadata(
        self.STATUS_INSUFFICIENT_DATA, message=message
    )

    self._write_result(result_with_metadata)

    sys.exit(0)
