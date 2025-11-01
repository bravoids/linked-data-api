# generar_datos.py
# Genera dataset procesado y gráfico de clusters para el proyecto Linked Data
# Autor: Héctor Bravo

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import os

# ==============================
#  CARGA Y LIMPIEZA DE DATOS
# ==============================
csv_file = "ISOFV163_A8_Anexo.csv"
data = pd.read_csv(csv_file)
data = data.ffill()  # Rellenar valores faltantes

# ==============================
#  CODIFICACIÓN DE VARIABLES
# ==============================
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# ==============================
#  CLUSTERING (K-Means)
# ==============================
n_clusters = 3
model = KMeans(n_clusters=n_clusters, random_state=42)
data["cluster"] = model.fit_predict(data.select_dtypes(include=[np.number]))

# ==============================
#  GUARDAR RESULTADOS
# ==============================
data.to_csv("dataset_procesado.csv", index=False)
print("✅ Dataset procesado guardado como 'dataset_procesado.csv'")

# Crear carpeta static si no existe
os.makedirs("static", exist_ok=True)

# ==============================
#  VISUALIZACIÓN
# ==============================
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=data.select_dtypes(include=[np.number]).columns[0],
    y=data.select_dtypes(include=[np.number]).columns[1],
    hue="cluster", palette="viridis", data=data
)
plt.title("Patrones de comportamiento (K-Means)")
plt.savefig("static/clusters.png")
plt.close()
print("✅ Gráfico guardado en 'static/clusters.png'")
