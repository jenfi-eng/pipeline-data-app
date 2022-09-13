from jenfi_pipeline_data_app import __version__, PipelineDataApp as Jenfi
from pathlib import Path

var_defined_globally = 'test_val'

def test_version():
    assert __version__ == "0.1.0"

def test_root_dir():
    assert Jenfi.ROOT_DIR == str(Path(__file__).parents[1])

def test_access_global_defined_var():
    assert Jenfi.__test_access_global_var__() == var_defined_globally

# sets the var to 'bar'
def test_set_global_defined_var():
    Jenfi.__test_set_global_var__()

    assert var_defined_globally == 'bar'