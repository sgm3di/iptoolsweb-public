import os
import re
from datetime import datetime

# Configuración: ajusta las rutas a tus carpetas de artículos
carpetas = [
    './articulos',        # Artículos en español
    './en/articles'       # Artículos en inglés
]

# Footer legal y script de año
footer = '''
<div class="footer-legal">
  <a href="/politica-cookies.html" target="_blank">Política de cookies</a>
  <a href="/politica-privacidad.html" target="_blank">Privacidad</a>
  <a href="/terminos-condiciones.html" target="_blank">Términos</a>
  <br>
  © <span id="year"></span> IPToolsWeb.io — Herramientas IP &amp; red
</div>
<script>
  document.getElementById('year').textContent = new Date().getFullYear();
</script>
'''

footer_en = '''
<div class="footer-legal">
  <a href="/politica-cookies.html" target="_blank">Cookies Policy</a>
  <a href="/politica-privacidad.html" target="_blank">Privacy</a>
  <a href="/terminos-condiciones.html" target="_blank">Terms</a>
  <br>
  © <span id="year"></span> IPToolsWeb.io — IP &amp; Network Tools
</div>
<script>
  document.getElementById('year').textContent = new Date().getFullYear();
</script>
'''

# CSS retro (puedes ajustarlo si lo cambias en el futuro)
style = '''
  <style>
    article {
      background: #000;
      color: #00FF00;
      font-family: 'Fira Mono', 'IBM Plex Mono', Courier, monospace;
      border: 2px solid #00FF00;
      padding: 2.5rem 1.7rem;
      border-radius: 0;
      max-width: 750px;
      margin: 2.5rem auto 2rem auto;
      box-shadow: 0 0 8px #00FF0040;
    }
    h1, h2, h3 {
      color: #00FF00;
      margin-top: 2rem;
      margin-bottom: 1rem;
      font-family: inherit;
      font-weight: bold;
    }
    h1 {
      text-align: center;
      font-size: 2.0rem;
      margin-bottom: 2rem;
      text-shadow: 0 0 3px #00FF00;
    }
    h2 { font-size: 1.25rem; }
    h3 { font-size: 1.05rem; margin-top: 1.5rem;}
    p, ul, ol {
      color: #00FF00;
      margin-bottom: 1.1rem;
      line-height: 1.6;
      font-size: 1.05rem;
    }
    ul, ol { margin-left: 1.3em;}
    a { color: #00FF00; text-decoration: underline; }
    code {
      background: #111;
      color: #00FF00;
      border: 1px solid #00FF00;
      padding: 0.13em 0.33em;
      border-radius: 0;
      font-size: 1em;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 2.2rem 0 2.2rem 0;
      font-size: 1rem;
      background: transparent;
    }
    th, td {
      border: 1px solid #00FF00;
      padding: 0.65em 0.6em;
      background: rgba(0,255,0,0.05);
      color: #00FF00;
      border-radius: 0;
      font-family: inherit;
      text-align: left;
    }
    th {
      background: rgba(0,255,0,0.12);
      font-weight: bold;
    }
    @media (max-width: 600px) {
      article { padding: 1rem 0.4rem; font-size: 97%; }
      h1 { font-size: 1.2rem; }
      table { font-size: 0.92em;}
    }
    .footer-legal {
      margin: 2.1rem 0 0 0;
      color: #00FF00;
      text-align: center;
      font-size: 1rem;
      opacity: 0.88;
    }
    .footer-legal a { color: #00FF00; margin:0 14px; text-decoration: underline;}
    .volver {
      color:#00FF00; text-decoration:none; font-size:1.3rem;
      border:1px dashed #00FF00; padding:0.38rem 0.92rem; font-family:monospace;
      margin: 2.2rem auto 1.5rem auto; display:inline-block;
      background:transparent;
      border-radius: 0;
      transition: background .15s;
    }
    .volver:hover { background:#00FF0044;}
  </style>
'''

# Plantilla de head en ES/EN
def make_head(titulo, desc, canonical, ogimage, lang='es'):
    hreflang_es = f'https://iptoolsweb.io{canonical}' if lang == 'es' else canonical.replace('/en/', '/')
    hreflang_en = canonical.replace('/articulos/', '/en/articles/').replace('.html', '.html')
    head = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}" />
  <link rel="icon" type="image/png" href="/img/favicon.png" />
  <link rel="stylesheet" href="/style.css" />
  <meta property="og:title" content="{titulo}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{ogimage}" />
  <link rel="alternate" hreflang="es" href="{hreflang_es}" />
  <link rel="alternate" hreflang="en" href="{hreflang_en}" />
  {style}
</head>
<body>
    '''
    return head

# Buscamos h1, description, canonical y preparamos head para cada archivo
for carpeta in carpetas:
    for nombre in os.listdir(carpeta):
        if not nombre.endswith('.html'):
            continue
        ruta = os.path.join(carpeta, nombre)
        with open(ruta, encoding="utf-8") as f:
            html = f.read()

        # Detectar idioma
        lang = 'en' if '/en/' in ruta or 'en' in ruta else 'es'

        # Extraer <h1>
        h1 = re.search(r'<h1.*?>(.*?)</h1>', html, re.DOTALL)
        titulo = h1.group(1).strip() if h1 else 'Artículo IPToolsWeb.io'
        # Meta description si existe
        desc = re.search(r'<meta name="description" content="(.*?)"', html)
        if desc:
            desc = desc.group(1)
        else:
            # Primer <p>
            p1 = re.search(r'<p>(.*?)</p>', html, re.DOTALL)
            desc = p1.group(1).strip()[:160] if p1 else titulo

        # Canonical sugerido
        if lang == 'es':
            canonical = f'https://iptoolsweb.io/articulos/{nombre}'
        else:
            canonical = f'https://iptoolsweb.io/en/articles/{nombre}'

        ogimage = 'https://iptoolsweb.io/img/og-iptoolsweb.png'
        # Footer legal
        ftr = footer_en if lang == 'en' else footer

        # Eliminar head antiguo y body open
        contenido = re.sub(r'<!DOCTYPE html>.*?<body[^>]*>', '', html, flags=re.DOTALL)
        contenido = contenido.strip()
        # Quitar doble article si lo hubiera
        contenido = re.sub(r'</?html.*?>|</?head.*?>|<body.*?>|</body>|</?article.*?>', '', contenido, flags=re.DOTALL).strip()
        # Añadir botón volver arriba del artículo
        volver = '<a href="../blog.html" class="volver">&larr; Volver</a>' if lang == 'es' else '<a href="../../en/blog.html" class="volver">&larr; Back</a>'
        # Armar archivo final
        final = make_head(titulo, desc, canonical, ogimage, lang)
        final += f'<article>\n{volver}\n{contenido}\n</article>\n{ftr}\n</body>\n</html>'

        with open(ruta, 'w', encoding="utf-8") as f:
            f.write(final)
        print(f'Actualizado: {ruta}')

print('\n¡Todos los artículos ahora tienen el estilo retro, head SEO y footer unificados!')
