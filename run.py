"""Punto de entrada: arranca la interfaz web del agente.

Uso:
    python run.py
Luego abre http://127.0.0.1:5000 en el navegador.
"""
from web.app import app

if __name__ == "__main__":
    print("Agente de Redes en marcha  →  http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
