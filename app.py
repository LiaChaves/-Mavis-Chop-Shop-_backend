from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

# --- MUDANÇA IMPORTANTE AQUI ---
# Não carregamos a sessão agora. Deixamos como None.
# Isso permite que o Gunicorn inicie o servidor IMEDIATAMENTE.
model_session = None

@app.route('/')
def home():
    return jsonify({
        'message': '✂️ Mavis Chop Shop Backend Online!',
        'status': 'Aguardando cortes...'
    })

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    global model_session
    
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada!'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado!'}), 400

        # --- CARREGAMENTO PREGUIÇOSO (LAZY LOADING) ---
        # A IA só carrega na primeira vez que alguém usa.
        if model_session is None:
            print("⏳ Carregando modelo de IA pela primeira vez... (pode demorar um pouco)")
            # Usamos o modelo 'u2netp' (leve) para não estourar a memória
            model_session = new_session("u2netp")
            print("✅ Modelo carregado!")

        input_image = Image.open(file.stream)
        
        # Processa a imagem usando a sessão carregada
        output_image = remove(input_image, session=model_session)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='mavis_recorte.png'
        )
        
    except Exception as e:
        print(f"Erro no servidor: {str(e)}")
        # Se der erro de memória, resetamos a sessão para tentar de novo limpo na próxima
        model_session = None 
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
