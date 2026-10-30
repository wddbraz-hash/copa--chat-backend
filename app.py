import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)  # Permite requisições do seu frontend

# Insira sua chave da Groq aqui ou configure via Variável de Ambiente (GROQ_API_KEY)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "SUA_CHAVE_GROQ_AQUI")
MODELO=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

client = Groq(api_key=GROQ_API_KEY)

@app.route('/api/perguntar', methods=['POST'])
def perguntar_copa():
    dados = request.get_json()
    pergunta_usuario = dados.get('pergunta', '').strip()

    if not pergunta_usuario:
        return jsonify({"erro": "A pergunta não pode estar vazia."}), 400

    try:
        chat_completion = client.chat.completions.create(
            model=MODELO,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um historiador especialista em futebol e Copa do Mundo FIFA. Responda em português do Brasil de forma clara, direta e objetiva. Se a pergunta não for sobre futebol/Copa do Mundo, responda educadamente que é especializado apenas em história da Copa do Mundo."
                },
                {
                    "role": "user",
                    "content": pergunta_usuario
                }
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        resposta_ia = chat_completion.choices[0].message.content
        return jsonify({"resposta": resposta_ia})

    except Exception as e:
        print(f"Erro na API Groq: {e}")
        return jsonify({"erro": "Ocorreu um erro ao processar sua solicitação com a inteligência artificial."}), 500

if __name__ == '__main__':
    # Roda o servidor local na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)