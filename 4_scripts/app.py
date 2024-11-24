from flask import Flask, jsonify, abort
import csv
import os

app = Flask(__name__)

def ler_dados_csv(caminho_arquivo):
    dados = []
    try:
        with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            for linha in leitor:
                dados.append(linha)
    except FileNotFoundError:
        return None
    return dados

@app.route('/dados', methods=['GET'])
def get_dados():
    # Caminho absoluto baseado no diretório do script atual
    base_dir = os.path.abspath(os.path.dirname(__file__))
    caminho_csv = os.path.join(base_dir, '..', '3_base_de_upload', 'df_tratada.csv')
    
    if not os.path.exists(caminho_csv):
        abort(404, description=f"Arquivo não encontrado: {caminho_csv}")
    
    dados = ler_dados_csv(caminho_csv)
    
    if dados is None:
        abort(500, description="Erro ao ler o arquivo CSV.")
    
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
