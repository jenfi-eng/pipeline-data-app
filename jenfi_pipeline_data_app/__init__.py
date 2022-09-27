__version__ = "0.3.0"

from ._pdoc import __pdoc__

from .app import Application

PipelineDataApp = Application()

PipelineDataApp.boot()
