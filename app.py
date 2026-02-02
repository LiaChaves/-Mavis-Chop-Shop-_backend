from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

# Carrega o modelo U2Net uma vez no início
print("=" * 50)
print("Iniciando Mavis Background Remover...")
print("Carregando modelo de IA...")

# Tenta carregar o modelo
try:
    # Força o download do modelo
    from rembg.session_factory import new_session
    model_session = new_session("u2net")
    print("✓ Modelo U2Net carregado com sucesso!")
except Exception as e:
    print(f"✗ Erro ao carregar modelo: {e}")
    model_session = None

print("=" * 50)

@app.route('/')
def home():
    return jsonify({
        'message': 'Mavis Background Remover está funcionando! 🐱✂️',
        'status': 'online',
        'model_loaded': model_session is not None,
        'endpoint': 'POST /remove-bg com multipart/form-data'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model': 'loaded' if model_session else 'not_loaded'
    }), 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        print("Recebendo requisição para remover fundo...")
        
        # Verifica se há arquivo
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada! Envie com key=image'}), 400
            
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado!'}), 400
        
        print(f"Processando: {file.filename} ({file.content_type})")
        
        # Lê a imagem
        image_bytes = file.read()
        
        # Converte para PIL Image
        input_image = Image.open(io.BytesIO(image_bytes))
        print(f"Tamanho original: {input_image.size}")
        
        # Remove fundo
        if model_session:
            output_image = remove(input_image, session=model_session)
        else:
            # Fallback: retorna a imagem original se o modelo não carregou
            output_image = input_image
            print("Aviso: Usando fallback (modelo não carregado)")
        
        # Converte para bytes
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG', optimize=True)
        img_io.seek(0)
        
        print("✓ Fundo removido com sucesso!")
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'mavis_cut_{file.filename}.png'
        )
        
    except Exception as e:
        print(f"✗ ERRO no processamento: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Erro interno no servidor',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint não encontrado', 'path': request.path}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Servidor iniciando na porta {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
