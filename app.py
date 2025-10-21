# app.py
from flask import Flask, render_template, request, jsonify
import webbrowser
from threading import Timer
from waitress import serve
import base64
import numpy as np
import cv2

# Asumimos que tu modelo está en un archivo llamado 'tu_modelo.py' EL MODELO/ ARCHIVO LO ENVIARÁ CELESTINO
# y tiene una función 'detectar_postura(frame)'
# ¡DEBES MODIFICAR ESTA LÍNEA!
from tu_modelo import detectar_postura 

app = Flask(__name__)

@app.route('/')
def index():
    """Ruta principal que muestra la página web."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Recibe la imagen, la procesa con el modelo y devuelve el resultado."""
    # Obtener la imagen en formato Base64 desde el JSON de la solicitud
    image_data = request.json['image']
    
    # Decodificar la imagen Base64
    # Se quita el prefijo 'data:image/jpeg;base64,'
    image_data = image_data.split(',')[1]
    decoded_image = base64.b64decode(image_data)
    
    # Convertir los datos de la imagen a un array de numpy
    np_arr = np.frombuffer(decoded_image, np.uint8)
    
    # Decodificar el array de numpy a una imagen de OpenCV
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # --- ¡AQUÍ SE USA TU MODELO! ---
    # Llama a la función de tu modelo para obtener la postura
    # Esta función debe recibir una imagen (frame de OpenCV) y devolver un string
    resultado = detectar_postura(frame) 
    
    # Devolver el resultado en formato JSON
    return jsonify({'postura': resultado})
def open_browser():
    """Abre el navegador en la dirección correcta."""
    webbrowser.open_new("http://127.0.0.1:5000")
if __name__ == '__main__':
    # Inicia el navegador un segundo después de que el servidor comience.
    Timer(1, open_browser).start()
    # Usa Waitress para servir la aplicación.
    serve(app, host="127.0.0.1", port=5000)