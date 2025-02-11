import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")  # Nova variável para a chave do Gemini

# Configuração dos Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Inicializa o bot
client = discord.Client(intents=intents)

# Configura o Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# Função para consultar o Gemini
def get_gemini_response(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"❌ Erro no Gemini: {str(e)}"

# Função para obter piadas
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any?lang=pt"
    response = requests.get(url).json()
    
    if response["type"] == "single":
        return response["joke"]
    else:
        return f'{response["setup"]} - {response["delivery"]}'

# Evento quando o bot estiver pronto
@client.event
async def on_ready():
    print(f'Bot está online como {client.user}')

# Evento para detectar mensagens no chat
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Evita que o bot responda a si mesmo

    # Comando !ping
    if message.content == "!ping":
        await message.channel.send("Pong! 🏓")

    # Comando !bolsonaro
    elif message.content == "!bolsonaro":
        await message.channel.send("Mito 🔫")

    # Comando !piu
    elif message.content.lower() == "!piu":
        joke = get_joke()
        await message.channel.send(joke)

    # Comando !pergunta
    elif message.content.startswith("!pergunta"):
        question = message.content[len("!pergunta"):].strip()  # Extrai a pergunta
        
        if not question:
            await message.channel.send("❌ Por favor, faça uma pergunta após o comando!")
            return

        async with message.channel.typing():
            answer = get_gemini_response(question)  # Chama o Gemini
            await message.channel.send(answer[:20])  # Limite de caracteres do Discord

# Inicia o bot
client.run(TOKEN)