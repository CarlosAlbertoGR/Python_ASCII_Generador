import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os 
ASCII_CHARS = '@%#*+=-:. ' 
ANCHO_NUEVO = 100 

def redimensionar_y_convertir(imagen, nuevo_ancho=ANCHO_NUEVO):
    """Redimensiona la imagen y la convierte a escala de grises."""
    ancho, alto = imagen.size
    proporcion = alto / ancho
    nuevo_alto = int(proporcion * nuevo_ancho * 0.55) 
    img = imagen.resize((nuevo_ancho, nuevo_alto))
    return img.convert('L')
def mapear_pixeles_a_caracteres(imagen):
    """Mapea cada píxel (0-255) a un carácter ASCII."""
    pixeles = imagen.getdata()
    rango = 255 / (len(ASCII_CHARS) - 1)
    caracteres = [ASCII_CHARS[int(p / rango)] for p in pixeles]
    return "".join(caracteres)
def generar_ascii_art(nombre_archivo):
    """Función principal que genera la cadena ASCII."""
    try:
        img = Image.open(nombre_archivo)
    except Exception as e:
        return f"Error al abrir la imagen: {e}"
    img_procesada = redimensionar_y_convertir(img)
    ascii_str = mapear_pixeles_a_caracteres(img_procesada)
    ascii_art = ""
    for i in range(0, len(ascii_str), img_procesada.width):
        ascii_art += ascii_str[i:i + img_procesada.width] + "\n"
    return ascii_art
class GeneradorAsciiApp:
    def __init__(self, master):
        self.master = master
        master.title("Generador de Arte ASCII")
        master.geometry("850x700") 
        master.configure(bg='#f0f0f0')
        self.titulo = tk.Label(master, text="🎨 Generador de Arte ASCII con Python",
                               font=("Arial", 16, "bold"), bg='#f0f0f0')
        self.titulo.pack(pady=10)
        self.cargar_btn = tk.Button(master, text="Cargar Imagen", command=self.cargar_imagen,
                                    font=("Arial", 12), bg='#4CAF50', fg='white', relief=tk.RAISED)
        self.cargar_btn.pack(pady=10)
        self.ruta_label = tk.Label(master, text="Ninguna imagen cargada.", bg='#f0f0f0')
        self.ruta_label.pack()
        self.ascii_label = tk.Label(master, text="", font=("Courier", 8), bg='black', fg='lime', justify=tk.LEFT)
        self.ascii_label.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.imagen_original_label = tk.Label(master, bg='#f0f0f0')
        self.imagen_original_label.pack(pady=10)
    def cargar_imagen(self):
        """Abre un diálogo de archivo y procesa la imagen seleccionada."""
        ruta_archivo = filedialog.askopenfilename(
            initialdir=os.getcwd(), 
            title="Seleccionar archivo de imagen",
            filetypes=(("Archivos de Imagen", "*.jpg *.jpeg *.png *.bmp"),
                       ("Todos los archivos", "*.*"))
        )
        if ruta_archivo:
            self.ruta_label.config(text=f"Cargado: {os.path.basename(ruta_archivo)}")
            arte_ascii = generar_ascii_art(ruta_archivo)
            self.ascii_label.config(text=arte_ascii)
            self.mostrar_imagen_original(ruta_archivo)
    def mostrar_imagen_original(self, ruta_archivo):
        """Muestra una miniatura de la imagen cargada."""
        try:
            img = Image.open(ruta_archivo)
            img.thumbnail((150, 150)) 
            self.tk_img = ImageTk.PhotoImage(img) 
            self.imagen_original_label.config(image=self.tk_img)
            self.imagen_original_label.image = self.tk_img 
        except Exception as e:
            self.imagen_original_label.config(text=f"Error al mostrar miniatura: {e}")
            self.tk_img = None
if __name__ == '__main__':
    root = tk.Tk()
    app = GeneradorAsciiApp(root)
    root.mainloop()