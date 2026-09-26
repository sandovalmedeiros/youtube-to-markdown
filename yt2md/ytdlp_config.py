"""
yt2md.ytdlp_config - Centraliza opções do yt-dlp que destravam YouTube em IP
de datacenter (cookies de sessão logada + servidor PO Token bgutil), para que
TODA chamada YoutubeDL() dentro do yt2md herde o mesmo desbloqueio.
"""
import os

# Cookies Netscape exportados de sessão logada no YouTube do dono da VPS.
# Opcional: se o arquivo ainda não existe, yt-dlp apenas avisa e segue.
YT_COOKIES_FILE = os.environ.get("YT2MD_COOKIES_FILE", "/root/yt-cookies.txt")

# Servidor bgutil-ytdlp-pot-provider (HTTP) rodando local na porta 4416.
YT_POT_BASEURL = os.environ.get("YT2MD_POT_BASEURL", "http://127.0.0.1:4416")


def base_ydl_opts(**extra):
    """Opções-base obrigatórias para qualquer YoutubeDL() do yt2md."""
    opts = {}

    if os.path.isfile(YT_COOKIES_FILE):
        opts["cookiefile"] = YT_COOKIES_FILE

    if YT_POT_BASEURL:
        opts["extractor_args"] = {
            "youtube": {"getpot_bgutil_baseurl": [YT_POT_BASEURL]}
        }

    opts.update(extra)
    return opts
