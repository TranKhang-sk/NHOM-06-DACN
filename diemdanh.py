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

class diemdanh(QtWidgets.QMainWindow):  # Đổi tên lớp và thừa kế đúng kiểu
    
    
    def __init__(self, parent=None):  # Thêm tham số parent
        super().__init__(parent)  # Gọi hàm khởi tạo của QWidget đúng cách
        uic.loadUi('diemdanh.ui', self)
        self.cap = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        # Kết nối Camera
        self.btnMoCamera.clicked.connect(self.open_camera)
        self.btnDongCamera.clicked.connect(self.close_camera)
        self.btnDiemDanh.clicked.connect(self.diemDanh)
        self.btnThoat.clicked.connect(self.confirm_exit)
        
        # Khởi tạo hàm kết nối cơ sở dữ liệu
        self.conn=conndb.conndb()
        
        #Biến dừng camera
        self.cap=None
    
    def open_camera (self):
        self.cap = cv2.VideoCapture(0) #Mở camera
        if not self.cap.isOpened():
            print ("Không thể mở camera")
            return
        self.timer.start(80) #Cập nhật khung mình mỗi 1ms
        self.btnMoCamera.setEnabled(False)
        self.btnDongCamera.setEnabled(True)
                                      
    def close_camera(self):       
        if self.cap is not None:  # Kiểm tra xem camera đã được mở hay chưa
            self.timer.stop()  # Dừng timer trước
            self.cap.release()  # Giải phóng camera
            self.cap = None  # Đặt cap về None sau khi giải phóng
            self.image_label.clear()  # Xóa nội dung label để tránh hiển thị khung hình cũ
            self.btnMoCamera.setEnabled(True)  # Bật lại nút "Mở Camera"
            self.btnDongCamera.setEnabled(False)  # Vô hiệu hóa nút "Đóng Camera"
           
    def recognizeFace(self, frame):
        #chuyển ảnh từ camera sang RGB
        rgb_frame =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Nhận diện khuôn mặt
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        #Truy xuất tất cả ảnh trong cơ sở dữ liệu
        strsql = "SELECT MaSinhVien, Avatar FROM sinh_vien"
        students = self.conn.queryResult(strsql)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            for student in students:
                # So sánh khuôn mặt
                avatar_path = f"./img/avatar/{student[1]}"
                known_image = face_recognition.load_image_file(avatar_path)
                known_encoding = face_recognition.face_encodings(known_image)[0]

                # So sánh khuôn mặt từ camera với ảnh từ database
                matches = face_recognition.compare_faces([known_encoding], face_encoding)
                if True in matches:
                    # Nếu trùng khớp, hiển thị thông tin sinh viên
                    self.displayStudentInfo(student[0])
                    return      
    def displayStudentInfo(self, MaSinhVien):
        strsql = f"SELECT * FROM sinh_vien WHERE MaSinhVien = '{MaSinhVien}'"
        student = self.conn.queryResult(strsql)[0]

        self.lblMaSinhVien.setText(student[0])
        self.lblTenSinhVien.setText(student[1])
        self.lblLop.setText(student[2])
        self.lblGioiTinh.setText(student[3])
        avatar_path = f"./img/avatar/{student[4]}"
        pixmap = QPixmap(avatar_path)
        self.lblAvatar.setPixmap(pixmap) 
    
    def diemDanh(self):
        # Ghi lại thời gian điểm danh
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        self.txtNgayHienTai.setText(current_date)
        self.txtThoiGianHienTai.setText(current_time)

        QMessageBox.information(self, "Thông báo", "Đã điểm danh thành công!")             

    def closeCamera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
               
    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()  # Đọc khung hình từ camera
            if ret:
                
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                # Vẽ hình chữ nhật quanh khuôn mặt
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Chuyển đổi khung hình từ BGR sang RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(q_img))  # Hiển thị trên image_label
        else:
            self.timer.stop()
            
    def setupUi(self, diemdanh):
        diemdanh.setObjectName("diemdanh")
        diemdanh.resize(1001, 697)
        self.centralwidget = QtWidgets.QWidget(parent=diemdanh)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-1, 0, 1001, 51))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(89, 89, 89);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.windowSinhVien = QtWidgets.QPushButton(parent=self.frame)
        self.windowSinhVien.setGeometry(QtCore.QRect(0, 0, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.windowSinhVien.setFont(font)
        self.windowSinhVien.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.windowSinhVien.setAutoFillBackground(False)
        self.windowSinhVien.setStyleSheet("color: rgb(255, 255, 255);")
        self.windowSinhVien.setFlat(True)
        self.windowSinhVien.setObjectName("windowSinhVien")
        self.windowDiemDanh = QtWidgets.QPushButton(parent=self.frame)
        self.windowDiemDanh.setGeometry(QtCore.QRect(130, 0, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.windowDiemDanh.setFont(font)
        self.windowDiemDanh.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.windowDiemDanh.setAutoFillBackground(False)
        self.windowDiemDanh.setStyleSheet("color: rgb(255, 255, 255);")
        self.windowDiemDanh.setFlat(True)
        self.windowDiemDanh.setObjectName("windowDiemDanh")
        self.btnThoat = QtWidgets.QPushButton(parent=self.frame)
        self.btnThoat.setGeometry(QtCore.QRect(850, 0, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.btnThoat.setFont(font)
        self.btnThoat.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnThoat.setAutoFillBackground(False)
        self.btnThoat.setStyleSheet("color: rgb(255, 255, 255);")
        self.btnThoat.setFlat(True)
        self.btnThoat.setObjectName("btnThoat")
        self.windowLopHocPhan = QtWidgets.QPushButton(parent=self.frame)
        self.windowLopHocPhan.setGeometry(QtCore.QRect(280, 0, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.windowLopHocPhan.setFont(font)
        self.windowLopHocPhan.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.windowLopHocPhan.setAutoFillBackground(False)
        self.windowLopHocPhan.setStyleSheet("color: rgb(255, 255, 255);")
        self.windowLopHocPhan.setFlat(True)
        self.windowLopHocPhan.setObjectName("windowLopHocPhan")
        self.windowTinhDiem = QtWidgets.QPushButton(parent=self.frame)
        self.windowTinhDiem.setGeometry(QtCore.QRect(450, 0, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.windowTinhDiem.setFont(font)
        self.windowTinhDiem.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.windowTinhDiem.setAutoFillBackground(False)
        self.windowTinhDiem.setStyleSheet("color: rgb(255, 255, 255);")
        self.windowTinhDiem.setFlat(True)
        self.windowTinhDiem.setObjectName("windowTinhDiem")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 590, 641, 91))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnDiemDanh = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.btnDiemDanh.setEnabled(False)
        self.btnDiemDanh.setGeometry(QtCore.QRect(230, 20, 191, 51))
        self.btnDiemDanh.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnDiemDanh.setObjectName("btnDiemDanh")
        self.txtNgayHienTai = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.txtNgayHienTai.setEnabled(False)
        self.txtNgayHienTai.setGeometry(QtCore.QRect(450, 10, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.txtNgayHienTai.setFont(font)
        self.txtNgayHienTai.setText("")
        self.txtNgayHienTai.setReadOnly(True)
        self.txtNgayHienTai.setObjectName("txtNgayHienTai")
        self.txtThoiGianHienTai = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.txtThoiGianHienTai.setEnabled(False)
        self.txtThoiGianHienTai.setGeometry(QtCore.QRect(450, 50, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtThoiGianHienTai.setFont(font)
        self.txtThoiGianHienTai.setReadOnly(True)
        self.txtThoiGianHienTai.setObjectName("txtThoiGianHienTai")
        self.btnMoCamera = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.btnMoCamera.setGeometry(QtCore.QRect(20, 10, 181, 31))
        self.btnMoCamera.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnMoCamera.setObjectName("btnMoCamera")
        self.btnDongCamera = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.btnDongCamera.setEnabled(False)
        self.btnDongCamera.setGeometry(QtCore.QRect(20, 50, 181, 31))
        self.btnDongCamera.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnDongCamera.setObjectName("btnDongCamera")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(690, 390, 311, 301))
        self.groupBox_4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(10, 30, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(10, 180, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(130, 30, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(130, 80, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(130, 130, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(130, 180, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        diemdanh.setCentralWidget(self.centralwidget)

        self.retranslateUi(diemdanh)
        QtCore.QMetaObject.connectSlotsByName(diemdanh)

    def retranslateUi(self, diemdanh):
        _translate = QtCore.QCoreApplication.translate
        diemdanh.setWindowTitle(_translate("diemdanh", "Điểm Danh"))
        self.windowSinhVien.setText(_translate("diemdanh", "Sinh Viên"))
        self.windowDiemDanh.setText(_translate("diemdanh", "Điểm Danh"))
        self.btnThoat.setText(_translate("diemdanh", "Thoát"))
        self.windowLopHocPhan.setText(_translate("diemdanh", "Lớp Học Phần"))
        self.windowTinhDiem.setText(_translate("diemdanh", "Tính Điểm"))
        self.btnDiemDanh.setText(_translate("diemdanh", "Điểm Danh"))
        self.btnMoCamera.setText(_translate("diemdanh", "Mở Camera"))
        self.btnDongCamera.setText(_translate("diemdanh", "Đóng Camera"))
        self.groupBox_4.setTitle(_translate("diemdanh", "Thông Tin"))
        self.label.setText(_translate("diemdanh", "Mã Sinh Viên:"))
        self.label_3.setText(_translate("diemdanh", "Họ Tên:"))
        self.label_4.setText(_translate("diemdanh", "Lớp:"))
        self.label_5.setText(_translate("diemdanh", "Địa Chỉ:"))
        self.label_2.setText(_translate("diemdanh", "None"))
        self.label_6.setText(_translate("diemdanh", "None"))
        self.label_7.setText(_translate("diemdanh", "None"))
        self.label_8.setText(_translate("diemdanh", "None"))
        
    def confirm_exit(self):
        reply = QMessageBox.question(self, 'xác nhận',"Bạn có chắc chắn muốn thoát ?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QtWidgets.QApplication.quit()
        else:
            pass
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = diemdanh()  # Tạo một đối tượng của lớp diemdanh
    main_window.show()  # Hiển thị cửa sổ chính
    sys.exit(app.exec())
