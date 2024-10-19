import mysql.connector
import numpy as np
import cv2
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import img_to_array

# Thiết lập kết nối đến cơ sở dữ liệu
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Thay đổi với mật khẩu của bạn
        database="sinhvien_ai"
    )

# Lấy hình ảnh sinh viên từ cơ sở dữ liệu
def fetch_student_images():
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT Avatar FROM sinh_vien")
    images = cursor.fetchall()
    
    # Chuyển đổi hình ảnh từ dạng nhị phân
    student_images = []
    for img in images:
        # Giả sử hình ảnh được lưu ở dạng nhị phân
        student_images.append(np.frombuffer(img[0], np.uint8))
    
    cursor.close()
    db_connection.close()
    return student_images

# Tiền xử lý hình ảnh
def preprocess_images(images):
    processed_images = []
    for image in images:
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Chuyển đổi nhị phân thành hình ảnh
        image = cv2.resize(image, (128, 128))  # Thay đổi kích thước hình ảnh
        image = img_to_array(image) / 255.0  # Chuyển đổi thành mảng và chuẩn hóa
        processed_images.append(image)
    return np.array(processed_images)

# Tạo mô hình CNN
def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Điều chỉnh cho số lượng lớp đầu ra
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Huấn luyện mô hình
def train_model():
    images = fetch_student_images()
    processed_images = preprocess_images(images)
    
    # Tạo nhãn cho mô hình (cần điều chỉnh theo dữ liệu của bạn)
    labels = np.array([1] * len(processed_images))  # Giả định tất cả hình ảnh là cùng một lớp (thay đổi nếu cần)

    model = create_model()
    model.fit(processed_images, labels, epochs=10, batch_size=32)

    # Lưu mô hình
    model.save("student_model.h5")

if __name__ == "__main__":
    train_model()
