import requests
import img2pdf
import os
from concurrent.futures import ThreadPoolExecutor

def descargar_imagen(url_imagen, nombre):
    print(f"Descargando Imagen {url_imagen}...")
    imagen = requests.get(url_imagen).content
    with open(nombre, 'wb') as handler:
        handler.write(imagen)
        

def descargar_libro(url_base, paginas):
    imagenes = []
    
    def descargar_pagina(i):
        url_imagen = f"{url_base}/{i:03d}.jpg"
        nombre_imagen_descargada = f"{i:03d}.jpg"
        descargar_imagen(url_imagen, nombre_imagen_descargada)
        return nombre_imagen_descargada
    
    with ThreadPoolExecutor() as executor:
        imagenes = list(executor.map(descargar_pagina, range(1, paginas+1)))
    
    return imagenes

def convertir_a_pdf(imagenes):
    bytes_pdf = img2pdf.convert(imagenes)
    for imagen in imagenes:
        os.remove(imagen)
    return bytes_pdf

def guardar_pdf(nombre_pdf, bytes_pdf):
    with open(nombre_pdf, "wb") as pdf_file:
        pdf_file.write(bytes_pdf)

def main():
    url_base = input("Ingresa la URL: ")
    paginas = int(input("Ingresa la cantidad de Paginas a descargar: "))
    titulo = input("Ingresa el título del libro: ")
    
    imagenes_descargadas = descargar_libro(url_base, paginas)
    bytes_pdf = convertir_a_pdf(imagenes_descargadas)
    
    nombre_pdf = f'{titulo}.pdf'
    guardar_pdf(nombre_pdf, bytes_pdf)
    
    print(f"PDF creado: {nombre_pdf}")

if __name__ == "__main__":
    main()
