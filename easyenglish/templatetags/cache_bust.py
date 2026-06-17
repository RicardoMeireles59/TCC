"""Cache-busting para arquivos estáticos (sem build step / Manifest storage).

Acrescenta `?v=<mtime>` na URL do static, baseado na data de modificação do
arquivo em disco. Assim, toda vez que um CSS/JS é editado, o navegador busca
a versão nova automaticamente — sem precisar de Ctrl+Shift+R manual.
"""
import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def static_v(path):
    url = static(path)
    try:
        absolute_path = finders.find(path)
        if absolute_path:
            version = int(os.path.getmtime(absolute_path))
            return f"{url}?v={version}"
    except Exception:
        pass
    return url
