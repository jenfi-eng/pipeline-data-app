import sys
from pathlib import Path

import papermill as pm
import pytest

from jenfi_pipeline_data_app import PipelineDataApp as Jenfi

from ._jupyter_faker import fake_jupyter_notebook
from ._pytest_all import run_before_and_after_tests  # noqa F401


def test_root_dir():
    assert Jenfi.ROOT_DIR == str(Path(__file__).parents[1])


def test_access_global_defined_var():
    assert Jenfi._test_access_global_var() == var_defined_globally


####################################################################################################################
var_defined_globally = "foo"


def test_set_global_defined_var():
    # sets the var to 'bar'
    Jenfi._test_set_global_var()

    assert var_defined_globally == "bar"


####################################################################################################################
var_do_not_change = "foo"


def test_set_parameters():
    with fake_jupyter_notebook(__name__):
        Jenfi.load_test_parameters(
            {"a_new_var": "new_val", "var_do_not_change": "should_not_change"}
        )

        assert a_new_var == "new_val"  # noqa F821
        assert (
            var_do_not_change == "foo"
        )  # Originally set to foo, attempted to change to 'should_not_change'


####################################################################################################################
def test_get_parameter_missing_module():
    sys.modules["__main__"] = None

    with pytest.raises(ModuleNotFoundError):
        Jenfi.get_parameter("mod_missing")


####################################################################################################################
var_do_not_change = "foo"


def test_get_parameter_works():
    with fake_jupyter_notebook(__name__):
        assert Jenfi.get_parameter("var_do_not_change") == var_do_not_change


####################################################################################################################


def test_no_result():
    assert Jenfi.load_result()["run_metadata"]["status"] == Jenfi.STATUS_NO_RESULT


def test_not_applicable():
    pm.execute_notebook(
        Path(__file__).parent / "./notebooks/exit_not_applicable.ipynb",
        Jenfi.tmp_filepath("notebook_output.ipynb"),
    )

    result = Jenfi.load_result()
    assert result["run_metadata"]["status"] == Jenfi.STATUS_NOT_APPLICABLE
    assert result["run_metadata"]["message"] == "exiting early exit_not_applicable"


def test_exit_insufficient_data():
    pm.execute_notebook(
        Path(__file__).parent / "./notebooks/exit_insufficient_data.ipynb",
        Jenfi.tmp_filepath("notebook_output.ipynb"),
    )

    result = Jenfi.load_result()
    assert result["run_metadata"]["status"] == Jenfi.STATUS_INSUFFICIENT_DATA
    assert result["run_metadata"]["message"] == "exiting early exit_insufficient_data"


def test_results_to_tmpfile():
    pm.execute_notebook(
        Path(__file__).parent / "./notebooks/write_result.ipynb",
        Jenfi.tmp_filepath("notebook_output.ipynb"),
    )

    result = Jenfi.load_result()
    assert result["run_metadata"]["status"] == Jenfi.STATUS_SUCCESS
    assert result["my_result_val"] == 3
    assert "message" not in result["run_metadata"]


def test_result_to_db():
    from jenfi_pipeline_data_app.db_models import (
        state_machine_model,
        state_machine_run_model,
    )

    pipeline_name = "TEST_PIPELINE"
    logical_step_name = "TEST_STEP_NAME"
    results = {"TEST_RESULT": "OK"}

    StateMachine = state_machine_model(Jenfi)
    sm = StateMachine(pipeline_name=pipeline_name)
    Jenfi.db.add(sm)
    Jenfi.db.commit()

    StateMachineRun = state_machine_run_model(Jenfi)
    sm_run = StateMachineRun(pipeline_state_machine_id=sm.id)
    Jenfi.db.add(sm_run)
    Jenfi.db.commit()

    sm_run.result_to_db(logical_step_name, sm_run.id, results)

    assert sm_run.result[logical_step_name] == results


def test_notebook_not_found_s3():
    Jenfi.notebook_not_found_s3()
