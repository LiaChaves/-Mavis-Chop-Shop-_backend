from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import os
from PIL import Image

app = Flask(__name__)
CORS(app)

# Variável global para a sessão
session = None

def get_session():
    global session
    if session is None:
        from rembg import new_session
        # O modelo 'u2netp' é essencial para não travar o Render Free
        session = new_session("u2netp")
    return session

@app.route('/')
def home():
    return jsonify({'status': 'Mavis Online', 'model': 'u2netp'})

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        from rembg import remove
        
        if 'image' not in request.files:
            return jsonify({'error': 'Sem imagem'}), 400
            
        file = request.files['image']
        
        # Abre a imagem e reduz a resolução se for muito grande para economizar RAM
        img = Image.open(file.stream)
        if max(img.size) > 1500:
            img.thumbnail((1500, 1500))
        
        # Processamento com o modelo leve
        output = remove(img, session=get_session())
        
        buf = io.BytesIO()
        output.save(buf, format='PNG')
        buf.seek(0)
        
        return send_file(buf, mimetype='image/png')
        
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        return jsonify({'error': str(e)}), 500
