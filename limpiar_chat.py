import re
import csv
import os

def procesar_chat():
    archivo_txt = '_chat.txt'  # Asegúrate de que el archivo se llame así
    archivo_csv = 'datos_patologia.csv'
    
    if not os.path.exists(archivo_txt):
        print(f"❌ Error: No encuentro el archivo '{archivo_txt}' en esta carpeta.")
        print("Asegúrate de haberlo movido a la carpeta del proyecto.")
        return

    # Este patrón busca el formato estándar de exportación de WhatsApp:
    # [fecha hora] Nombre: <Adjunto: imagen.jpg> Descripción del patógeno
    patron = r"<Adjunto: (.*?\.jpg)> (.*)"
    
    resultados = []
    
    print("Reading chat...")
    
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            # Buscamos líneas que contengan adjuntos de imagen
            match = re.search(patron, linea)
            if match:
                nombre_foto = match.group(1).strip()
                # Limpiamos el texto descriptivo (quitamos espacios extra)
                descripcion = match.group(2).strip()
                
                # Solo lo agregamos si hay una descripción válida
                if descripcion:
                    resultados.append({
                        "Imagen": nombre_foto, 
                        "Descripcion": descripcion
                    })

    # Guardar los resultados en el archivo CSV
    if resultados:
        with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Imagen", "Descripcion"])
            writer.writeheader()
            writer.writerows(resultados)
        
        print("-" * 30)
        print(f"✅ ¡PROCESO EXITOSO!")
        print(f"Se encontraron {len(resultados)} muestras con descripción.")
        print(f"Archivo generado: {archivo_csv}")
        print("-" * 30)
    else:
        print("⚠️ No se encontró ninguna coincidencia.")
        print("Esto puede pasar si el formato de tu WhatsApp es distinto.")
        print("Prueba abrir el .txt y mira si las fotos aparecen como '<Adjunto: ...>' o con otra palabra.")

if __name__ == "__main__":
    procesar_chat()