import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from agent import chain_sumarizacao
from tools import extrair_url_youtube, extrair_video_id




# --- Streamlit UI ---
st.title("Sumarizador de Vídeos do YouTube com SequentialChain")

entrada = st.text_area("Cole um texto com a URL do YouTube que deseja fazer o resumo :)")

if st.button("Gerar resumo"):
    url = extrair_url_youtube(entrada)
    if not url:
        st.error("Não encontrei URL válida no texto.")
    else:
        video_id = extrair_video_id(url)
        if not video_id:
            st.error("Não consegui extrair o ID do vídeo.")
        else:
            st.info(f"ID do vídeo: {video_id}")
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR', 'en'])
                transcript_text = " ".join([t['text'] for t in transcript_list])
            except Exception as e:
                st.error(f"Erro ao obter transcrição: {str(e)}")
                transcript_text = None

            if transcript_text:
                resumo = chain_sumarizacao.run(transcript=transcript_text)
                st.subheader("Resumo:")
                st.write(resumo)
