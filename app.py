# app.py
from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2

# Importamos la función de nuestro modelo
from tu_modelo import detectar_postura 

app = Flask(__name__)

@app.route('/')
def index():
    """Ruta principal que muestra la página web."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Recibe la imagen, la procesa con el modelo y devuelve el resultado."""
    
    image_data = request.json['image']
    
    # Decodificar la imagen Base64
    image_data = image_data.split(',')[1]
    decoded_image = base64.b64decode(image_data)
    
    # Convertir a un array de numpy
    np_arr = np.frombuffer(decoded_image, np.uint8)
    
    # Decodificar a una imagen de OpenCV
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # --- ¡AQUÍ SE USA TU MODELO! ---
    resultado = detectar_postura(frame) 
    
    # Devolver el resultado en formato JSON
    return jsonify({'postura': resultado})

if __name__ == '__main__':
    # Esta parte solo se usa cuando ejecutas 'python app.py' en tu PC
    app.run(host='0.0.0.0', port=5000, debug=False)