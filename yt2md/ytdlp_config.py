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

# Congostrinha: extractor arg do POT mudou de nome no yt-dlp 2026.08+
# (o antigo youtube:getpot_bgutil_baseurl foi deprecated e rejeitado).
EXTRACTOR_ARG_POT = os.environ.get(
    "YT2MD_EXTRACTOR_ARG_POT", "youtubepot-bgutilhttp:base_url"
)

# yt-dlp >= 2026.08 pede runtime JS p/ extrair do YouTube.
# Node 24 resolve (deno não existe na VPS). Na CLI o formato é string
# 'RUNTIME[:PATH]'; na API YoutubeDL é dict {'runtime': {'path': ...}}.
JS_RUNTIME_SPEC = os.environ.get("YT2MD_JS_RUNTIME", "node:/root/.hermes/node/bin/node")

# Solver de desafios do player (n-challenge): componentes oficiais baixados
# do github do projeto yt-dlp/ejs (API recebe lista contendo 'ejs:github').
REMOTE_COMPONENTS = os.environ.get("YT2MD_REMOTE_COMPONENTS", "ejs:github")


def _js_runtimes_param(spec):
    """'node:/caminho' (estilo CLI) -> {'node': {'path': '/caminho'}} (API)."""
    if isinstance(spec, dict):
        return spec
    name, sep, path = str(spec).partition(":")
    if not sep or not path:
        return {name: {}}
    return {name: {"path": path}}


def base_ydl_opts(**extra):
    """Opções-base obrigatórias para qualquer YoutubeDL() do yt2md."""
    opts = {}

    if os.path.isfile(YT_COOKIES_FILE):
        opts["cookiefile"] = YT_COOKIES_FILE

    if YT_POT_BASEURL:
        opts["extractor_args"] = {
            "youtube": {EXTRACTOR_ARG_POT: [YT_POT_BASEURL]}
        }

    if JS_RUNTIME_SPEC:
        opts["js_runtimes"] = _js_runtimes_param(JS_RUNTIME_SPEC)

    if REMOTE_COMPONENTS:
        opts["remote_components"] = [
            c.strip() for c in str(REMOTE_COMPONENTS).split(",") if c.strip()
        ]

    opts.update(extra)
    return opts
