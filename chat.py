import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")  # se obtiene de las variables de entorno en Vercel
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def handler(request, response):
    try:
        body = request.json()
        user_message = body.get("message", "")

        prompt = f"Eres un experto en contaminación, medio ambiente y cambio climático. Responde siempre en español de manera clara y sencilla.\n\nUsuario: {user_message}\nAsistente:"

        data = {"inputs": prompt}
        r = requests.post(API_URL, headers=headers, json=data)
        result = r.json()

        # Extraer respuesta
        reply = result[0]["generated_text"].split("Asistente:")[-1].strip()

        return response.json({"reply": reply})
    except Exception as e:
        return response.json({"error": str(e)})
