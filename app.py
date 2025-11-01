# app.py
# Proyecto Linked Data - API + Análisis de Patrones
# Autor: Héctor Bravo

from flask import Flask, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

# =======================================================
# 1. Función para procesar el dataset
# =======================================================
def procesar_datos():
    csv_file = "ISOFV163_A8_Anexo.csv"

    # Verifica que el archivo exista
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ No se encontró el archivo {csv_file}")

    # Cargar datos
    data = pd.read_csv(csv_file)

    # Limpieza de valores nulos (rellena con el valor anterior válido)
    data = data.ffill()

    # Codificación de columnas tipo texto
    label_encoders = {}
    for column in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le

    # Clustering con K-Means
    n_clusters = 3
    model = KMeans(n_clusters=n_clusters, random_state=42)
    data["cluster"] = model.fit_predict(data.select_dtypes(include=[np.number]))

    # Guardar el dataset procesado
    data.to_csv("dataset_procesado.csv", index=False)
    print("✅ Dataset procesado guardado como 'dataset_procesado.csv'")

    # Visualización básica
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x=data.select_dtypes(include=[np.number]).columns[0],
        y=data.select_dtypes(include=[np.number]).columns[1],
        hue="cluster", palette="viridis", data=data
    )
    plt.title("Patrones de comportamiento (K-Means)")
    plt.savefig("clusters.png")
    plt.close()

    return data


# =======================================================
# 2. Cargar los datos procesados (o generarlos si no existen)
# =======================================================
try:
    if os.path.exists("dataset_procesado.csv"):
        data = pd.read_csv("dataset_procesado.csv")
        print("📄 Se cargó el dataset procesado existente.")
    else:
        print("⚙️ Procesando datos por primera vez...")
        data = procesar_datos()
except Exception as e:
    print(f"❌ Error durante el procesamiento: {e}")
    data = pd.DataFrame()


# =======================================================
# 3. Definición de rutas de la API
# =======================================================

@app.route('/')
def home():
    if data.empty:
        return jsonify({"error": "No hay datos procesados"}), 500

    return jsonify({
        "mensaje": "API del Proyecto Linked Data",
        "total_registros": len(data),
        "columnas": list(data.columns),
        "clusters_detectados": int(data['cluster'].nunique())
    })


@app.route('/cluster/<int:id>')
def get_cluster(id):
    if data.empty:
        return jsonify({"error": "No hay datos procesados"}), 500

    if id not in data['cluster'].unique():
        return jsonify({"error": "Cluster no encontrado"}), 404

    subset = data[data['cluster'] == id].head(10).to_dict(orient='records')
    return jsonify({"cluster": id, "ejemplos": subset})


@app.route('/reprocesar')
def reprocesar():
    """
    Permite reprocesar el dataset manualmente desde la API.
    Por ejemplo: https://linked-data-api.onrender.com/reprocesar
    """
    global data
    try:
        data = procesar_datos()
        return jsonify({"mensaje": "✅ Dataset reprocesado correctamente", "total_registros": len(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =======================================================
# 4. Ejecución del servidor Flask
# =======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
