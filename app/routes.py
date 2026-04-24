from flask import Blueprint, request, jsonify
from .models import db, Student

main = Blueprint('main', __name__)

# 1. Ambil Semua Data
@main.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

# 2. Tambah Mahasiswa
@main.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not data.get('nama') or not data.get('nim'):
        return jsonify({"error": "Data tidak lengkap"}), 400
        
    try:
        new_student = Student(
            nama=data['nama'],
            nim=data['nim'],
            prodi=data.get('prodi', 'Informatika')
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Berhasil!", "data": new_student.to_dict()}), 201
    except:
        db.session.rollback()
        return jsonify({"error": "NIM sudah ada"}), 400

# 3. Cari Mahasiswa berdasarkan NIM
@main.route('/students/<nim>', methods=['GET'])
def get_student_by_nim(nim):
    student = Student.query.filter_by(nim=nim).first()
    if student:
        return jsonify(student.to_dict()), 200
    return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404

# 4. Hapus Mahasiswa berdasarkan NIM
@main.route('/students/<nim>', methods=['DELETE'])
def delete_student(nim):
    student = Student.query.filter_by(nim=nim).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Mahasiswa dengan NIM {nim} berhasil dihapus"}), 200
    return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404