import os

# Configuración base por tipo de contenido
HEAD_TEMPLATES = {
    "herramienta": """<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - IPToolsWeb.io</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/png" href="../img/favicon.png" />
  <link rel="stylesheet" href="style.css" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{title} - IPToolsWeb.io" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://iptoolsweb.io/img/{image}" />
  <link rel="alternate" hreflang="es" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="{alt}" />
</head>""",

    "noticia": """<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - IPToolsWeb.io</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/png" href="../../img/favicon.png" />
  <link rel="stylesheet" href="../../style.css" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{title} - IPToolsWeb.io" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://iptoolsweb.io/img/{image}" />
  <link rel="alternate" hreflang="es" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="{alt}" />
</head>""",

    "articulo": """<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - IPToolsWeb.io</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/png" href="../../img/favicon.png" />
  <link rel="stylesheet" href="../../style.css" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{title} - IPToolsWeb.io" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://iptoolsweb.io/img/{image}" />
  <link rel="alternate" hreflang="es" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="{alt}" />
</head>"""
}

# Títulos y descripciones básicas por archivo
AUTO_DATA = {
    # Español
    "ping.html": (
        "Ping desde Internet",
        "Comprueba si tu IP o dominio responde desde el exterior con nuestro ping online.",
        "ping-cover.png"
    ),
    "password.html": (
        "Generador de Contraseñas",
        "Crea contraseñas seguras y aleatorias en segundos. Fácil, rápido y gratuito.",
        "password-cover.png"
    ),
    "puertos.html": (
        "Escáner de Puertos",
        "Analiza puertos abiertos en cualquier host con nuestro escáner rápido y gratuito.",
        "puertos-cover.png"
    ),
    "whois.html": (
        "Consulta WHOIS",
        "Obtén la información WHOIS de cualquier dominio. Propietario, fechas, servidores y más.",
        "whois-cover.png"
    ),
    "email-header.html": (
        "Analizador de Cabeceras de Email",
        "Analiza cabeceras de correos electrónicos para detectar IPs, SPF, DKIM, DMARC y más.",
        "email-cover.png"
    ),
    "dns.html": (
        "DNS Checker",
        "Verifica la propagación de registros DNS de cualquier dominio en múltiples servidores.",
        "dns-cover.png"
    ),
    "cidr.html": (
        "Conversor CIDR",
        "Convierte entre notación CIDR y máscara de red de forma sencilla.",
        "cidr-cover.png"
    ),

    # Inglés
    "en/ping.html": (
        "Ping from the Internet",
        "Check if your IP or domain responds from the outside using our online ping tool.",
        "ping-cover.png"
    ),
    "en/password.html": (
        "Password Generator",
        "Create strong and random passwords in seconds. Easy, fast, and free.",
        "password-cover.png"
    ),
    "en/puertos.html": (
        "Port Scanner",
        "Scan open ports on any host with our fast and free port scanner.",
        "puertos-cover.png"
    ),
    "en/whois.html": (
        "WHOIS Lookup",
        "Get WHOIS information for any domain: owner, dates, nameservers and more.",
        "whois-cover.png"
    ),
    "en/email-header.html": (
        "Email Header Analyzer",
        "Analyze email headers to detect IPs, SPF, DKIM, DMARC and more.",
        "email-cover.png"
    ),
    "en/dns.html": (
        "DNS Checker",
        "Check DNS record propagation of any domain across multiple servers.",
        "dns-cover.png"
    ),
    "en/cidr.html": (
        "CIDR Converter",
        "Easily convert between CIDR notation and subnet mask format.",
        "cidr-cover.png"
    )
}


def detectar_tipo_y_ruta(path):
    if "/en/" in path:
        lang = "en"
    else:
        lang = "es"

    if "/noticias/" in path or "/en/news/" in path:
        tipo = "noticia"
    elif "/articulos/" in path or "/en/articles/" in path:
        tipo = "articulo"
    else:
        tipo = "herramienta"

    return tipo, lang

def procesar_html(filepath):
    filename = os.path.basename(filepath)
    tipo, lang = detectar_tipo_y_ruta(filepath)

    if tipo == "herramienta" and filename not in AUTO_DATA:
        print(f"⚠️  No hay datos definidos para {filename}, saltando.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        contenido = f.read()

    inicio_html = contenido.find("<head>")
    fin_head = contenido.find("</head>") + 7
    if inicio_html == -1 or fin_head == -1:
        print(f"❌ {filepath} no tiene HEAD válido")
        return

    if tipo == "herramienta":
        title, desc, image = AUTO_DATA[filename]
        canonical = f"https://iptoolsweb.io/{filename}" if lang == "es" else f"https://iptoolsweb.io/en/{filename}"
        alt = canonical.replace("/en/", "/") if lang == "en" else canonical.replace("iptoolsweb.io/", "iptoolsweb.io/en/")
    else:
        # Noticias y artículos
        slug = filepath.split("/")[-1]
        carpeta = "noticias" if tipo == "noticia" else "articulos"
        canonical = f"https://iptoolsweb.io/{carpeta}/{slug}" if lang == "es" else f"https://iptoolsweb.io/en/{'news' if tipo == 'noticia' else 'articles'}/{slug}"
        alt = canonical.replace("/en/", "/") if lang == "en" else canonical.replace("iptoolsweb.io/", "iptoolsweb.io/en/")
        title = slug.replace(".html", "").replace("-", " ").capitalize()
        desc = f"Lee más sobre: {title}"
        image = "default-cover.png"

    nuevo_head = HEAD_TEMPLATES[tipo].format(
        title=title, description=desc, canonical=canonical, alt=alt, image=image
    )

    contenido_mod = contenido[:inicio_html] + nuevo_head + contenido[fin_head:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(contenido_mod)
    print(f"✅ HEAD actualizado: {filepath}")

def recorrer_archivos():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                procesar_html(os.path.join(root, file))

if __name__ == "__main__":
    recorrer_archivos()
