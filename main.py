import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

USUARIOS_PATH = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(USUARIOS_PATH):
        return {}
    with open(USUARIOS_PATH, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(USUARIOS_PATH, "w") as f:
        json.dump(usuarios, f, indent=2)

def iniciar_chat():
    print("👋 Quem está falando?")
    nome = input("🧑 Seu nome: ").strip().capitalize()

    usuarios = carregar_usuarios()

    if nome not in usuarios:
        usuarios[nome] = {
            "mensagens": [
                {"role": "system", "content": f"Você é um assistente pessoal amigável para {nome}."}
            ]
        }
        salvar_usuarios(usuarios)
        print(f"✅ Criado assistente para {nome}.")
    else:
        print(f"👋 Bem-vindo de volta, {nome}!")

    while True:
        entrada = input(f"{nome}: ")
        if entrada.lower() in ['sair', 'exit', 'quit']:
            print("🔚 Até mais!")
            break

        usuarios[nome]["mensagens"].append({"role": "user", "content": entrada})

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=usuarios[nome]["mensagens"]
            )
            texto = response.choices[0].message.content.strip()
            print(f"🤖 ChatGPT: {texto}\n")

            usuarios[nome]["mensagens"].append({"role": "assistant", "content": texto})

            salvar_usuarios(usuarios)

        except Exception as e:
            print(f"⚠️ Erro ao obter resposta: {e}")

if __name__ == "__main__":
    iniciar_chat()
