from app.server import app
from app.db import db
from workers.routers import worker_model

app.register_blueprint(worker_model, url_prefix='/workers')
db.init_app(app=app)

with app.app_context():
    # db.drop_all()
    db.create_all()