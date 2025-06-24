import os
import re

root_dir = os.path.dirname(os.path.abspath(__file__))

def add_class(tag, class_name):
    # Si el tag ya tiene class, añade la clase solo si no está presente
    if 'class="' in tag:
        if class_name not in tag:
            return re.sub(r'class="([^"]*)"', rf'class="\1 {class_name}"', tag)
        else:
            return tag
    else:
        return tag.replace('>', f' class="{class_name}">', 1)

for dirpath, _, files in os.walk(root_dir):
    for filename in files:
        if filename.lower().endswith('.html'):
            path = os.path.join(dirpath, filename)
            with open(path, encoding="utf-8") as f:
                html = f.read()

            original = html

            # Actualizar todos los <button ...>
            def button_repl(m):
                return add_class(m.group(0), "iptools-btn")
            html = re.sub(r'<button\b[^>]*>', button_repl, html)

            # Actualizar todos los <input type="submit" ...>
            def input_repl(m):
                return add_class(m.group(0), "iptools-btn")
            html = re.sub(r'<input\b[^>]*type=["\']submit["\'][^>]*>', input_repl, html, flags=re.IGNORECASE)

            # Actualizar los enlaces de volver a index.html
            def volver_repl(m):
                return add_class(m.group(0), "volver")
            html = re.sub(r'<a\b[^>]*href=["\'][^"\']*index\.html["\'][^>]*>', volver_repl, html, flags=re.IGNORECASE)

            if html != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Actualizado: {path}")

print("\n¡Todos los botones y 'Volver' están actualizados con las clases correctas!")
