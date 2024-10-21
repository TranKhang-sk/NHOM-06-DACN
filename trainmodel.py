import face_recognition
import os
import conndb
import pickle

# Kết nối cơ sở dữ liệu
conn = conndb.conndb()

# Truy xuất tất cả ảnh trong cơ sở dữ liệu
strsql = "SELECT MaSinhVien, Avatar FROM sinh_vien"
students = conn.queryResult(strsql)

known_face_encodings = []
known_face_ids = []

for student in students:
    avatar_path = f"./img/avatar/{student[1]}"
    if os.path.exists(avatar_path):
        # Tải ảnh và mã hóa
        image = face_recognition.load_image_file(avatar_path)
        encoding = face_recognition.face_encodings(image)
        
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_ids.append(student[0])  # Lưu mã sinh viên tương ứng

# Lưu các encoding vào file để sử dụng sau này
import pickle

with open('face_encodings.pkl', 'wb') as f:
    pickle.dump((known_face_encodings, known_face_ids), f)
