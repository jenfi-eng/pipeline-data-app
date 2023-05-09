__version__ = "0.3.14"

# from ._pdoc import __pdoc__
from .app import Application

PipelineDataApp = Application()

PipelineDataApp.boot()

print()
print()
print(f"Welcome to the Jenfi Data App! v{__version__}")
print("https://jenfi-eng.github.io/pipeline-data-app")
print(
    "------------------------------------------------------------------------------------"
)
print()
print("!!REQUIRED!! variables in `parameters` tagged cell.")
print()
print("logical_step_name        - ex:   logical_step_name = 'sg_first_payment_default'")
print("state_machine_run_id     - ex:   state_machine_run_id = 5")
print(
    "------------------------------------------------------------------------------------"
)
print()
print()
