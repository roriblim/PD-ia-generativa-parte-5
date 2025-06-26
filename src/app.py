import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from agent import VideoAgent
from tools import cortar_transcricao, extrair_url_youtube, extrair_video_id
import os
import logging

LOGGER = logging.getLogger(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

video_agent = VideoAgent(API_KEY)

st.title("Mimiryx - Analisador de Vídeos do YouTube !")
st.info(f"Quer saber algo sobre um vídeo mas está sem poder assisti-lo? Talvez deseja um resumo do que se trata o vídeo? Ou já viu um vídeo mas não lembra um algo que foi falado e deseja saber?")
st.info(f"Experimente o Mimiryx! :)")

url_text = st.text_area("Cole a URL do YouTube")
pergunta_text = st.text_area("Faça uma pergunta ou comando sobre o vídeo :)")

if st.button("Analisar"):
    url = extrair_url_youtube(url_text)
    if not url:
        st.error("Não encontrei URL válida no texto.")
    else:
        video_id = extrair_video_id(url)
        if not video_id:
            st.error("Não consegui extrair o ID do vídeo.")
        else:
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            st.image(thumbnail_url, caption=f"Thumbnail do vídeo de id {video_id}", width=300)

            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR', 'en'])
                transcript_text = " ".join([t['text'] for t in transcript_list])
            except Exception as e:
                st.error(f"Erro ao obter transcrição: {str(e)}")
                transcript_text = None

            if transcript_text:
                transcript_text, cortado = cortar_transcricao(transcript_text)
                if cortado:
                    st.warning("⚠️ A transcrição do vídeo foi cortada para respeitar o limite máximo de tokens.")
                with st.spinner("ID do vídeo encontrado. Carregando a resposta..."):
                    resumo = video_agent.responder_pergunta(transcript_text, pergunta_text)
                st.subheader("Resposta:")
                st.write(resumo)
