from jenfi_pipeline_data_app import __version__, PipelineDataApp
from pathlib import Path


def test_version():
    assert __version__ == "0.1.0"

def test_root_dir():
    assert PipelineDataApp.ROOT_DIR == str(Path(__file__).parents[1])