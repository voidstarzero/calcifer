import importlib
from . import app

# Setup dynamic imports relative to this root module
app.import_module = lambda relative_name: importlib.import_module(relative_name, __name__)