from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Mavis Background Remover está funcionando!',
        'status': 'online',
        'instructions': 'Envie uma imagem POST para /remove-bg'
    })

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada!'}), 400
            
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado!'}), 400
        
        # Processa a imagem
        input_image = Image.open(file.stream)
        output_image = remove(input_image)
        
        # Salva em memória
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='imagem_sem_fundo_by_mavis.png'
        )
        
    except Exception as e:
        print(f"Erro: {str(e)}")  # Log para debug
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
