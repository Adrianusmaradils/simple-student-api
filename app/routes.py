from flask import Blueprint, request, jsonify
from .models import db, Student

main = Blueprint('main', __name__)

@main.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

@main.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(nama=data['nama'], nim=data['nim'], prodi=data.get('prodi', 'Informatika'))
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Berhasil!"}), 201