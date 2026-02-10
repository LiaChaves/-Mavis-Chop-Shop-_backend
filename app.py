from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io
import os

app = Flask(__name__)
# Permite que qualquer origem acesse (necessário para seu front no GitHub Pages funcionar)
CORS(app) 

# Pré-carrega o modelo leve (u2netp) para evitar crash de memória no Render Free
# O modelo padrão é muito pesado para 512MB de RAM
model_name = "u2netp" 
session = new_session(model_name)

@app.route('/')
def home():
    return jsonify({
        'message': '✂️ Mavis Chop Shop Backend Online!',
        'model': model_name
    })

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada!'}), 400
            
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado!'}), 400
        
        # Converte a imagem enviada
        input_image = Image.open(file.stream)
        
        # --- A MÁGICA ACONTECE AQUI ---
        # Usamos a 'session' com o modelo leve
        output_image = remove(input_image, session=session)
        
        # Prepara para devolver
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
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Esta parte só roda se você testar no seu PC. 
    # No Render, o Gunicorn ignora isso e usa o comando do Procfile.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
