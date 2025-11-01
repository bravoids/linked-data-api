# api_linked_data.py
# API Flask para mostrar resultados del análisis Linked Data
# Autor: Héctor Bravo

from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar datos procesados
data = pd.read_csv("dataset_procesado.csv")

@app.route('/')
def home():
    return jsonify({
        "mensaje": "API del Proyecto Linked Data",
        "total_registros": len(data),
        "columnas": list(data.columns),
        "clusters_detectados": int(data['cluster'].nunique())
    })

@app.route('/cluster/<int:id>')
def get_cluster(id):
    if id not in data['cluster'].unique():
        return jsonify({"error": "Cluster no encontrado"}), 404
    subset = data[data['cluster'] == id].head(10).to_dict(orient='records')
    return jsonify({"cluster": id, "ejemplos": subset})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)