import os
import sys
from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def list_files():
    root_dir = app.config['ROOT_DIR']
    return generate_directory_listing(root_dir)

@app.route('/<path:path>')
def download_file(path):
    root_dir = app.config['ROOT_DIR']
    file_path = os.path.join(root_dir, path)

    if os.path.isfile(file_path):
        return send_from_directory(root_dir, path, as_attachment=True)
    elif os.path.isdir(file_path):
        return generate_directory_listing(file_path)
    else:
        return "Erro: Página não encontrada", 404

@app.route('/HEADER')
def show_header():
    headers = request.headers  # Obtém o cabeçalho da requisição
    return str(headers)

def generate_directory_listing(directory):
    files = os.listdir(directory)
    file_list = "<ul>"
    for file in files:
        file_path = os.path.join(directory, file)
        file_url = file_path.replace(app.config['ROOT_DIR'], '', 1).lstrip('/')
        if os.path.isdir(file_path):
            file += '/'
        file_list += f"<li><a href='{file_url}'>{file}</a></li>"
    file_list += "</ul>"
    return file_list

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 http_server.py <porta> <diretório>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        root_dir = sys.argv[2]
        if not os.path.isdir(root_dir):
            print("Diretório inválido.")
            sys.exit(1)
        app.config['ROOT_DIR'] = os.path.abspath(root_dir)
        app.run(port=port)
    except ValueError:
        print("A porta deve ser um número inteiro válido.")
    except OSError as e:
        print(f"Erro ao iniciar o servidor: {e}")

