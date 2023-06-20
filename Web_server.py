import os
import sys
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__)

# Rota para listar os arquivos e diretórios no diretório raiz
@app.route('/')
def list_files():
    root_dir = app.config['ROOT_DIR']
    return generate_directory_listing(root_dir)

# Rota para exibir o conteúdo do arquivo
@app.route('/file/<path:path>')
def show_file_content(path):
    root_dir = app.config['ROOT_DIR']
    file_path = os.path.join(root_dir, path)

    if os.path.isfile(file_path):  # Verifica se é um arquivo
        with open(file_path, 'r') as file:
            content = file.read()
            return render_template('file_content.html', content=content)
    else:
        return "Erro: Página não encontrada", 404

# Função para gerar a listagem de arquivos e diretórios em um determinado diretório
def generate_directory_listing(directory):
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        return "Erro: Diretório não encontrado"
    
    file_list = "<ul>"
    for file in files:
        file_path = os.path.join(directory, file)
        file_url = os.path.relpath(file_path, app.config['ROOT_DIR']).replace("\\", "/")  # Gera a URL relativa ao diretório raiz
        if os.path.isdir(file_path):
            file_url += '/'
        file_list += f"<li><a href='/file/{file_url}'>{file}</a></li>"
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
        app.env = 'production'  # Define o ambiente como 'production'
        app.run(host='0.0.0.0', port=port, debug=False)
    except ValueError:
        print("A porta deve ser um número inteiro válido.")
    except OSError as e:
        print(f"Erro ao iniciar o servidor: {e}")
