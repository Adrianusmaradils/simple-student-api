from flask_sqlalchemy import SQLAlchemy

# Variabel ini yang dicari oleh app.py
db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    prodi = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "nim": self.nim,
            "prodi": self.prodi
        }