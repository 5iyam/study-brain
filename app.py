from flask import Flask

from services.metadata_service import migrate_topics_to_metadata

from routes.home import home_bp
from routes.upload import upload_bp
from routes.search import search_bp
from routes.topics import topics_bp
from routes.universal import universal_bp
from routes.time import time_bp
from routes.note import note_bp


app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(search_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(universal_bp)
app.register_blueprint(time_bp)
app.register_blueprint(note_bp)


if __name__ == "__main__":
    migrate_topics_to_metadata()
    app.run(debug=True)