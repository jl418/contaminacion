import json
import os
import requests

# Cargar dataset
with open("api/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def buscar_dataset(user_message):
    for item in dataset:
        if item["pregunta"].lower() in user_message.lower():
            return item["respuesta"]
    return None

def handler(request, response):
    try:
        body = request.json()
        user_message = body.get("message", "")

        # Primero revisar dataset
        reply = buscar_dataset(user_message)
        if not reply:
            # Si no hay coincidencia, usar Hugging Face
            prompt = f"Eres un experto en contaminación, medio ambiente y cambio climático. Responde siempre en español de manera clara y sencilla.\n\nUsuario: {user_message}\nAsistente:"
            r = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            data = r.json()
            reply = data[0]["generated_text"].split("Asistente:")[-1].strip()

        return response.json({"reply": reply})
    except Exception as e:
        return response.json({"error": str(e)})
