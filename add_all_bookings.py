#!/usr/bin/env python3
from datetime import datetime, timedelta
import re

# Paleta de 6 colores pastel
COLORS = [
    "#FFE5B4",  # Beige claro
    "#B4E5FF",  # Azul claro
    "#D4FFD4",  # Verde claro
    "#FFD4FF",  # Rosa claro
    "#E5D4FF",  # Morado claro
    "#FFFFD4",  # Amarillo claro
]

# Reservas con los cambios aplicados
bookings = [
    {"apellido": "Diaz", "nombre": "Evelyn", "checkin": "2025-10-31", "checkout": "2025-11-01", "cabin": 1, "observaciones": ""},
    {"apellido": "Skrypnik", "nombre": "Andrea Roxana", "checkin": "2025-10-31", "checkout": "2025-11-01", "cabin": 6, "observaciones": ""},
    {"apellido": "Nahal", "nombre": "Maria Laura", "checkin": "2025-11-01", "checkout": "2025-11-02", "cabin": 5, "observaciones": ""},
    {"apellido": "Saez", "nombre": "Laura", "checkin": "2025-11-20", "checkout": "2025-11-26", "cabin": 6, "observaciones": "son 3 parejas amigas. pidio 2 arriba 1 abajo"},
    {"apellido": "Saez", "nombre": "Laura", "checkin": "2025-11-20", "checkout": "2025-11-26", "cabin": 7, "observaciones": ""},
    {"apellido": "Saez", "nombre": "Laura", "checkin": "2025-11-20", "checkout": "2025-11-26", "cabin": 8, "observaciones": ""},
    {"apellido": "Perez", "nombre": "Daniela", "checkin": "2025-11-21", "checkout": "2025-11-23", "cabin": 1, "observaciones": ""},
    {"apellido": "Zalieckas", "nombre": "Juan Jose", "checkin": "2025-11-22", "checkout": "2025-11-29", "cabin": 2, "observaciones": ""},  # CAMBIO
    {"apellido": "Perez", "nombre": "Daniel", "checkin": "2025-12-29", "checkout": "2026-01-07", "cabin": 1, "observaciones": "Es cliente"},
    {"apellido": "Perez", "nombre": "Daniel", "checkin": "2025-12-29", "checkout": "2026-01-07", "cabin": 3, "observaciones": "Es cliente"},
    {"apellido": "Barale", "nombre": "Eugenia", "checkin": "2026-01-03", "checkout": "2026-01-07", "cabin": 2, "observaciones": ""},
    {"apellido": "Pascual", "nombre": "Pamela", "checkin": "2026-01-05", "checkout": "2026-01-08", "cabin": 4, "observaciones": ""},  # CAMBIO
    {"apellido": "Peragallo", "nombre": "Paula", "checkin": "2026-01-09", "checkout": "2026-01-22", "cabin": 3, "observaciones": "Es cliente. Cabana 3 pide siempre"},
    {"apellido": "Cura", "nombre": "Maximiliano", "checkin": "2026-01-10", "checkout": "2026-01-16", "cabin": 1, "observaciones": ""},
    {"apellido": "Roza", "nombre": "Vanina", "checkin": "2026-01-12", "checkout": "2026-01-19", "cabin": 2, "observaciones": "Es cliente. Estuvo en chiquita. ahora vienen con los hijos"},
    {"apellido": "Gomez", "nombre": "Luciano", "checkin": "2026-01-19", "checkout": "2026-01-23", "cabin": 7, "observaciones": ""},
    {"apellido": "Benítez", "nombre": "Daniela", "checkin": "2026-01-20", "checkout": "2026-01-24", "cabin": 2, "observaciones": ""},
    {"apellido": "Gutierrez", "nombre": "Sonia", "checkin": "2026-01-21", "checkout": "2026-01-26", "cabin": 5, "observaciones": ""},
    {"apellido": "Fassi", "nombre": "Melisa", "checkin": "2026-01-25", "checkout": "2026-01-30", "cabin": 2, "observaciones": ""},
]

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def get_all_dates(checkin, checkout):
    """Get all dates in range (inclusive)"""
    start = parse_date(checkin)
    end = parse_date(checkout)
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates

# Read the file
with open('index2026.php', 'r') as f:
    content = f.read()

# Track color assignments per cabin and date to ensure adjacent bookings have different colors
cabin_date_colors = {}  # {cabin: {date: [used_colors]}}

# Process each booking
for booking in bookings:
    cabin = booking["cabin"]
    checkin = booking["checkin"]
    checkout = booking["checkout"]
    
    # Build tooltip text
    tooltip = f"{booking['apellido']} {booking['nombre']} {booking['observaciones']}".strip()
    
    # Get all dates for this booking
    dates = get_all_dates(checkin, checkout)
    
    # Find available color for this booking (check adjacent dates)
    used_colors = set()
    for date in dates:
        if cabin not in cabin_date_colors:
            cabin_date_colors[cabin] = {}
        if date in cabin_date_colors[cabin]:
            used_colors.update(cabin_date_colors[cabin][date])
    
    # Choose a color that's not used by adjacent bookings
    available_colors = [c for c in COLORS if c not in used_colors]
    if not available_colors:
        # If all colors are used, use the first one (shouldn't happen with 6 colors)
        chosen_color = COLORS[0]
    else:
        chosen_color = available_colors[0]
    
    # Process each date in the booking
    for date in dates:
        year = date.year
        month = date.month
        day = date.day
        
        # Only process if date is within calendar range (Nov 2025 - Feb 2026)
        if (year == 2025 and month >= 11) or (year == 2026 and month <= 2):
            cell_id = f"cab{cabin}_{year}_{month}_{day}"
            
            # Find the cell in the content
            pattern = f'<td id=\'{cell_id}\'>'
            replacement = f'<td id=\'{cell_id}\' title=\'{tooltip}\'>'
            
            if pattern in content:
                content = content.replace(pattern, replacement, 1)
                
                # Add CSS color rule if not exists
                css_rule = f"#{cell_id} {{\n    background-color: {chosen_color};\n}}"
                if css_rule.split('\n')[0] not in content:
                    # Find the style section and add before closing tag
                    style_end = content.find('</style>')
                    if style_end != -1:
                        content = content[:style_end] + css_rule + '\n' + content[style_end:]
                
                # Track this color for this cabin and date
                if cabin not in cabin_date_colors:
                    cabin_date_colors[cabin] = {}
                if date not in cabin_date_colors[cabin]:
                    cabin_date_colors[cabin][date] = []
                cabin_date_colors[cabin][date].append(chosen_color)

# Write the updated content
with open('index2026.php', 'w') as f:
    f.write(content)

print(f"✅ Procesadas {len(bookings)} reservas")
print(f"✅ Colores asignados desde paleta de {len(COLORS)} colores pastel")

