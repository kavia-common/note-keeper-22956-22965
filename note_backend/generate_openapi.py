import json
import os
from app import app
from flask_smorest import Api

with app.app_context():
    # Build a fresh Api spec from registered blueprints.
    # Prefer existing Api instance if already attached.
    api = app.extensions.get("flask-smorest", None)
    if not api or not isinstance(api, Api):
        api = Api(app)
    openapi_spec = api.spec.to_dict()

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
