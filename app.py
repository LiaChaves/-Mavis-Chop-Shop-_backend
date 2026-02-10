from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import os
from PIL import Image

app = Flask(__name__)
CORS(app)

# Variável global para manter a sessão da IA na memória após o primeiro uso
model_session = None

@app.route('/')
def home():
    return jsonify({
        'message': '✂️ Mavis Chop Shop Backend Online!',
        'status': 'Pronta para cortar!'
    })

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    global model_session
    
    try:
        # Importamos o rembg apenas aqui dentro para o servidor ligar rápido
        from rembg import remove, new_session
        
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada!'}), 400
            
        file = request.files['image']
        
        # Carrega o modelo apenas uma vez (Lazy Loading)
        if model_session is None:
            # Usamos o modelo 'u2netp' que é a versão leve para economizar RAM
            model_session = new_session("u2netp")

        input_image = Image.open(file.stream)
        
        # Processamento
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
        print(f"Erro: {str(e)}")
        return jsonify({'error': 'Erro ao processar imagem. Tente uma menor.'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
