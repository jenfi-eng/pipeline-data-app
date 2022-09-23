from jenfi_pipeline_data_app import __version__, PipelineDataApp as Jenfi
from pathlib import Path
import sys
import pytest

from ._jupyter_faker import fake_jupyter_notebook


def test_root_dir():
    assert Jenfi.ROOT_DIR == str(Path(__file__).parents[1])


def test_access_global_defined_var():
    assert Jenfi._test_access_global_var() == var_defined_globally


########################################################################################################################################
var_defined_globally = "foo"


def test_set_global_defined_var():
    # sets the var to 'bar'
    Jenfi._test_set_global_var()

    assert var_defined_globally == "bar"


########################################################################################################################################
var_do_not_change = "foo"


def test_set_parameters():
    with fake_jupyter_notebook(__name__):
        Jenfi.load_test_parameters(
            {"a_new_var": "new_val", "var_do_not_change": "should_not_change"}
        )

        assert a_new_var == "new_val"
        assert (
            var_do_not_change == "foo"
        )  # Originally set to foo, attempted to change to 'should_not_change'


########################################################################################################################################
def test_get_parameter_missing_module():
    sys.modules["__main__"] = None

    with pytest.raises(ModuleNotFoundError):
        Jenfi.get_parameter("mod_missing")


########################################################################################################################################
var_do_not_change = "foo"


def test_get_parameter_works():
    with fake_jupyter_notebook(__name__):
        assert Jenfi.get_parameter("var_do_not_change") == var_do_not_change
