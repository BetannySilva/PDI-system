from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from charset_normalizer import from_path
import cv2
from numpy import imag


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Processamento de Imagens")
        self.setGeometry(100, 100, 800, 500)

        # Layout principal
        main_layout = QHBoxLayout()
        # Sidebar


        self.r1_input = QLineEdit()
        self.s1_input = QLineEdit()
        self.r2_input = QLineEdit()
        self.s2_input = QLineEdit()
        self.r1_input.setPlaceholderText("r1 (0-255)")
        self.r1_input.setObjectName("paramInput")
        self.s1_input.setPlaceholderText("s1 (0-255)")
        self.s1_input.setObjectName("paramInput")
        self.r2_input.setPlaceholderText("r2 (0-255)")
        self.r2_input.setObjectName("paramInput")
        self.s2_input.setPlaceholderText("s2 (0-255)")
        self.s2_input.setObjectName("paramInput")
        self.bit_input = QLineEdit()
        self.bit_input.setObjectName("paramInput")
        self.bit_input.setPlaceholderText("Bit (0-7)")



        self.gamma_input = QLineEdit()
        self.gamma_input.setObjectName("gammaInput")
        self.gamma_input.setPlaceholderText("Gamma (ex: 1.0)")
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)


        title = QLabel("MENU")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        # Botões
        self.btn_load = QPushButton("Carregar Imagem")
        self.btn_save = QPushButton("Salvar Imagem")
        self.btn_zero = QPushButton("Zerar Pixels")
        self.btn_restore = QPushButton("Restaurar Original")
        self.btn_potencia = QPushButton("Transformação de Potência")
        self.bnt_contraste = QPushButton("Alargamento de Contraste")
        self.bnt_bit_plane = QPushButton("Bit Plane Slicing")


        # Conectar botão
        self.btn_load.clicked.connect(self.load_image)
        self.btn_zero.clicked.connect(self.zero_image)
        self.btn_restore.clicked.connect(self.restore_image)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_potencia.clicked.connect(self.aplicar_gamma)
        self.bnt_contraste.clicked.connect(self.aplicar_alargamento_contraste)
        self.bnt_bit_plane.clicked.connect(self.aplicar_bit_plane_slicing)


        # Adicionar na sidebar
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(self.btn_load)
        sidebar_layout.addWidget(self.btn_save)
        sidebar_layout.addWidget(self.btn_zero)
        sidebar_layout.addWidget(self.btn_restore)
        sidebar_layout.addWidget(self.btn_potencia)
        sidebar_layout.addWidget(self.gamma_input)
        sidebar_layout.addWidget(self.bnt_contraste)
        sidebar_layout.addWidget(self.r1_input)
        sidebar_layout.addWidget(self.s1_input)
        sidebar_layout.addWidget(self.r2_input)
        sidebar_layout.addWidget(self.s2_input)
        sidebar_layout.addWidget(self.bnt_bit_plane)
        sidebar_layout.addWidget(self.bit_input)

        sidebar_layout.addStretch()

        # Área da imagem
        self.image_label = QLabel("Área Imagem")
        self.image_label.setObjectName("imageArea")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Adicionar ao layout principal
        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(self.image_label, 4)

        # Container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.original_image = None
        self.current_image = None

        with open("assets/style.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

       


    def load_image(self):
            file_path, _ = QFileDialog.getOpenFileName()

            if file_path:
                self.original_image = cv2.imread(file_path)
                self.current_image = self.original_image.copy()
                self.display_image(self.current_image)

    def display_image(self, imagem):
            
            if len(imagem.shape) == 2: 
                 h,w= imagem.shape
                 
                 q_img = QImage(imagem.data, w, h, w, QImage.Format_Grayscale8) 

            else:

                img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

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

    def transformacao_potencia(self, c, gamma, current_image):
            if self.current_image is not None:
                self.final_image = current_image.copy()
                rows, cols, channels = current_image.shape 
                for i in range(rows):
                    for j in range(cols): 
                        for k in range(channels): 
                            r = current_image[i, j, k]
                            #normalização
                            r = r/255.0
                            #transformação de potência
                            s = (r**gamma)*c
                            #reescalar
                            s= s*255
                            #limite
                            s = max(0, min(255, int(s)))
                            self.final_image[i, j, k] = s

            return self.final_image

    def aplicar_gamma(self):
            if self.current_image is not None:
                try:
                    gamma = float(self.gamma_input.text())

                    self.current_image = self.transformacao_potencia(
                        1, gamma, self.original_image
                    )

                    self.display_image(self.current_image)

                except:
                    print("Valor inválido")

    def alargamento_contraste(self, r1, s1, r2, s2 ,current_image):
        if self.current_image is not None:
            self.final_image = current_image.copy()
            
            rows, cols, channels = current_image.shape 
            for i in range(rows):
                for j in range(cols): 
                    for k in range(channels): 
                        r = current_image[i, j, k]
                        if r2 == r1:
                         r2 += 1
                        if r < r1:
                            s=(s1/r1)*r
                        elif r <= r2: 
                            s = ((s2 - s1)/(r2 - r1)) * (r - r1) + s1
                        else:
                            s = ((255 - s2)/(255 - r2)) * (r - r2) + s2
                        s = max(0, min(255, int(s)))
                        self.final_image[i, j, k] = s

            return self.final_image
        
    def aplicar_alargamento_contraste(self):
            if self.current_image is not None:
                try:
                    r1 = float(self.r1_input.text())
                    s1 = float(self.s1_input.text())
                    r2 = float(self.r2_input.text())
                    s2 = float(self.s2_input.text())

                    self.current_image = self.alargamento_contraste(
                        r1, s1, r2, s2, self.original_image
                    )

                    self.display_image(self.current_image)

                except:
                    print("Valor inválido")

    def bit_plane_slicing(self, bit, current_image):
        if current_image is not None:
            
                if bit < 0 or bit > 7:
                  print("Valor do bit deve ser entre 0 e 7")
                  return current_image

                gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

                final_image = current_image.copy()
                rows, cols = gray.shape 

                for i in range(rows):
                    for j in range(cols): 
                        pixel = gray[i, j]

                        plano = (pixel >> bit) & 1

                        if plano == 1:
                            final_image[i, j] = 255
                        else:
                            final_image[i, j] = 0

        return final_image
            
        

    def aplicar_bit_plane_slicing(self):
            if self.current_image is not None:
                try:
                    bit = int(self.bit_input.text())

                    self.current_image = self.bit_plane_slicing(bit, self.original_image)

                    self.display_image(self.current_image)

                except Exception as e:
                    print("Erro:", e)
                    print("Valor inválido")