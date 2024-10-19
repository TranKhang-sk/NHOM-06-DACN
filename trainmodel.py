import os
import face_recognition
import numpy as np
import conndb

def train_model():
    # Kết nối đến cơ sở dữ liệu
    conn = conndb.conndb()
    
    # Truy vấn tất cả sinh viên và ảnh của họ từ cơ sở dữ liệu
    strsql = "SELECT MaSinhVien, Avatar FROM sinh_vien"
    students = conn.queryResult(strsql)

    known_face_encodings = []
    known_face_names = []

    for student in students:
        avatar_path = f"./img/avatar/{student[1]}"
        # Tải ảnh và mã hóa khuôn mặt
        image = face_recognition.load_image_file(avatar_path)
        encoding = face_recognition.face_encodings(image)

        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(student[0])  # Giả sử MaSinhVien là tên

    return known_face_encodings, known_face_names

if __name__ == "__main__":
    encodings, names = train_model()
    print("Mô hình đã được huấn luyện thành công!")