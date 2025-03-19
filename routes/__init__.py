from routes.meal import register_meal_routes
from routes.personal_info import register_personal_info_routes
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

# API Info
info = Info(
    title="TFT API",
    version="1.0.0",
    description="API for managing meals and foods"
)

# Initialize Flask app with OpenAPI
app = OpenAPI(__name__, info=info)
CORS(app)

# API Tags
home_tag = Tag(
    name="Docs",
    description="Documentation selection: Swagger, Redoc or ReDoc"
)

meal_tag = Tag(
    name="Meals",
    description="Operations for managing meals"
)

personal_info_tag = Tag(
    name="Personal Info",
    description="Operations for managing personal information"
)

# Home route


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi, screen that allows choosing the documentation style.
    """
    return redirect('/openapi')


# Register routes after app initialization
register_meal_routes(app)
register_personal_info_routes(app)
