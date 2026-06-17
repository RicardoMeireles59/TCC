"""Biblioteca de ícones SVG inline (estilo outline, 24x24) — substitui emojis.

Sem dependência externa: cada ícone é um conjunto de paths/shapes embutido
e renderizado via {% icon "nome" %}.
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    "home": '<path d="M3 11.2 12 4l9 7.2"/><path d="M5 9.8V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9.8"/>',
    "layers": '<rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/>',
    "book-open": '<path d="M2 4.5h6a3.5 3.5 0 0 1 3.5 3.5v13a2.5 2.5 0 0 0-2.5-2.5H2Z"/><path d="M22 4.5h-6A3.5 3.5 0 0 0 12.5 8v13A2.5 2.5 0 0 1 15 18.5h7Z"/>',
    "clock": '<circle cx="12" cy="12" r="9.25"/><path d="M12 7v5l3.5 2"/>',
    "chevrons-left": '<polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/>',
    "chevron-left": '<polyline points="15 18 9 12 15 6"/>',
    "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
    "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
    "user": '<circle cx="12" cy="7.5" r="4"/><path d="M4.5 20.5v-1a7.5 7.5 0 0 1 15 0v1"/>',
    "sun": '<circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v3M12 18.5v3M4.6 4.6l2.1 2.1M17.3 17.3l2.1 2.1M2.5 12h3M18.5 12h3M4.6 19.4l2.1-2.1M17.3 6.7l2.1-2.1"/>',
    "moon": '<path d="M21 13.5A9 9 0 1 1 10.5 3 7.2 7.2 0 0 0 21 13.5Z"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "search": '<circle cx="11" cy="11" r="7.5"/><line x1="21" y1="21" x2="16.2" y2="16.2"/>',
    "filter": '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
    "pencil": '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497Z"/><path d="m15 5 4 4"/>',
    "trash": '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "check-circle": '<path d="M21 11.08V12a9 9 0 1 1-5.34-8.23"/><polyline points="21 4 12 14.01 9 11.01"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "x-circle": '<circle cx="12" cy="12" r="9.25"/><line x1="14.5" y1="9.5" x2="9.5" y2="14.5"/><line x1="9.5" y1="9.5" x2="14.5" y2="14.5"/>',
    "play": '<polygon points="5 3 19 12 5 21 5 3"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11Z"/>',
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "external-link": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "eye-off": '<path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/>',
    "sparkles": '<path d="M9.94 14.06A2 2 0 0 0 8.5 12.6l-4.6-1.2a.5.5 0 0 1 0-.96l4.6-1.18A2 2 0 0 0 9.94 7.8l1.18-4.6a.5.5 0 0 1 .96 0l1.18 4.6a2 2 0 0 0 1.44 1.46l4.6 1.18a.5.5 0 0 1 0 .96l-4.6 1.2a2 2 0 0 0-1.44 1.46l-1.18 4.6a.5.5 0 0 1-.96 0Z"/><path d="M19 4v3M20.5 5.5h-3"/>',
    "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
    "alert-triangle": '<path d="M10.6 3.5 1.8 19a1.5 1.5 0 0 0 1.3 2.25h17.8a1.5 1.5 0 0 0 1.3-2.25L13.4 3.5a1.5 1.5 0 0 0-2.6 0Z"/><line x1="12" y1="9.5" x2="12" y2="13.5"/><line x1="12" y1="17" x2="12" y2="17.01"/>',
}


@register.simple_tag
def icon(name, size=20, css_class=""):
    inner = ICONS.get(name, "")
    klass = f"icon {css_class}".strip()
    return mark_safe(
        f'<svg class="{klass}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
    )
