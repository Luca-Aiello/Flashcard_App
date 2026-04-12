import pandas as pd
import os

def rellenar_muestras_faltantes():
    archivo_csv = 'datos_patologia.csv'
    carpeta_fotos = 'fotos'
    
    if not os.path.exists(archivo_csv):
        print(f"❌ No se encontró {archivo_csv}")
        return

    # 1. Cargar lo que ya existe
    df = pd.read_csv(archivo_csv)
    fotos_en_csv = set(df['Imagen'].astype(str).tolist())
    
    # 2. Listar fotos reales en la carpeta
    if not os.path.exists(carpeta_fotos):
        print(f"❌ No se encontró la carpeta '{carpeta_fotos}'")
        return
        
    fotos_en_carpeta = [f for f in os.listdir(carpeta_fotos) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    nuevos_registros = []
    
    # 3. Ver cuáles faltan
    for foto in fotos_en_carpeta:
        if foto not in fotos_en_csv:
            nuevos_registros.append({
                "Imagen": foto,
                "Descripcion": "Información en la imagen 🖼️"
            })
    
    # 4. Guardar cambios
    if nuevos_registros:
        df_nuevos = pd.DataFrame(nuevos_registros)
        df_final = pd.concat([df, df_nuevos], ignore_index=True)
        df_final.to_csv(archivo_csv, index=False)
        print(f"✅ ¡Éxito! Se agregaron {len(nuevos_registros)} fotos nuevas.")
    else:
        print("✨ Todas las fotos ya estaban registradas.")

if __name__ == "__main__":
    rellenar_muestras_faltantes()