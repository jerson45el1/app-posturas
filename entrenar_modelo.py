# entrenar_modelo.py
import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# --- CONFIGURACIÓN ---
DATA_DIR = 'dataset'
IMG_SIZE = 64 # Reducimos el tamaño para un entrenamiento más rápido
# --------------------

data = []
labels = []
clases = os.listdir(DATA_DIR)

print("Cargando imágenes...")
for clase in clases:
    path = os.path.join(DATA_DIR, clase)
    if not os.path.isdir(path):
        continue
    for img_name in os.listdir(path):
        try:
            img_path = os.path.join(path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) # Usar escala de grises
            img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            data.append(img_resized)
            labels.append(clase)
        except Exception as e:
            print(f"Error cargando imagen {img_path}: {e}")

# Convertir a numpy arrays y normalizar
data = np.array(data, dtype="float") / 255.0
data = data.reshape(data.shape[0], IMG_SIZE, IMG_SIZE, 1) # Añadir canal para Keras
labels = np.array(labels)

# Codificar etiquetas (sentado -> 0, de_pie -> 1)
le = LabelEncoder()
labels = le.fit_transform(labels)
labels = to_categorical(labels)

# Guardar el codificador de etiquetas para usarlo después
np.save('label_encoder.npy', le.classes_)

# Dividir datos en entrenamiento y prueba
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.20, stratify=labels, random_state=42)

# --- Construcción del Modelo CNN ---
print("Construyendo el modelo...")
model = Sequential()
model.add(Conv2D(32, (3, 3), padding="same", activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(clases), activation="softmax")) # Capa de salida

# Compilar el modelo
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# --- Entrenamiento ---
print("Entrenando el modelo...")
model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=32, epochs=30, verbose=1)

# --- Guardar el Modelo ---
print("Guardando el modelo entrenado en 'posture_model.h5'...")
# Guardar en el nuevo formato .keras (más robusto)
model.save('clasif_posturas.keras')

print("¡Entrenamiento completado!")