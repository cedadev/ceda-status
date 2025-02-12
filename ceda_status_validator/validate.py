import sys

from pydantic import ValidationError

from .model import StatusPage

with open("status.json", "r") as status_file:
    status_page = status_file.read()

# using a try/except block so that the traceback doesn't clog up pre-commit/CI output
try:
    StatusPage.model_validate_json(status_page)
except ValidationError as err:
    print(err)
    sys.exit(1)
