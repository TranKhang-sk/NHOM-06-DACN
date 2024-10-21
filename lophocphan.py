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
import sys

class lophocphan(QtWidgets.QMainWindow):  
    def __init__(self, parent=None):
        super(lophocphan, self).__init__(parent)
        self.ui = uic.loadUi('lophocphan.ui', self)

        # Kết nối các nút với các hàm xử lý
        self.ui.btnThem.clicked.connect(self.them_lop_hoc)
        self.ui.btnSua.clicked.connect(self.sua_lop_hoc)
        self.ui.btnXoa.clicked.connect(self.xoa_lop_hoc)
        self.ui.btnTimKiemLopHocPhan.clicked.connect(self.tim_kiem_lop_hoc)

    def them_lop_hoc(self):
        # Thêm logic cho chức năng thêm lớp học phần
        pass

    def sua_lop_hoc(self):
        # Thêm logic cho chức năng sửa lớp học phần
        pass

    def xoa_lop_hoc(self):
        # Thêm logic cho chức năng xóa lớp học phần
        pass

    def tim_kiem_lop_hoc(self):
        # Thêm logic cho chức năng tìm kiếm lớp học phần
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = lophocphan()
    main_window.show()
    sys.exit(app.exec())
