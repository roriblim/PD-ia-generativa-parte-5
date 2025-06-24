import re
from urllib.parse import urlparse, parse_qs
import tiktoken

MAX_TOKENS = 20000

def extrair_url_youtube(texto):
    padrao = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+)'
    urls = re.findall(padrao, texto)
    return urls[0] if urls else None


def extrair_video_id(url):
    # 1. Tenta extrair com padrão youtu.be/ID
    match = re.match(r'(https?://)?(www\.)?youtu\.be/([^?&]+)', url)
    if match:
        return match.group(3)
    # 2. Tenta extrair com padrão youtube.com/watch?v=ID
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            query = parse_qs(parsed_url.query)
            return query.get("v", [None])[0]
        # 3. Tenta extrair com padrão /embed/ID
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]
        # 4. Tenta extrair com padrão /v/ID
        elif parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]

    return None


def cortar_transcricao(texto, modelo="gpt-4o", max_tokens=MAX_TOKENS):
    encoding = tiktoken.encoding_for_model(modelo)
    tokens = encoding.encode(texto)
    if len(tokens) > max_tokens:
        tokens_cortados = tokens[:max_tokens]
        texto_cortado = encoding.decode(tokens_cortados)
        return texto_cortado, True
    return texto, False