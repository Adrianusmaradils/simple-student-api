import os
from flask import Flask
from app.models import db
from app.routes import main

app = Flask(__name__)

# Konfigurasi Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Buat folder data dan tabel otomatis
with app.app_context():
    if not os.path.exists('data'):
        os.makedirs('data')
    db.create_all()

app.register_blueprint(main)

if __name__ == '__main__':
    print("\n--- SERVER AKTIF DI http://127.0.0.1:5000/students ---\n")
    app.run(debug=True)