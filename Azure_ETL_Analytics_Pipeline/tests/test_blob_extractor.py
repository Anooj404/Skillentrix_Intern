import pytest
from azure.core.exceptions import ResourceNotFoundError

from etl.blob_extractor import extract_from_blob


def test_missing_blob_file():
    """Ensure a missing Azure Blob source is handled as an error."""

    with pytest.raises(ResourceNotFoundError):
        extract_from_blob("file_that_does_not_exist.csv")