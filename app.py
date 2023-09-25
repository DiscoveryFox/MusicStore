import flask
from models import db  # Import the SQLAlchemy db object
from models import User, Orchestra, OrchestraMembership

app = flask.Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = r"sqlite:///C:\Users\Flinn\OneDrive\Dokumente\MusicStore\database.db"

db.init_app(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    app.run()
