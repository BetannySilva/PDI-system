from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QLineEdit, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from charset_normalizer import from_path
import cv2
import numpy as np



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Processamento de Imagens")
        self.setGeometry(100, 100, 800, 500)

        # Layout principal
        main_layout = QHBoxLayout()
        # Sidebar

        # ===== SIDEBAR =====
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(sidebar)

        # ===== TÍTULO =====
        title = QLabel("MENU")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        # ===== SEÇÕES =====
        sec_arquivo = QLabel("📂 Arquivo")
        sec_intensidade = QLabel("🎨 Intensidade")
        sec_histograma = QLabel("📊 Histograma")
        sec_lineares = QLabel("🌊 Filtros Lineares")
        sec_ordem = QLabel("🧱 Filtros de Ordem")

        for sec in [sec_arquivo, sec_intensidade, sec_histograma, sec_lineares, sec_ordem]:
            sec.setObjectName("sectionTitle")

        # ===== INPUTS =====
        self.gamma_input = QLineEdit()
        self.gamma_input.setPlaceholderText("Gamma")

        self.r1_input = QLineEdit()
        self.r1_input.setPlaceholderText("r1")

        self.s1_input = QLineEdit()
        self.s1_input.setPlaceholderText("s1")

        self.r2_input = QLineEdit()
        self.r2_input.setPlaceholderText("r2")

        self.s2_input = QLineEdit()
        self.s2_input.setPlaceholderText("s2")

        self.bit_input = QLineEdit()
        self.bit_input.setPlaceholderText("Bit (0-7)")

        self.kernel_gauss_input = QLineEdit()
        self.kernel_gauss_input.setPlaceholderText("Kernel Gauss")

        self.sigma_input = QLineEdit()
        self.sigma_input.setPlaceholderText("Sigma")

        self.kernel_ordem_input = QLineEdit()
        self.kernel_ordem_input.setPlaceholderText("Kernel (Min/Max/Median)")

        # ===== BOTÕES =====
        self.btn_load = QPushButton("Carregar Imagem")
        self.btn_save = QPushButton("Salvar Imagem")
        self.btn_zero = QPushButton("Zerar Pixels")
        self.btn_restore = QPushButton("Restaurar Original")

        self.btn_potencia = QPushButton("Gamma")
        self.bnt_contraste = QPushButton("Contraste")
        self.bnt_bit_plane = QPushButton("Bit Plane")

        self.bnt_histograma = QPushButton("Equalização")
        self.bnt_pseudocores = QPushButton("Pseudocores")

        self.btn_gaussian = QPushButton("Gaussiano")

        self.btn_min = QPushButton("Mínimo")
        self.btn_max = QPushButton("Máximo")
        self.btn_median = QPushButton("Mediana")

        # ===== CONEXÕES =====
        self.btn_load.clicked.connect(self.load_image)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_zero.clicked.connect(self.zero_image)
        self.btn_restore.clicked.connect(self.restore_image)

        self.btn_potencia.clicked.connect(self.aplicar_gamma)
        self.bnt_contraste.clicked.connect(self.aplicar_alargamento_contraste)
        self.bnt_bit_plane.clicked.connect(self.aplicar_bit_plane_slicing)

        self.bnt_histograma.clicked.connect(self.aplicar_equalizacao_histograma)
        self.bnt_pseudocores.clicked.connect(self.aplicar_fatiamento_pseudocores)

        self.btn_gaussian.clicked.connect(self.filtro_gaussiano)

        self.btn_min.clicked.connect(lambda: self.aplicar_filtro(self.min_filter))
        self.btn_max.clicked.connect(lambda: self.aplicar_filtro(self.max_filter))
        self.btn_median.clicked.connect(lambda: self.aplicar_filtro(self.median_filter))

        # ===== MONTAGEM =====

        sidebar_layout.addWidget(title)

        # --- ARQUIVO ---
        sidebar_layout.addWidget(sec_arquivo)
        sidebar_layout.addWidget(self.btn_load)
        sidebar_layout.addWidget(self.btn_save)
        sidebar_layout.addWidget(self.btn_zero)
        sidebar_layout.addWidget(self.btn_restore)

        # --- INTENSIDADE ---
        sidebar_layout.addWidget(sec_intensidade)
        sidebar_layout.addWidget(self.btn_potencia)
        sidebar_layout.addWidget(self.gamma_input)

        sidebar_layout.addWidget(self.bnt_contraste)
        sidebar_layout.addWidget(self.r1_input)
        sidebar_layout.addWidget(self.s1_input)
        sidebar_layout.addWidget(self.r2_input)
        sidebar_layout.addWidget(self.s2_input)

        sidebar_layout.addWidget(self.bnt_bit_plane)
        sidebar_layout.addWidget(self.bit_input)

        # --- HISTOGRAMA ---
        sidebar_layout.addWidget(sec_histograma)
        sidebar_layout.addWidget(self.bnt_histograma)
        sidebar_layout.addWidget(self.bnt_pseudocores)

        # --- FILTROS LINEARES ---
        sidebar_layout.addWidget(sec_lineares)
        sidebar_layout.addWidget(self.btn_gaussian)
        sidebar_layout.addWidget(self.kernel_gauss_input)
        sidebar_layout.addWidget(self.sigma_input)

        # --- FILTROS DE ORDEM ---
        sidebar_layout.addWidget(sec_ordem)
        sidebar_layout.addWidget(self.kernel_ordem_input)
        sidebar_layout.addWidget(self.btn_min)
        sidebar_layout.addWidget(self.btn_max)
        sidebar_layout.addWidget(self.btn_median)

        sidebar_layout.addStretch()

        # ===== ADICIONAR AO MAIN LAYOUT =====
        main_layout.addWidget(scroll, 1)



        # ===== ÁREA DA IMAGEM =====
        self.image_label = QLabel("Original")
        self.image_equalizada_label = QLabel("Equalizada")
        self.hist_original_label = QLabel("Hist Original")
        self.hist_equalizado_label = QLabel("Hist Equalizado")

        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_equalizada_label.setAlignment(Qt.AlignCenter)
        self.hist_original_label.setAlignment(Qt.AlignCenter)
        self.hist_equalizado_label.setAlignment(Qt.AlignCenter)

        # Layout das imagens
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.image_equalizada_label)

        # Layout dos histogramas
        hist_layout = QHBoxLayout()
        hist_layout.addWidget(self.hist_original_label)
        hist_layout.addWidget(self.hist_equalizado_label)

        # Adicionar ao layout principal
        main_layout.addLayout(image_layout, 4)
        main_layout.addLayout(hist_layout, 2)

        # ===== CONTAINER FINAL =====
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


        with open("assets/style.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def load_image(self):
            file_path, _ = QFileDialog.getOpenFileName()

            if file_path:
                self.original_image = cv2.imread(file_path)
                self.current_image = self.original_image.copy()
                self.display_image(self.current_image, self.image_label)

    def display_image(self, imagem, label):
            
            if len(imagem.shape) == 2: 
                 h,w= imagem.shape
                 
                 q_img = QImage(imagem.data, w, h, w, QImage.Format_Grayscale8) 

            else:

                img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

                h, w, ch = img_rgb.shape
                bytes_per_line = ch * w

                q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)


                # 🔥 REDIMENSIONAMENTO AUTOMÁTICO
            pixmap = pixmap.scaled(
                label.width(),
                label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            label.setPixmap(pixmap)
        
    def zero_image(self):
            if self.current_image is not None:
                self.current_image[:]=0
                self.display_image(self.current_image, self.image_label)

    def restore_image(self):
            if self.original_image is not None:
                self.current_image = self.original_image.copy()
                self.display_image(self.current_image, self.image_label)

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
            if current_image is not None:
                img = current_image.astype(float)

                 # normalização
                r = img / 255.0
                # transformação de potência
                s = (r ** gamma) * c

                #reescalando 
                s = s * 255
                # limite (equivalente ao max/min)
                s = np.clip(s, 0, 255)

                final_image= s.astype(np.uint8)
                return final_image
            
            return None
    
    def aplicar_gamma(self):
            if self.current_image is not None:
                try:
                    gamma = float(self.gamma_input.text())

                    self.current_image = self.transformacao_potencia(
                        1, gamma, self.original_image
                    )

                    self.display_image(self.current_image, self.image_label)

                except:
                    print("Valor inválido")

    def alargamento_contraste(self, r1, s1, r2, s2 ,current_image):
        if current_image is not None:
            imagem = current_image.astype(float)
            r = imagem

            mask1 = imagem < r1
            mask2 = (imagem>=r1) & (imagem<=r2)
            mask3 = imagem > r2

            final_image = np.zeros_like(imagem)

            final_image[mask1] = (s1 / r1) * imagem[mask1]
            final_image[mask2] = ((s2 - s1) / (r2 - r1)) * (imagem[mask2] - r1) + s1
            final_image[mask3] = ((255 - s2) / (255 - r2)) * (imagem[mask3] - r2) + s2  
            final_image = np.clip(final_image, 0, 255).astype(np.uint8)





            return final_image
        
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

                    self.display_image(self.current_image, self.image_label)

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

                    self.display_image(self.current_image, self.image_label)

                except Exception as e:
                    print("Erro:", e)
                    print("Valor inválido")
                    
    def calcular_histograma(self, gray):
        histograma = np.zeros(256)

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                intensidade = gray[i, j]
                histograma[intensidade] += 1

        return histograma

    def grafico_histograma(self, histograma):
        altura_img = 300
        largura_img = 512
        hist_img = np.zeros((altura_img, largura_img), dtype=np.uint8)
        histograma_normalizado = (histograma / np.max(histograma)) * altura_img
        for i in range(256):
             valor = int(histograma_normalizado[i]  )
             cv2.line(
                    hist_img,
                    (i * 2, altura_img),
                    (i * 2, altura_img - valor),
                    255,
                    1
                )
             
        return hist_img

    def equalizacao_histograma(self, current_image):
        if current_image is not None:

            #conversão pra escala de cinza
            gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
            final_image = current_image.copy()

            #histograma
            histograma_original  = self.calcular_histograma(gray)
            #pdf
            quant_pixels = gray.shape[0] * gray.shape[1]
            probability = histograma_original / quant_pixels

            #cdf
            cdf = np.zeros(256)
            cdf[0] = probability[0]
            for k in range(1, 256):
                cdf[k] = cdf[k-1] + probability[k]

            #função de transformação

            L = 256
            transform = np.floor(cdf * (L - 1) + 0.5).astype(np.uint8)

            #aplicando transformação 
            imagem_equalizada = transform[gray]
            histograma_equalizado = self.calcular_histograma(imagem_equalizada)


            

            return gray, imagem_equalizada, histograma_original, histograma_equalizado

    def aplicar_equalizacao_histograma(self):
     

     if self.current_image is not None:
          
        gray, img_equalizada, hist_original, hist_equalizado = self.equalizacao_histograma(self.current_image)

        self.display_image(gray, self.image_label)
        self.display_image(img_equalizada, self.image_equalizada_label)
        hist_img_orig = self.grafico_histograma(hist_original)
        hist_img_eq = self.grafico_histograma(hist_equalizado)

        self.display_image(hist_img_orig, self.hist_original_label)
        self.display_image(hist_img_eq, self.hist_equalizado_label)

    def fatiamento_pseudocores(self, current_image):
        if current_image is not None:
            gray= cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
            numero_faixas=8

            faixa_tamanho = 256 / numero_faixas
            intensidade_pixel = (gray / faixa_tamanho).astype(int)

            intensidade_pixel = np.clip(intensidade_pixel, 0, numero_faixas - 1)
            print(gray.min(), gray.max())
             
            cores = np.array([
            [128,   0,   0],
            [255,   0,   0],
            [255, 128,   0],
            [0,   255,   0],
            [0,   255, 255],
            [0,   165, 255],
            [0,    69, 255],
            [0,     0, 255]
        ], dtype=np.uint8)
            
            imagem_colorida = cores[intensidade_pixel]

            return imagem_colorida
    
    def aplicar_fatiamento_pseudocores(self):

        if self.current_image is not None:
            imagem_colorida = self.fatiamento_pseudocores(self.current_image)

            self.current_image = imagem_colorida

            self.display_image(imagem_colorida, self.image_label)

    def kernel(self, size, desvioP):
        #distamcia do centro
        raio = size //2

        #criando kernel
        kernel = np.zeros((size, size), dtype=np.float32)

        #constante K
        K = 1 / (2 * np.pi * (desvioP ** 2))

        for s in range(-raio, raio + 1):
             for t in range(-raio , raio +1):
                W = K* np.exp(-(s**2 + t**2)/(2*desvioP**2))
                kernel[s+raio, t+raio] = W
        return kernel / np.sum(kernel)
    

    def convolucao(self, imagem, kernel):

            altura, largura = imagem.shape
            raio = kernel.shape[0] // 2

            final_image = np.zeros((altura, largura), dtype=np.float32)

            bordas = np.pad(imagem, raio, mode='constant', constant_values=0)

            for i in range(altura):
                for j in range(largura):

                    janela = bordas[i:i + 2*raio +1, j:j + 2*raio +1]

                    valor_pixel = np.sum(janela * kernel)

                    final_image[i,j] = valor_pixel

            return np.clip(final_image, 0, 255).astype(np.uint8)

    def filtro_gaussiano(self):
        if self.current_image is not None:
            try:
                tamanho = int(self.kernel_gauss_input.text())
                desvioP = float(self.sigma_input.text())

                if len(self.current_image.shape) == 3:
                    gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
                else:
                    gray = self.current_image

                final_image = self.convolucao(gray, self.kernel(tamanho, desvioP))

                self.current_image = final_image
                self.display_image(self.current_image, self.image_label)

            except Exception as e:
                print("Erro:", e)


    def min_filter(self, current_image, kernel_size): 
        if current_image is None:
            print("Nenhuma imagem carregada")
            return None 
        if len(current_image.shape) == 3: 
            gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY) 
        else: gray = current_image 
        
        if kernel_size % 2 == 0: 
            print("Tamanho do kernel deve ser ímpar") 
            return None 
        else: 
            altura, largura = gray.shape 
            pad_size = kernel_size // 2 
            padded_image = np.pad(gray, pad_size, mode='edge') 
            final_image = np.zeros((altura, largura), dtype=np.uint8) 
            for i in range(altura): 
                for j in range(largura): 
                    janela = padded_image[i:i+kernel_size, j:j+kernel_size] 
                    final_image[i, j] = np.min(janela) 
            return final_image
        

    def max_filter(self, current_image, kernel_size): 
            if current_image is None:
                print("Nenhuma imagem carregada")
                return None 
            if len(current_image.shape) == 3: 
                gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY) 
            else: gray = current_image 
            
            if kernel_size % 2 == 0: 
                print("Tamanho do kernel deve ser ímpar") 
                return None 
            else: 
                altura, largura = gray.shape 
                pad_size = kernel_size // 2 
                padded_image = np.pad(gray, pad_size, mode='edge') 
                final_image = np.zeros((altura, largura), dtype=np.uint8) 
                for i in range(altura): 
                    for j in range(largura): 
                        janela = padded_image[i:i+kernel_size, j:j+kernel_size] 
                        final_image[i, j] = np.max(janela) 
                return final_image
        

    def median_filter(self, current_image, kernel_size):

        if current_image is None:
            print("Nenhuma imagem carregada")
            return current_image

        # Converter para cinza se necessário
        if len(current_image.shape) == 3:
            gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = current_image

        # Validar kernel
        if kernel_size % 2 == 0:
            print("Tamanho do kernel deve ser ímpar")
            return current_image

        altura, largura = gray.shape
        pad_size = kernel_size // 2
        padded_image = np.pad(gray, pad_size, mode='edge')
        final_image = np.zeros((altura, largura), dtype=np.uint8)

        for i in range(altura):
            for j in range(largura):
                janela = padded_image[i:i+kernel_size, j:j+kernel_size]
                final_image[i, j] = np.median(janela)

        return final_image
    
    def aplicar_filtro(self, funcao_filtro):
        if self.current_image is not None:
            try:
                texto = self.kernel_ordem_input.text()

                if texto == "":
                    print("Digite o tamanho do kernel")
                    return

                k = int(texto)

                resultado = funcao_filtro(self.current_image, k)

                if resultado is not None:
                    self.current_image = resultado
                    self.display_image(self.current_image, self.image_label)

            except:
                print("Valor inválido")























