from jenfi_pipeline_data_app import __version__, PipelineDataApp as Jenfi
from pathlib import Path

def test_root_dir():
    assert Jenfi.ROOT_DIR == str(Path(__file__).parents[1])

def test_access_global_defined_var():
    assert Jenfi.__test_access_global_var__() == var_defined_globally

########################################################################################################################################
var_defined_globally = 'foo'
def test_set_global_defined_var():
    # sets the var to 'bar'
    Jenfi.__test_set_global_var__()

    assert var_defined_globally == 'bar'

########################################################################################################################################
var_do_not_change = 'foo'
def test_set_parameters():
    Jenfi.load_test_parameters({
        'a_new_var': 'new_val',
        'var_do_not_change': 'should_not_change'
    })

    assert a_new_var == 'new_val'
    assert var_do_not_change == 'foo' # Originally set to foo, attempted to change to 'should_not_change'