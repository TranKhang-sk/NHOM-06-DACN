from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
import os
import conndb
from PyQt6.QtWidgets import QFileDialog
import shutil

class SinhVien(QMainWindow):
    def __init__(self, parent=None):
        super(SinhVien, self).__init__(parent)
        uic.loadUi("sinhvien.ui", self)
        self.setWindowTitle("Thông tin sinh viên")
        
        # Khởi tạo biến
        self.image_path = None  
        self.pixmap = QPixmap("./img/avatar/user.png")
        
        # Khởi tạo các nút và kết nối tín hiệu
        self.setupUi()

        # Kết nối đến cơ sở dữ liệu
        self.conn = conndb.conndb()
        self.loadData()

    def setupUi(self):
        self.btnTimKiem = self.findChild(QtWidgets.QPushButton, 'btnTimKiem')
        self.btnChonAnh = self.findChild(QtWidgets.QPushButton, 'btnChonAnh')
        self.btnThem = self.findChild(QtWidgets.QPushButton, 'btnThem')
        self.btnLamMoi = self.findChild(QtWidgets.QPushButton, 'btnLamMoi')
        self.btnSua = self.findChild(QtWidgets.QPushButton, 'btnSua')
        self.btnXoa = self.findChild(QtWidgets.QPushButton, 'btnXoa')
        self.btnThoat = self.findChild(QtWidgets.QPushButton, 'btnThoat')

        self.lblAvatar = self.findChild(QtWidgets.QLabel, 'lblAvatar')  
        self.lblAvatar.setPixmap(self.pixmap)
        self.lblAvatar.setScaledContents(True)

        # Kết nối các nút với các hàm xử lý
        self.btnTimKiem.clicked.connect(self.searchItem)
        self.btnChonAnh.clicked.connect(self.chooseImage)
        self.tblSinhVien.clicked.connect(self.getItem)
        self.btnThem.clicked.connect(self.addItem)
        self.btnLamMoi.clicked.connect(self.resetTextBox)
        self.btnSua.clicked.connect(self.updateItem)
        self.btnXoa.clicked.connect(self.deleteItem)
        self.btnThoat.clicked.connect(self.confirmExit)

    def chooseImage(self):
        imgLink, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.jpg *.png)")
        if imgLink:
            self.image_path = imgLink
            self.setAvatarImage()

    def setAvatarImage(self):
        self.pixmap = QPixmap(self.image_path)

        # Kiểm tra kích thước ảnh
        if self.pixmap.width() > 1024 or self.pixmap.height() > 1024:
            self.messageBoxInfo("Thông báo", "Ảnh quá lớn, vui lòng chọn ảnh có kích thước nhỏ hơn!")
            return

        # Giảm kích thước nếu cần
        self.pixmap = self.pixmap.scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.lblAvatar.setPixmap(self.pixmap)

    def addItem(self):
        if self.txtMaSinhVien.text() == "" or self.txtTenSinhVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        MaSinhVien = self.txtMaSinhVien.text()
        TenSinhVien = self.txtTenSinhVien.text()
        Lop = self.txtLop.text()
        GioiTinh = self.cbGioiTinh.currentText()
        Avatar = os.path.basename(self.image_path) if self.image_path else "user.png"

        # Thêm thông tin sinh viên vào CSDL MySQL
        strsql = f"INSERT INTO sinh_vien (MaSinhVien, TenSinhVien, Lop, GioiTinh, Avatar) VALUES ('{MaSinhVien}', '{TenSinhVien}', '{Lop}', '{GioiTinh}', '{Avatar}')"
        self.conn.queryExecute(strsql)

        if self.image_path:
            self.saveAvatar()

        self.messageBoxInfo("Thông báo", "Thêm sinh viên thành công!")
        self.resetTextBox()
        self.loadData()

    def saveAvatar(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        avatar_dir = os.path.join(dir_path, 'img', 'avatar')

        new_avatar = os.path.join(avatar_dir, os.path.basename(self.image_path))
        shutil.copy2(self.image_path, new_avatar)

    def getItem(self):
        row = self.tblSinhVien.currentRow()
        if row < 0:
            return

        try:
            MaSinhVien = self.tblSinhVien.item(row, 0).text()
            strsql = f"SELECT MaSinhVien, TenSinhVien, Lop, GioiTinh, Avatar FROM sinh_vien WHERE MaSinhVien = '{MaSinhVien}'"
            result = self.conn.queryResult(strsql)

            if result:
                self.populateForm(result[0])
            else:
                self.messageBoxInfo("Thông báo", "Không tìm thấy sinh viên.")
        except Exception as e:
            print(f"Lỗi: {e}")

    def populateForm(self, student):
        self.txtMaSinhVien.setText(student[0])
        self.txtTenSinhVien.setText(student[1])
        self.txtLop.setText(student[2])
        self.cbGioiTinh.setCurrentText(student[3])

        avatar_data = student[4]
        self.loadAvatar(avatar_data)

    def loadAvatar(self, avatar_data):
        if avatar_data:  
            # Xử lý nếu Avatar là dạng BLOB
            if isinstance(avatar_data, bytes):
                pixmap = QPixmap()
                pixmap.loadFromData(avatar_data)
            else:
                avatar_path = avatar_data.strip("b'\"")
                pixmap = QPixmap(avatar_path)

            self.lblAvatar.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.lblAvatar.setPixmap(QPixmap("./img/avatar/user.png"))

    def searchItem(self):
        if self.txtTimKiem.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập tên sinh viên cần tìm!")
            return
        
        TenSinhVien = self.txtTimKiem.text()
        strsql = f"SELECT * FROM sinh_vien WHERE TenSinhVien LIKE '%{TenSinhVien}%'"
        result = self.conn.queryResult(strsql)
        
        self.updateTable(result)
        self.resetAvatar()

    def updateTable(self, data):
        self.tblSinhVien.setRowCount(len(data))
        for row, user in enumerate(data):
            self.tblSinhVien.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblSinhVien.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblSinhVien.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblSinhVien.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))

    def resetAvatar(self):
        self.pixmap = QPixmap("./img/avatar/user.png")
        self.lblAvatar.setPixmap(self.pixmap)

    def updateItem(self):
        if self.txtMaSinhVien.text() == "" or self.txtTenSinhVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        MaSinhVien = self.txtMaSinhVien.text()
        HoTen = self.txtTenSinhVien.text()
        GioiTinh = self.cbGioiTinh.currentText()
        Lop = self.txtLop.text()

        strsql = f"SELECT * FROM sinh_vien WHERE MaSinhVien = '{MaSinhVien}'"
        result = self.conn.queryResult(strsql)

        if not result:
            self.messageBoxInfo("Thông Báo", "Mã sinh viên không tồn tại!")
            return

        self.updateStudentInfo(MaSinhVien, HoTen, GioiTinh, Lop, result[0][4])

    def updateStudentInfo(self, MaSinhVien, HoTen, GioiTinh, Lop, old_avatar):
        strsql_update = f"UPDATE sinh_vien SET TenSinhVien='{HoTen}', GioiTinh='{GioiTinh}', Lop='{Lop}' WHERE MaSinhVien='{MaSinhVien}'"
        self.conn.queryExecute(strsql_update)

        if self.image_path:
            self.updateAvatar(MaSinhVien, old_avatar)

        self.messageBoxInfo("Thông Báo", "Cập nhật thông tin sinh viên thành công!")
        self.resetTextBox()
        self.loadData()

    def updateAvatar(self, MaSinhVien, old_avatar):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        avatar_dir = os.path.join(dir_path, 'img', 'avatar')

        old_avatar_path = os.path.join(avatar_dir, old_avatar)
        if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)

        new_avatar = os.path.join(avatar_dir, os.path.basename(self.image_path))
        shutil.copy2(self.image_path, new_avatar)

    def deleteItem(self):
        if self.txtMaSinhVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập mã sinh viên cần xóa!")
            return

        MaSinhVien = self.txtMaSinhVien.text()
        strsql = f"DELETE FROM sinh_vien WHERE MaSinhVien='{MaSinhVien}'"
        self.conn.queryExecute(strsql)

        self.messageBoxInfo("Thông Báo", "Xóa sinh viên thành công!")
        self.resetTextBox()
        self.loadData()

    def resetTextBox(self):
        self.txtMaSinhVien.clear()
        self.txtTenSinhVien.clear()
        self.txtLop.clear()
        self.cbGioiTinh.setCurrentIndex(0)
        self.resetAvatar()

    def loadData(self):
        strsql = "SELECT * FROM sinh_vien"
        result = self.conn.queryResult(strsql)
        self.updateTable(result)

    def confirmExit(self):
        reply = QMessageBox.question(self, "Thông báo", "Bạn có chắc muốn thoát?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    def messageBoxInfo(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SinhVien()
    window.show()
    sys.exit(app.exec())
