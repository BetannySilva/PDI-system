  
from PyQt5 import *




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