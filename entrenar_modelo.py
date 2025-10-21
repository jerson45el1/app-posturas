# entrenar_modelo.py
import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# --- CONFIGURACIÓN ---
DATA_DIR = 'dataset'
IMG_SIZE = 64 # Usaremos imágenes más pequeñas para ahorrar memoria
# --------------------

data = []
labels = []
clases = os.listdir(DATA_DIR)
# Filtramos para asegurarnos de que solo procesamos carpetas
clases = [d for d in clases if os.path.isdir(os.path.join(DATA_DIR, d))]
NUM_CLASES = len(clases)

if NUM_CLASES == 0:
    print("Error: La carpeta 'dataset' está vacía o no contiene subcarpetas.")
    exit()

print(f"Cargando {NUM_CLASES} clases: {clases}")

for clase in clases:
    path = os.path.join(DATA_DIR, clase)
    for img_name in os.listdir(path):
        try:
            img_path = os.path.join(path, img_name)
            # Cargar en escala de grises (1 canal)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            data.append(img_resized)
            labels.append(clase)
        except Exception as e:
            print(f"Error cargando imagen {img_path}: {e}")

# Convertir a numpy arrays y normalizar (0 a 1)
data = np.array(data, dtype="float") / 255.0
data = data.reshape(data.shape[0], IMG_SIZE, IMG_SIZE, 1) # Shape para Keras (1 canal)
labels = np.array(labels)

# Codificar etiquetas
le = LabelEncoder()
labels_encoded = le.fit_transform(labels)
labels_categorical = to_categorical(labels_encoded)

# Guardar el codificador de etiquetas
np.save('label_encoder.npy', le.classes_)

# Dividir datos en entrenamiento y prueba
(trainX, testX, trainY, testY) = train_test_split(data, labels_categorical, test_size=0.20, stratify=labels_categorical, random_state=42)

# --- Construcción del Modelo CNN Ligero ---
print("Construyendo el modelo CNN ligero...")
model = Sequential()
model.add(Input(shape=(IMG_SIZE, IMG_SIZE, 1)))

model.add(Conv2D(32, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(NUM_CLASES, activation="softmax")) # Capa de salida

# Compilar el modelo
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.summary()

# --- Entrenamiento ---
print("Entrenando el modelo...")
model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=32, epochs=25, verbose=1)

# --- Guardar el Modelo ---
# Guardamos en el formato .keras que es más robusto
print("Guardando el modelo entrenado en 'clasif_posturas.keras'...")
model.save('clasif_posturas.keras')

print("¡Entrenamiento completado!")