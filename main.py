from PyQt6 import QtWidgets
import sys
from sinhvien import sinhvien  
from diemdanh import diemdanh  
from lophocphan import lophocphan

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget()
    # Khởi tạo giao diện sinh viên
    sinhvien_window = sinhvien(main_widget)
    sinhvien_window.show()  # Hiển thị cửa sổ Sinh Viên

    # Khởi tạo giao diện điểm danh
    diemdanh_window = diemdanh(main_widget)
    diemdanh_window.show()  # Hiển thị cửa sổ Điểm Danh
    
    # Chạy ứng dụng
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
