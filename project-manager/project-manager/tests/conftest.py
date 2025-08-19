import os
import sys

# add parent directory to sys path to import 'main' and 'data_preparation'.
# https://docs.python-guide.org/writing/structure/#test-suite
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../service"))
)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Set projects directory for tests before import any module in `service` that could
# overwrite the env variables
projects_dir = os.path.dirname(__file__) + os.path.sep + "tmp-projects"
os.environ["PROJECTS_FOLDER"] = projects_dir
