from model import StatusPage
from pydantic import ValidationError

with open("status.json", "r") as status_file:
    status_page = status_file.read()

try:
    StatusPage.model_validate_json(status_page)
except ValidationError as err:
    print(err)
    exit(1)