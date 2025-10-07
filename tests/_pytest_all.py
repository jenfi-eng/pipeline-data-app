import pytest
from sqlalchemy import text

from jenfi_pipeline_data_app import PipelineDataApp as Jenfi
from jenfi_pipeline_data_app import __version__  # noqa E401


# This function wraps every test and clears the tables used below.
# I'm not a fan of this but it's because we can't prevent commits in a nice way? At least I'm not aware of it.
@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    from jenfi_pipeline_data_app.db_models import (
        state_machine_run_model,
    )

    StateMachineRun = state_machine_run_model(Jenfi)
    used_objs = [StateMachineRun]

    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    _truncate_db(used_objs)

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    _truncate_db(used_objs)


def _truncate_db(objs):
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    engine = Jenfi.db_engine

    con = engine.connect()
    trans = con.begin()
    for obj in objs:
        con.execute(text(f'ALTER TABLE "{obj.__table__.name}" DISABLE TRIGGER ALL;'))
        con.execute(obj.__table__.delete())
        con.execute(text(f'ALTER TABLE "{obj.__table__.name}" ENABLE TRIGGER ALL;'))
    trans.commit()
