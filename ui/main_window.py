from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Processamento de Imagens")
        self.setGeometry(100, 100, 800, 500)

        # Layout principal
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar_layout = QVBoxLayout()
        title = QLabel("Menu")
        title.setAlignment(Qt.AlignCenter)

        # Botões
        self.btn_load = QPushButton("Carregar Imagem")
        self.btn_save = QPushButton("Salvar Imagem")
        self.btn_zero = QPushButton("Zerar Pixels")
        self.btn_restore = QPushButton("Restaurar Original")

        # Conectar botão
        self.btn_load.clicked.connect(self.load_image)
        self.btn_zero.clicked.connect(self.zero_image)
        self.btn_restore.clicked.connect(self.restore_image)
        self.btn_save.clicked.connect(self.save_image)

        # Adicionar na sidebar
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(self.btn_load)
        sidebar_layout.addWidget(self.btn_save)
        sidebar_layout.addWidget(self.btn_zero)
        sidebar_layout.addWidget(self.btn_restore)
        sidebar_layout.addStretch()

        # Área da imagem
        self.image_label = QLabel("Área Imagem")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Adicionar ao layout principal
        main_layout.addLayout(sidebar_layout, 1)
        main_layout.addWidget(self.image_label, 4)

        # Container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.original_image = None
        self.current_image = None

        

    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName()

        if file_path:
            self.original_image = cv2.imread(file_path)
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w

        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap)
    
    def zero_image(self):
        if self.current_image is not None:
            self.current_image[:]=0
            self.display_image(self.current_image)

    def restore_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)

    def save_image(self):
        if self.current_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Imagem",
            "",
            "PNG (*.png)"
        )
        if file_path:
            cv2.imwrite(f"{file_path}.png", self.current_image)
