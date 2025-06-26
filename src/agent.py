import logging
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import LLMChain

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

class AnaliseVideoTemplate:
    def __init__(self):
        self.system_template = """
        Você é um especialista em compreender o conteúdo de vídeos do YouTube a partir das suas transcrições e gerar respostas sobre ele para o usuário. 

        A transcrição do vídeo será fornecida após quatro hashtags, e será seguida de uma pergunta ou comando que também aparecerá após quatro hashtags.

        Sua tarefa é responder à pergunta de forma clara, objetiva e de fácil compreensão, baseando-se apenas na transcrição. 
        Siga estas regras:
        - Não invente nada que não esteja claro no texto original.
        - Mantenha o texto em português.
        - Seja sucinto, com no máximo 300 palavras.
        - Ignore informações repetidas.
        - Se o conteúdo da pergunta estiver vazio, responda "Não encontrei a pergunta."
        - Se não encontrar a resposta para a pergunta, responda "Não encontrei resposta para a pergunta feita."

        Forneça apenas a resposta, sem explicações adicionais.
        """

        self.human_template = """
        #### TRANSCRIÇÃO
        {transcript}

        #### PERGUNTA
        {pergunta}
        """

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([
            self.system_message_prompt,
            self.human_message_prompt
        ])


class VideoAgent:
    def __init__(self, open_ai_key, model="gpt-4o", temperature=0.1):
        self.open_ai_key = open_ai_key
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=self.open_ai_key
        )

    def responder_pergunta(self, transcript, pergunta):
        template = AnaliseVideoTemplate()
        chain = LLMChain(
            llm=self.chat_model,
            prompt=template.chat_prompt,
            output_key="resposta"
        )
        return chain.run({"transcript": transcript, "pergunta": pergunta})


