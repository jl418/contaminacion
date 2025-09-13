import json
import os
import requests

# Ruta absoluta para dataset en Vercel
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.json")

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer " + HF_TOKEN} if HF_TOKEN else {}

def buscar_dataset(user_message):
    for item in dataset:
        if item["pregunta"].lower() in user_message.lower():
            return item["respuesta"]
    return None

def handler(request, response):
    try:
        body = request.json()
        user_message = body.get("message", "")

        # Buscar primero en dataset
        reply = buscar_dataset(user_message)
        if not reply and HF_TOKEN:
            prompt = f"Eres un experto en contaminación, medio ambiente y cambio climático. Responde siempre en español de manera clara y sencilla.\n\nUsuario: {user_message}\nAsistente:"
            r = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
            data = r.json()

            if isinstance(data, list) and "generated_text" in data[0]:
                reply = data[0]["generated_text"].split("Asistente:")[-1].strip()
            else:
                reply = "Lo siento, no pude obtener respuesta del modelo en este momento."
        
        if not reply:
            reply = "Lo siento, no tengo información sobre eso por ahora."

        return response.json({"reply": reply})
    except Exception as e:
        return response.json({"error": str(e)})
