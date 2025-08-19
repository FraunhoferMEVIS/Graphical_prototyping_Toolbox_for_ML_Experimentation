"""
Reads dotenv once and provide all required settings for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


projects_folder = os.getenv("PROJECTS_FOLDER")
api_version = os.getenv("API_VERSION")
sandbox_api = os.getenv("SANDBOX_API")
unit_test_mode = os.getenv("UNIT_TEST_MODE")
root_path = os.getenv("ROOT_PATH", "")
