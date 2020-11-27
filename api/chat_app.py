"""This file is the entrypoint for the application."""


import os
from app import create_app


app = create_app(os.environ.get("FLASK_CONFIG", "development"))




if __name__ == "__main__":
    app.run(debug=True)
