import re
import csv
import os

def procesar_chat_estricto():
    archivo_txt = '_chat.txt'
    archivo_csv = 'datos_patologia.csv'
    
    if not os.path.exists(archivo_txt):
        print(f"No encuentro el archivo '{archivo_txt}'")
        return

    patron_adjunto = r"<adjunto:\s*(.*?\.(?:jpg|jpeg|png))>"
    patron_mensaje = r"\] (.*?): (.*)"
    
    resultados = []
    puedo_anexar = False 
    ultimo_usuario = ""

    print("Procesando chat con lógica de etiquetas [Revisar]...")

    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.replace('\u200e', '').replace('\u200f', '').strip()
            
            match_msg = re.search(patron_mensaje, linea)
            if not match_msg:
                continue

            usuario = match_msg.group(1).strip()
            contenido = match_msg.group(2).strip()
            
            match_adjunto = re.search(patron_adjunto, contenido)

            if match_adjunto:
                foto = match_adjunto.group(1).strip()
                texto_adjunto = contenido.split("<adjunto")[0].strip()
                
                if texto_adjunto == usuario or not texto_adjunto:
                    texto_adjunto = ""

                resultados.append({
                    "Imagen": foto,
                    "Descripcion": texto_adjunto
                })
                
                puedo_anexar = True
                ultimo_usuario = usuario
            
            elif puedo_anexar and usuario == ultimo_usuario:
                if "omitido" not in contenido.lower() and len(contenido) > 1:
                    original = resultados[-1]["Descripcion"]
                    
                    if original:
                        resultados[-1]["Descripcion"] = f'{original} || [Revisar] {contenido}'
                    else:
                        resultados[-1]["Descripcion"] = f'[Revisar] {contenido}'
                
                puedo_anexar = False 
            else:
                puedo_anexar = False

    for r in resultados:
        if not r["Descripcion"]:
            r["Descripcion"] = "Información en la imagen 🖼️"

    with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Imagen", "Descripcion"])
        writer.writeheader()
        writer.writerows(resultados)
    
    print(f"CSV generado con {len(resultados)} muestras.")

if __name__ == "__main__":
    procesar_chat_estricto()