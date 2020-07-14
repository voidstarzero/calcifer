import importlib
import app

# Setup dynamic imports to be absolute when run as a command
app.import_module = lambda relative_name: importlib.import_module(relative_name[1:])

def main():
    app.run('sample.cfg')

main()