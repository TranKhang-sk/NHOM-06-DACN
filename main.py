from PyQt6 import QtWidgets
import sys
from sinhvien import SinhVien  
from diemdanh import diemdanh
from lophocphan import lophocphan 

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setWindowTitle("Ứng dụng quản lý sinh viên")
        self.setGeometry(100, 100, 350, 250)  # Thay đổi kích thước để phù hợp với thêm nút

        self.widget = QtWidgets.QStackedWidget()
        
        # Tạo nút để mở giao diện sinh viên
        self.btnSinhVien = QtWidgets.QPushButton("Quản lý sinh viên", self)
        self.btnSinhVien.setGeometry(50, 50, 200, 40)
        self.btnSinhVien.clicked.connect(self.open_sinhvien)

        # Tạo nút để mở giao diện điểm danh
        self.btnDiemDanh = QtWidgets.QPushButton("Điểm danh sinh viên", self)
        self.btnDiemDanh.setGeometry(50, 100, 200, 40)
        self.btnDiemDanh.clicked.connect(self.open_diemdanh)

        # Tạo nút để mở giao diện lớp học phần
        self.btnLopHocPhan = QtWidgets.QPushButton("Xem lớp học phần", self)
        self.btnLopHocPhan.setGeometry(50, 150, 200, 40)  # Thay đổi tọa độ y cho nút mới
        self.btnLopHocPhan.clicked.connect(self.open_lophocphan)

    def open_sinhvien(self):
        try:
            self.sinhvien_window = SinhVien(self.widget)  # Mở giao diện quản lý sinh viên
            self.sinhvien_window.show()
        except Exception as e:
            print(f"Error opening sinhvien: {e}")

    def open_diemdanh(self):
        try:
            self.diemdanh_window = diemdanh()  # Mở giao diện điểm danh
            self.diemdanh_window.show()
        except Exception as e:
            print(f"Error opening diemdanh: {e}")

    def open_lophocphan(self):
        try:
            self.lop_hoc_phan_window = lophocphan()  # Mở giao diện lớp học phần
            self.lop_hoc_phan_window.show()
        except Exception as e:
            print(f"Error opening lophocphan: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
