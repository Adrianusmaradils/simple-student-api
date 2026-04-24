from flask import Blueprint, request, jsonify
from .models import db, Student

main = Blueprint('main', __name__)

# 1. READ ALL: Ambil Semua Data Mahasiswa
@main.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

# 2. CREATE: Tambah Mahasiswa Baru
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

# 3. READ ONE: Cari Mahasiswa berdasarkan NIM
@main.route('/students/<nim>', methods=['GET'])
def get_student_by_nim(nim):
    student = Student.query.filter_by(nim=nim).first()
    if student:
        return jsonify(student.to_dict()), 200
    return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404

# 4. UPDATE: Ubah Data Mahasiswa berdasarkan NIM
@main.route('/students/<nim>', methods=['PUT'])
def update_student(nim):
    student = Student.query.filter_by(nim=nim).first()
    if not student:
        return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404
    
    data = request.get_json()
    
    # Update field hanya jika datanya dikirim di JSON
    if 'nama' in data:
        student.nama = data['nama']
    if 'prodi' in data:
        student.prodi = data['prodi']
        
    try:
        db.session.commit()
        return jsonify({
            "message": "Data berhasil diperbarui", 
            "data": student.to_dict()
        }), 200
    except:
        db.session.rollback()
        return jsonify({"error": "Terjadi kesalahan saat memperbarui data"}), 500

# 5. DELETE: Hapus Mahasiswa berdasarkan NIM
@main.route('/students/<nim>', methods=['DELETE'])
def delete_student(nim):
    student = Student.query.filter_by(nim=nim).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Mahasiswa dengan NIM {nim} berhasil dihapus"}), 200
    return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404