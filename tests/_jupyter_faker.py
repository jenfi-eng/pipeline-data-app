import contextlib
import sys


@contextlib.contextmanager
def fake_jupyter_notebook(mod_name):
    """Make the current module look like a jupyter notebook"""

    sys.modules["__main__"] = sys.modules[mod_name]

    yield

    sys.modules["__main__"] = None
