from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Prompt para sumarização
prompt_template = """
Você é um assistente especialista em resumir vídeos do YouTube a partir das suas transcrições. Abaixo está a transcrição de um vídeo:

{transcript}

Resuma o conteúdo de forma clara, objetiva e seguindo estas regras:
- Não invente nada que não esteja claro no texto original.
- Destaque os pontos principais abordados.
- Mantenha o texto em português.
- Seja sucinto, com no máximo 400 palavras.
- Fale de forma clara, dando preferência a utilizar frases curtas e palavras simplificadas sempre que possível.
- Ignore informações repetidas.
- Deixe explícita qual a opinião do interlocutor sobre o assunto falado no vídeo.

Resumo:
"""

prompt = PromptTemplate(input_variables=["transcript"], template=prompt_template)
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.1,openai_api_key=API_KEY)

chain_sumarizacao = LLMChain(llm=llm, prompt=prompt, output_key="resumo")