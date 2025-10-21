# tu_modelo.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# --- 1. Cargar el modelo y las etiquetas ---
try:
    print("Cargando modelo desde 'clasif_posturas.keras'...")
    modelo_cargado = load_model('clasif_posturas.keras')
    
    clases = np.load('label_encoder.npy', allow_pickle=True)
    
    # IMPORTANTE: Este es el tamaño de imagen de tu script de entrenamiento
    IMG_SIZE = 64 
    
    print("¡Modelo cargado exitosamente!")
    print(f"Modelo entrenado para {len(clases)} clases: {clases}")

except Exception as e:
    print(f"Error crítico al cargar el modelo o las etiquetas: {e}")
    modelo_cargado = None
    clases = None
# ---------------------------------------------------

def detectar_postura(frame):
    """
    Recibe un frame de OpenCV, lo procesa para el modelo simple
    y devuelve un string con la postura detectada.
    """
    if modelo_cargado is None:
        return "Error: Modelo no cargado"

    try:
        # --- 2. Pre-procesamiento (¡CORREGIDO!) ---
        
        # 1. Convertir a escala de grises (1 canal)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. Cambiar tamaño
        img_resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
        
        # 3. Normalizar (rango 0 a 1)
        img_normalized = img_resized / 255.0
        
        # 4. Reformar (Batch, Altura, Ancho, Canales)
        # El '1' al final es para la escala de grises
        img_reshaped = img_normalized.reshape(1, IMG_SIZE, IMG_SIZE, 1)

        # --- 3. Inferencia (Predicción) ---
        prediction = modelo_cargado.predict(img_reshaped)
        
        # --- 4. Post-procesamiento del resultado ---
        indice_prediccion = np.argmax(prediction)
        etiqueta_final = clases[indice_prediccion]
        
        return etiqueta_final.capitalize()

    except Exception as e:
        print(f"Error en la detección: {e}")
        return "Error"