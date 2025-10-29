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
    {"apellido": "Zalieckas", "nombre": "Juan Jose", "checkin": "2025-11-22", "checkout": "2025-11-29", "cabin": 2, "observaciones": ""},
    {"apellido": "Perez", "nombre": "Daniel", "checkin": "2025-12-29", "checkout": "2026-01-07", "cabin": 1, "observaciones": "Es cliente"},
    {"apellido": "Perez", "nombre": "Daniel", "checkin": "2025-12-29", "checkout": "2026-01-07", "cabin": 3, "observaciones": "Es cliente"},
    {"apellido": "Barale", "nombre": "Eugenia", "checkin": "2026-01-03", "checkout": "2026-01-07", "cabin": 2, "observaciones": ""},
    {"apellido": "Pascual", "nombre": "Pamela", "checkin": "2026-01-05", "checkout": "2026-01-08", "cabin": 4, "observaciones": ""},
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

def dates_overlap_or_adjacent(start1, end1, start2, end2):
    """Check if two date ranges overlap or are adjacent (touch)"""
    # Adjacent means one ends the day before the other starts
    return start1 <= end2 + timedelta(days=1) and start2 <= end1 + timedelta(days=1)

# Assign colors to bookings
booking_colors = {}
for i in range(len(bookings)):
    b1 = bookings[i]
    start1 = parse_date(b1["checkin"])
    end1 = parse_date(b1["checkout"])
    
    # Find colors used by adjacent bookings in same cabin
    used_colors = set()
    for j in range(i):
        if booking_colors[j] is None:
            continue
        b2 = bookings[j]
        if b1["cabin"] != b2["cabin"]:
            continue
        start2 = parse_date(b2["checkin"])
        end2 = parse_date(b2["checkout"])
        if dates_overlap_or_adjacent(start1, end1, start2, end2):
            used_colors.add(booking_colors[j])
    
    # Choose first available color
    for color in COLORS:
        if color not in used_colors:
            booking_colors[i] = color
            break
    if booking_colors[i] is None:
        booking_colors[i] = COLORS[0]  # Fallback

# Read the file
with open('index2026.php', 'r') as f:
    content = f.read()

# Remove all existing color rules first
content = re.sub(r'#[a-z0-9_]+ \{[^}]+\}\n', '', content)

# Process each booking
for idx, booking in enumerate(bookings):
    cabin = booking["cabin"]
    checkin = booking["checkin"]
    checkout = booking["checkout"]
    
    # Build tooltip text
    tooltip = f"{booking['apellido']} {booking['nombre']} {booking['observaciones']}".strip()
    chosen_color = booking_colors[idx]
    
    # Get all dates for this booking
    start_date = parse_date(checkin)
    end_date = parse_date(checkout)
    current_date = start_date
    
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day
        
        # Only process if date is within calendar range
        if (year == 2025 and month >= 11) or (year == 2026 and month <= 2):
            cell_id = f"cab{cabin}_{year}_{month}_{day}"
            
            # Update or add title attribute
            pattern_without_title = f"<td id='{cell_id}'>"
            pattern_with_title = re.compile(f"<td id='{re.escape(cell_id)}' title='[^']*'>")
            
            if pattern_without_title in content:
                content = content.replace(pattern_without_title, f"<td id='{cell_id}' title='{tooltip}'>", 1)
            elif pattern_with_title.search(content):
                content = pattern_with_title.sub(f"<td id='{cell_id}' title='{tooltip}'>", content, count=1)
            
            # Add CSS color rule
            css_rule = f"#{cell_id} {{\n    background-color: {chosen_color};\n}}"
            # Check if rule already exists
            if f"#{cell_id} {{" not in content:
                style_end = content.find('</style>')
                if style_end != -1:
                    content = content[:style_end] + css_rule + '\n' + content[style_end:]
        
        current_date += timedelta(days=1)

# Write the updated content
with open('index2026.php', 'w') as f:
    f.write(content)

print(f"✅ Procesadas {len(bookings)} reservas")
print(f"✅ Colores asignados: {set(booking_colors.values())}")

