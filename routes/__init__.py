from flask_openapi3 import Tag
from flask import redirect
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS

info = Info(title="TFT API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags
home_tag = Tag(name="Docs",
               description="Doc selection: Swagger, Redoc or ReDoc")


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi, screen that allows choosing the documentation style.
    """
    return redirect('/openapi')
