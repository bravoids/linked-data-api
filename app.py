# app.py
# Proyecto Linked Data - API Flask con interfaz web
# Autor: Héctor Bravo

from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# ==============================
#  CARGA DE DATOS PROCESADOS
# ==============================
data_path = "dataset_procesado.csv"
if os.path.exists(data_path):
    data = pd.read_csv(data_path)
else:
    data = pd.DataFrame()  # Evita error si no existe el CSV

# ==============================
#  RUTA PRINCIPAL (HTML)
# ==============================
@app.route('/')
def home():
    """Muestra la página principal del proyecto Linked Data"""
    return render_template('index.html')

# ==============================
#  RUTA DE INFORMACIÓN GENERAL (API)
# ==============================
@app.route('/api/info')
def api_info():
    """Devuelve un resumen general del dataset procesado"""
    if data.empty:
        return jsonify({"error": "No se encontró el archivo 'dataset_procesado.csv'"}), 404

    return jsonify({
        "proyecto": "Linked Data - Análisis de Patrones",
        "total_registros": len(data),
        "columnas": list(data.columns),
        "clusters_detectados": int(data['cluster'].nunique()) if 'cluster' in data.columns else "N/A",
        "mensaje": "API operativa y lista para consultas"
    })

# ==============================
#  RUTA PARA CONSULTAR CLUSTERS
# ==============================
@app.route('/api/cluster/<int:id>')
def get_cluster(id):
    """Muestra ejemplos del cluster solicitado"""
    if data.empty:
        return jsonify({"error": "Datos no disponibles"}), 404

    if 'cluster' not in data.columns:
        return jsonify({"error": "El dataset no contiene la columna 'cluster'"}), 400

    if id not in data['cluster'].unique():
        return jsonify({"error": f"Cluster {id} no encontrado"}), 404

    subset = data[data['cluster'] == id].head(10).to_dict(orient='records')
    return jsonify({"cluster": id, "ejemplos": subset})

# ==============================
#  RUTA PARA VISUALIZAR DATASETS
# ==============================
@app.route('/ver_csv/<nombre>')
def ver_csv(nombre):
    if nombre == "dataset_procesado":
        df = pd.read_csv("dataset_procesado.csv")
    elif nombre == "ISOFV163_A8_Anexo":
        df = pd.read_csv("ISOFV163_A8_Anexo.csv")
    else:
        return "Archivo no encontrado", 404

    return df.to_html(classes='table table-striped', index=False)

# ==============================
#  EJECUCIÓN LOCAL O EN RENDER
# ==============================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)