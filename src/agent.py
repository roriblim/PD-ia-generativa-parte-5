from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")

# Prompt para responder perguntas
prompt_template = """
Você é um especialista em compreender o conteúdo de vídeos do YouTube a partir das suas transcrições e gerar respostas sobre ele para o usuário. 
Abaixo está a transcrição de um vídeo:
{transcript}

Abaixo está uma pergunta ou comando sobre a transcrição:
{pergunta}

Responda à pergunta de forma clara, objetiva, de fácil compreensão, tendo como base a transcrição e seguindo estas regras:
- Não invente nada que não esteja claro no texto original.
- Mantenha o texto em português.
- Seja sucinto, com no máximo 300 palavras.
- Ignore informações repetidas.
- Se o conteúdo da pergunta estiver vazio, responda "Não encontrei a pergunta."
- Se não encontrar a resposta para a pergunta, responda "Não encontrei resposta para a pergunta feita."

Resposta:

"""

prompt = PromptTemplate(input_variables=["transcript","pergunta"], template=prompt_template)
llm = ChatOpenAI(model="gpt-4o",temperature=0.1,openai_api_key=API_KEY)

chain_analise_video = LLMChain(llm=llm, prompt=prompt, output_key="resumo")