import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from agent import chain_analise_video
from tools import extrair_url_youtube, extrair_video_id


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
            st.info(f"ID do vídeo encontrado. Carregando a resposta...")
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR', 'en'])
                transcript_text = " ".join([t['text'] for t in transcript_list])
            except Exception as e:
                st.error(f"Erro ao obter transcrição: {str(e)}")
                transcript_text = None

            if transcript_text:
                resumo = chain_analise_video.run(transcript=transcript_text, pergunta=pergunta_text)
                st.subheader("Resposta:")
                st.write(resumo)
