from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
import cv2
import face_recognition
import numpy as np
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
import conndb
import os

class diemdanh(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super(diemdanh, self).__init__(parent)
        uic.loadUi('diemdanh.ui', self)
        self.lblStatus = QtWidgets.QLabel(self)
        self.lblStatus.setGeometry(10, 10, 200, 30)

        self.cap = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        # Kết nối Camera
        self.btnMoCamera.clicked.connect(self.open_camera)
        self.btnDongCamera.clicked.connect(self.close_camera)
        self.btnDiemDanh.clicked.connect(self.diemDanh)
        self.btnThoat.clicked.connect(self.confirm_exit)
        
        # Kết nối đến cơ sở dữ liệu
        self.conn = conndb.conndb()

    def open_camera(self):
        self.cap = cv2.VideoCapture(0) 
        if not self.cap.isOpened():
            print("Không thể mở camera")
            return
        self.timer.start(80) 
        self.btnMoCamera.setEnabled(False)
        self.btnDongCamera.setEnabled(True)
                                       
    def close_camera(self):       
        if self.cap is not None:
            self.timer.stop()  
            self.cap.release()  
            self.cap = None  
            self.image_label.clear()  
            self.btnMoCamera.setEnabled(True)  
            self.btnDongCamera.setEnabled(False) 
           
    def recognizeFace(self, frame):
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            strsql = "SELECT MaSinhVien, Avatar FROM sinh_vien"
            students = self.conn.queryResult(strsql)

            if face_encodings:
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    for student in students:
                        avatar_path = f"./img/avatar/{student[1].decode('utf-8').strip('b\'')}"
                        if not os.path.exists(avatar_path):
                            print(f"Hình ảnh không tồn tại cho sinh viên {student[0]}")
                            continue

                        known_image = face_recognition.load_image_file(avatar_path)
                        known_encoding = face_recognition.face_encodings(known_image)[0]

                        matches = face_recognition.compare_faces([known_encoding], face_encoding)
                        if True in matches:
                            self.displayStudentInfo(student[0], avatar_path)  # Gọi hàm với avatar_path
                            return
            
        except Exception as e:
            print(f"An error occurred: {e}")
            self.lblStatus.setText("Lỗi trong quá trình nhận diện.")

    def displayStudentInfo(self, MaSinhVien, avatar_path):
        strsql = f"SELECT * FROM sinh_vien WHERE MaSinhVien = '{MaSinhVien}'"
        student = self.conn.queryResult(strsql)[0]

        self.lblMaSinhVien.setText(student[0])  
        self.lblTenSinhVien.setText(student[1])  
        self.lblGioiTinh.setText(student[3])     
    
        # Hiển thị khuôn mặt đã nhận diện
        if os.path.exists(avatar_path):
            pixmap = QPixmap(avatar_path)             
            self.lblAvatar.setPixmap(pixmap)          
        else:
            print(f"Hình ảnh không tồn tại cho sinh viên {student[0]}")
            self.lblAvatar.clear()  # Xóa hình ảnh nếu không tìm thấy

    def diemDanh(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        self.txtNgayHienTai.setText(current_date)
        self.txtThoiGianHienTai.setText(current_time)

        QMessageBox.information(self, "Thông báo", "Đã điểm danh thành công!")             

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()  
            if ret:
                self.lblStatus.setText("Đang nhận diện...")  
                
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                self.recognizeFace(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(q_img))  
            else:
                self.timer.stop()
        else:
            self.timer.stop()

    def confirm_exit(self):
        reply = QMessageBox.question(self, 'xác nhận', "Bạn có chắc chắn muốn thoát ?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QtWidgets.QApplication.quit()
        else:
            pass
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = diemdanh()
    main_window.show()
    sys.exit(app.exec())
