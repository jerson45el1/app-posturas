# crear_labels.py
import numpy as np

# IMPORTANTE:
# Este es el orden alfabético de las carpetas que probablemente usó
# tu script de entrenamiento. Si el orden es diferente, DEBES
# cambiar esta lista para que coincida.

clases_correctas = np.array([
    "cuclillas",
    "Parado",        # Asumiendo que la carpeta es "de_pie"
    "manos_arriba",
    "manos_costado",
    "sentado"
])

# Guardar el nuevo archivo "diccionario"
np.save('label_encoder.npy', clases_correctas)

print(f"¡Listo! Se creó 'label_encoder.npy' con las 5 etiquetas correctas.")
print(clases_correctas)