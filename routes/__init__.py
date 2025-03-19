from routes.meal import register_meal_routes
from routes.activity_level import register_activity_level_routes
from routes.personal_info import register_personal_info_routes
from routes.food import register_food_routes
from routes.goal import register_goal_routes
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

# Home route


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi, screen that allows choosing the documentation style.
    """
    return redirect('/openapi')


def register_routes(app):
    """Register all routes."""
    register_food_routes(app)
    register_meal_routes(app)
    register_goal_routes(app)
    register_activity_level_routes(app)
    register_personal_info_routes(app)


register_routes(app)
