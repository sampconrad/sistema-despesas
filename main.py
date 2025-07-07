import os
import sys
import webbrowser
import threading
import time
from flask import Flask, send_from_directory
from flask_cors import CORS

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
    if hasattr(sys, '_MEIPASS'):
        base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

api_path = os.path.join(base_dir, 'sistema-despesas-api')
sys.path.insert(0, api_path)

try:
    from app import app as flask_app
except ImportError as e:
    print(f"Erro ao importar app: {e}")
    print(f"API path: {api_path}")
    print(f"Files in API path: {os.listdir(api_path) if os.path.exists(api_path) else 'Path not found'}")
    sys.exit(1)

client_dir = base_dir

print(f"Base directory: {base_dir}")
print(f"Client directory: {client_dir}")
print(f"Files in client directory: {os.listdir(client_dir) if os.path.exists(client_dir) else 'Directory not found'}")

app = Flask(__name__, static_folder=client_dir)
CORS(app)

for rule in flask_app.url_map.iter_rules():
    endpoint = rule.endpoint
    if endpoint != 'static' and endpoint != 'home':
        view_func = flask_app.view_functions[endpoint]
        app.add_url_rule(rule.rule, endpoint, view_func, methods=rule.methods)

@app.route('/')
def serve_index():
    return send_from_directory(client_dir, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if os.path.exists(os.path.join(client_dir, filename)):
        return send_from_directory(client_dir, filename)
    return app.send_static_file(filename)

@app.route('/img/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(client_dir, 'img'), filename)

def open_browser():
    """Abrindo o navegador automaticamente após um pequeno delay"""
    time.sleep(2) 
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("🚀 Iniciando Sistema de Despesas Mensais...")
    print("📱 Abrindo no navegador automaticamente...")
    print("🌐 Se não abrir automaticamente, acesse: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para encerrar o sistema")
    
    app.run(host='0.0.0.0', port=5000, debug=False) 