import re
import csv
import os

def procesar_chat():
    archivo_txt = '_chat.txt'
    archivo_csv = 'datos_patologia.csv'
    
    if not os.path.exists(archivo_txt):
        print(f"❌ No encuentro el archivo '{archivo_txt}'")
        return

    patron = r"<adjunto:\s*(.*?\.(?:jpg|jpeg|png))>"
    
    resultados = []
    
    print("Procesando chat...")
    
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            linea_limpia = linea.replace('\u200e', '').replace('\u200f', '').strip()
            
            match = re.search(patron, linea_limpia)
            if match:
                nombre_foto = match.group(1).strip()
                
                try:
                    parte_mensaje = linea_limpia.split(": ", 1)[1]
                    descripcion = parte_mensaje.split("<adjunto")[0].strip()
                    
                    if len(descripcion) > 2:
                        resultados.append({
                            "Imagen": nombre_foto,
                            "Descripcion": descripcion
                        })
                except IndexError:
                    continue

    if resultados:
        with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Imagen", "Descripcion"])
            writer.writeheader()
            writer.writerows(resultados)
        print(f"✅ ¡Éxito! Se encontraron {len(resultados)} muestras con descripción.")
    else:
        print("⚠️ Sigo sin encontrar coincidencias. Por favor, verifica que el archivo se llame '_chat.txt' y tenga el contenido dentro.")

if __name__ == "__main__":
    procesar_chat()