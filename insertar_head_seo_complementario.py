import os

DEFAULT_IMAGE = "default-cover.png"
DEFAULT_DESCRIPTION_ES = "Descubre herramientas y recursos técnicos en IPToolsWeb.io."
DEFAULT_DESCRIPTION_EN = "Discover technical tools and resources on IPToolsWeb.io."

def generar_titulo_desde_nombre(nombre):
    nombre = nombre.replace(".html", "").replace("-", " ")
    return nombre.capitalize()

def detectar_idioma_y_tipo(path):
    if "/en/" in path or "privacy" in path or "terms" in path or "cookies" in path:
        lang = "en"
    else:
        lang = "es"

    es_articulo = any(palabra in path.lower() for palabra in [
        "blog", "noticia", "articulo", "retro", "tools", "open", "password", "ip"
    ])
    tipo = "article" if es_articulo else "website"

    return lang, tipo

def insertar_head(filepath):
    filename = os.path.basename(filepath)
    relative_path = filepath.replace(".\\", "").replace("./", "").replace("\\", "/")

    lang, tipo = detectar_idioma_y_tipo(relative_path)
    nombre_corto = os.path.splitext(filename)[0]
    canonical = f"https://iptoolsweb.io/{relative_path}" if lang == "es" else f"https://iptoolsweb.io/{relative_path}"
    alt = canonical.replace("/en/", "/") if lang == "en" else canonical.replace("iptoolsweb.io/", "iptoolsweb.io/en/")
    title = generar_titulo_desde_nombre(nombre_corto)
    description = DEFAULT_DESCRIPTION_EN if lang == "en" else DEFAULT_DESCRIPTION_ES
    favicon_path = "../../img/favicon.png" if "/en/" in relative_path or "/" in relative_path else "../img/favicon.png"
    css_path = "../../style.css" if "/en/" in relative_path or "/" in relative_path else "style.css"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "<head>" in content:
        start = content.find("<head>")
        end = content.find("</head>") + 7
        content = content[:start] + generar_bloque_head(title, description, canonical, alt, tipo, favicon_path, css_path) + content[end:]
    else:
        print(f"❌ HEAD no encontrado en {filepath}")
        return

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ HEAD añadido: {filepath}")

def generar_bloque_head(title, desc, canonical, alt, tipo, favicon_path, css_path):
    return f"""<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - IPToolsWeb.io</title>
  <meta name="description" content="{desc}" />
  <link rel="icon" type="image/png" href="{favicon_path}" />
  <link rel="stylesheet" href="{css_path}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{title} - IPToolsWeb.io" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="{tipo}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://iptoolsweb.io/img/{DEFAULT_IMAGE}" />
  <link rel="alternate" hreflang="es" href="{alt if 'en' in canonical else canonical}" />
  <link rel="alternate" hreflang="en" href="{canonical if 'en' in canonical else alt}" />
</head>"""

def recorrer_fallidos():
    archivos = [
        "404.html", "blog.html", "index.html", "ip.html", "noticias.html",
        "politica-cookies.html", "politica-privacidad.html", "privacidad.html",
        "terminos-condiciones.html", "contraseñas-seguras.html", "cual-es-mi-ip.html",
        "herramientas-red.html", "herramientas-retro.html", "puertos-abiertos.html",
        "en/cookies-policy.html", "en/index.html", "en/ip.html", "en/news.html",
        "en/privacy-policy.html", "en/privacy.html", "en/terms-conditions.html",
        "en/network-tools.html", "en/open-ports.html", "en/retro-tools.html",
        "en/secure-passwords.html", "en/what-is-my-ip.html", "en/ios26.html"
    ]
    for archivo in archivos:
        if os.path.isfile(archivo):
            insertar_head(archivo)
        else:
            print(f"❌ No se encontró el archivo: {archivo}")

if __name__ == "__main__":
    recorrer_fallidos()
