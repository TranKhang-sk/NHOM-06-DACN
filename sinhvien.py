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

class sinhvien(QMainWindow):
    def __init__(self, widget):
        super(sinhvien, self).__init__()
        uic.loadUi("sinhvien.ui", self)
        self.widget = widget
        self.image = ""
        self.pixmap = QPixmap("./img/avatar/user.png")

        # Khởi tạo các nút và kết nối tín hiệu
        self.btnTimKiem = self.findChild(QtWidgets.QPushButton, 'btnTimKiem')
        self.btnChonAnh = self.findChild(QtWidgets.QPushButton, 'btnChonAnh')
        self.btnThem = self.findChild(QtWidgets.QPushButton, 'btnThem')
        self.btnLamMoi = self.findChild(QtWidgets.QPushButton, 'btnLamMoi')
        self.btnSua = self.findChild(QtWidgets.QPushButton, 'btnSua')
        self.btnXoa = self.findChild(QtWidgets.QPushButton, 'btnXoa')
        self.btnThoat = self.findChild(QtWidgets.QPushButton, 'btnThoat')  # Tìm nút THOÁT

        # Kết nối các nút với các hàm xử lý
        self.btnTimKiem.clicked.connect(self.searchItem)
        self.lblAvatar.setPixmap(self.pixmap)
        self.btnChonAnh.clicked.connect(self.chooseImage)
        self.tblSinhVien.clicked.connect(self.getItem)
        self.btnThem.clicked.connect(self.addItem)
        self.btnLamMoi.clicked.connect(self.resetTextBox)
        self.btnSua.clicked.connect(self.updateItem)
        self.btnXoa.clicked.connect(self.deleteItem)
        self.btnThoat.clicked.connect(self.exitForm)  # Kết nối nút THOÁT
        self.conn = conndb.conndb()
        self.loadData()
        self.image_path = None  # Biến lưu đường dẫn ảnh

    def chooseImage(self):
        imgLink = QFileDialog.getOpenFileName(filter='*.jpg *.png')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        avatar = dir_path + '\\' + 'img\\avatar\\' + imgLink[0].split('/')[-1]
        shutil.copyfile(imgLink[0], avatar)
        self.pixmap = QPixmap(imgLink[0])
        self.lblAvatar.setPixmap(self.pixmap)
        self.image = imgLink[0].split('/')[-1]

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
        
        self.messageBoxInfo("Thông báo", "Thêm sinh viên thành công!")
        self.resetTextBox()
        self.loadData()

    def getItem(self):
        # Lấy chỉ số hàng hiện tại trong bảng
        row = self.tblSinhVien.currentRow()
        
        # Kiểm tra nếu không có hàng nào được chọn
        if row < 0:  
            return  # Trở về nếu không có hàng nào được chọn
        
        try:
            # Lấy thông tin sinh viên từ hàng đã chọn
            MaSinhVien = self.tblSinhVien.item(row, 0).text()
            HoTen = self.tblSinhVien.item(row, 1).text()
            GioiTinh = self.tblSinhVien.item(row, 2).text()
            Lop = self.tblSinhVien.item(row, 3).text()

            # Truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của sinh viên
            strsql = f"SELECT * FROM sinh_vien WHERE MaSinhVien = '{MaSinhVien}'"
            result = self.conn.queryResult(strsql)

            # Cập nhật giao diện với thông tin sinh viên
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self.pixmap = QPixmap(dir_path + '\\' + 'img\\avatar\\' + result[0][4])
            self.lblAvatar.setPixmap(self.pixmap)
            self.txtMaSinhVien.setText(MaSinhVien)
            self.txtTenSinhVien.setText(HoTen)
            self.cbGioiTinh.setCurrentText(GioiTinh)

            # Kiểm tra xem 'cbLop' có tồn tại hay không trước khi sử dụng
            if hasattr(self, 'cbLop'):
                self.cbLop.setCurrentText(Lop)

            # Vô hiệu hóa các trường và nút thêm
            self.txtMaSinhVien.setEnabled(False)
            self.btnThem.setEnabled(False)
        except Exception:
            # Không hiển thị thông báo lỗi
            pass

    def searchItem(self):
        if self.txtTimKiem.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập tên sinh viên cần tìm!")
            return
        
        TenSinhVien = self.txtTimKiem.text()
        strsql = f"SELECT * FROM sinh_vien WHERE TenSinhVien LIKE '%{TenSinhVien}%'"
        result = self.conn.queryResult(strsql)
        
        row = 0
        self.tblSinhVien.setRowCount(len(result))
        for user in result:
            self.tblSinhVien.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblSinhVien.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblSinhVien.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblSinhVien.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
            row += 1
        
        self.pixmap = QPixmap("./img/avatar/user.png")
        self.lblAvatar.setPixmap(self.pixmap)
        self.txtMaSinhVien.setEnabled(True)

    def updateItem(self):
        if self.txtMaSinhVien.text() == "" or self.txtTenSinhVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        MaSinhVien = self.txtMaSinhVien.text()
        strsql = f"SELECT * FROM sinh_vien WHERE MaSinhVien = '{MaSinhVien}'"
        result = self.conn.queryResult(strsql)
        HoTen = self.txtTenSinhVien.text()
        GioiTinh = self.cbGioiTinh.currentText()
        Lop = self.cbLop.currentText()
        Avatar = result[0][4] if self.image == "" else self.image
        
        strsql = f"UPDATE `sinh_vien` SET `TenSinhVien`='{HoTen}',`GioiTinh`='{GioiTinh}',`Lop`='{Lop}',`Avatar`='{Avatar}' WHERE `MaSinhVien`='{MaSinhVien}'"
        self.conn.queryExecute(strsql)
        
        self.messageBoxInfo("Thông báo", "Cập nhật sinh viên thành công!")
        self.resetTextBox()
        self.loadData()

    def deleteItem(self):
        if self.txtMaSinhVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn sinh viên cần xóa!")
            return
        MaSinhVien = self.txtMaSinhVien.text()
        strsql = f"DELETE FROM `sinh_vien` WHERE MaSinhVien = '{MaSinhVien}'"
        self.conn.queryExecute(strsql)
        
        self.messageBoxInfo("Thông báo", "Xóa sinh viên thành công!")
        self.resetTextBox()
        self.loadData()

    def resetTextBox(self):
        self.txtMaSinhVien.setText('')
        self.txtTenSinhVien.setText('')
        self.cbGioiTinh.setCurrentText('Nam')
        self.cbLop.setCurrentText('Lop')
        self.pixmap = QPixmap("./img/avatar/user.png")
        self.lblAvatar.setPixmap(self.pixmap)
        
        self.txtMaSinhVien.setEnabled(True)
        self.btnThem.setEnabled(True)
        self.loadData()

    def loadData(self):
        strsql = "SELECT * FROM sinh_vien"
        result = self.conn.queryResult(strsql)
        
        row = 0
        self.tblSinhVien.setRowCount(len(result))
        for user in result:
            self.tblSinhVien.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblSinhVien.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblSinhVien.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblSinhVien.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
            row += 1
        
        self.txtMaSinhVien.setEnabled(True)
        self.btnThem.setEnabled(True)
    
    def exitForm(self):
        choice = QMessageBox.question(self, 'Xác Nhận', "Bạn có chắc chắn muốn thoát không?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            sys.exit()
            
    def messageBoxInfo(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainWindow = sinhvien(widget)
    mainWindow.show()
    sys.exit(app.exec())
