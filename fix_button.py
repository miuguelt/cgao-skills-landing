import os

file_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the button
old_button = """<button id="mobile-menu-btn" class="md:hidden text-white text-2xl" aria-label="Abrir menú de navegación"
                    title="Menú">"""
new_button = """<button id="mobile-menu-btn" class="md:hidden text-white text-2xl" aria-label="Abrir menú de navegación" title="Menú">"""

# For safety, let's use a simpler match if needed, but let's try exact first.
if old_button in content:
    content = content.replace(old_button, new_button)
else:
    # Try with different spacing/newlines
    import re
    content = re.sub(r'<button id="mobile-menu-btn"[^>]*aria-label="Abrir[^>]*title="Menú">', new_button, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
