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

st.set_page_config(layout="wide")

# Layout de duas colunas (direita um pouco menor)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.title("🎬 Mimiryx - Analisador de Vídeos do YouTube!")
    st.write("Quer saber algo sobre um vídeo mas não pode assisti-lo?")
    st.info("Experimente o Mimiryx! :)")
    url_text = st.text_area("Cole a URL do YouTube")
    pergunta_text = st.text_area("Faça uma pergunta ou comando sobre o vídeo :)")
    analisar = st.button("Analisar")

with col2:
    if analisar:
        url = extrair_url_youtube(url_text)
        if not url:
            st.error("Não encontrei URL válida no texto.")
        else:
            video_id = extrair_video_id(url)
            if not video_id:
                st.error("Não consegui extrair o ID do vídeo.")
            else:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="{thumbnail_url}" width="280" style="border-radius: 10px;" />
                        <p style="font-size: 0.9rem; color: gray;">Thumbnail do vídeo de id {video_id}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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

                    st.markdown(
                            f"""
                            <div style="max-width: 600px; margin: auto; text-align: justify;">
                                <h3 style="text-align: left;">Resposta:</h3>
                                <p style="font-size: 1.05rem; line-height: 1.6;">{resumo}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                            )


