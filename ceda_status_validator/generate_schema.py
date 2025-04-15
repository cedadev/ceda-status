import json

from .model import StatusPage

schema = StatusPage.model_json_schema()

with open("generated_schema.json", "w") as out_file:
    json.dump(schema, out_file, indent=2)
