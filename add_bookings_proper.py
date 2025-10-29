#!/usr/bin/env python3
from datetime import datetime, timedelta
import re

# Paleta de 6 colores pastel
COLORS = [
    "#FFE5B4",  # Beige claro (color 0)
    "#B4E5FF",  # Azul claro (color 1)
    "#D4FFD4",  # Verde claro (color 2)
    "#FFD4FF",  # Rosa claro (color 3)
    "#E5D4FF",  # Morado claro (color 4)
    "#FFFFD4",  # Amarillo claro (color 5)
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
    return start1 <= end2 + timedelta(days=1) and start2 <= end1 + timedelta(days=1)

# Build adjacency graph for each cabin
cabin_bookings = {}  # {cabin: [booking_indices]}
for i, booking in enumerate(bookings):
    cabin = booking["cabin"]
    if cabin not in cabin_bookings:
        cabin_bookings[cabin] = []
    cabin_bookings[cabin].append(i)

# Assign colors using proper graph coloring
booking_colors = {}
for cabin, indices in cabin_bookings.items():
    # Process bookings for this cabin
    for idx in indices:
        booking = bookings[idx]
        start1 = parse_date(booking["checkin"])
        end1 = parse_date(booking["checkout"])
        
        # Find all adjacent bookings in same cabin that already have colors
        used_colors = set()
        for other_idx in indices:
            if other_idx == idx or other_idx not in booking_colors:
                continue
            other_booking = bookings[other_idx]
            start2 = parse_date(other_booking["checkin"])
            end2 = parse_date(other_booking["checkout"])
            if dates_overlap_or_adjacent(start1, end1, start2, end2):
                used_colors.add(booking_colors[other_idx])
        
        # Choose first available color
        for color in COLORS:
            if color not in used_colors:
                booking_colors[idx] = color
                break
        if idx not in booking_colors:
            booking_colors[idx] = COLORS[0]  # Fallback

# Read the file
with open('index2026.php', 'r') as f:
    content = f.read()

# Remove all existing booking color rules (keep month-table rules)
# Find the style section
style_start = content.find('<style type=\'text/css\'>')
style_end = content.find('</style>')
if style_start != -1 and style_end != -1:
    style_content = content[style_start:style_end]
    # Keep the original rules (months-container, month-table)
    new_style = """<style type='text/css'>
.months-container {
    display: flex;
    flex-wrap: nowrap;
}
.month-table {
    margin-right: 10px;
}
.month-table td,
.month-table th {
    text-align: center;
}
"""
    # Add color rules for each booking
    for idx, booking in enumerate(bookings):
        checkin = booking["checkin"]
        checkout = booking["checkout"]
        cabin = booking["cabin"]
        color = booking_colors[idx]
        
        start_date = parse_date(checkin)
        end_date = parse_date(checkout)
        current_date = start_date
        
        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            day = current_date.day
            
            if (year == 2025 and month >= 11) or (year == 2026 and month <= 2):
                cell_id = f"cab{cabin}_{year}_{month}_{day}"
                new_style += f"#{cell_id} {{\n    background-color: {color};\n}}\n"
            
            current_date += timedelta(days=1)
    
    new_style += "</style>"
    content = content[:style_start] + new_style + content[style_end + len('</style>'):]

# Process each booking to add tooltips
for idx, booking in enumerate(bookings):
    cabin = booking["cabin"]
    checkin = booking["checkin"]
    checkout = booking["checkout"]
    
    # Build tooltip text
    tooltip = f"{booking['apellido']} {booking['nombre']} {booking['observaciones']}".strip()
    
    start_date = parse_date(checkin)
    end_date = parse_date(checkout)
    current_date = start_date
    
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day
        
        if (year == 2025 and month >= 11) or (year == 2026 and month <= 2):
            cell_id = f"cab{cabin}_{year}_{month}_{day}"
            
            # Update title attribute
            pattern_without_title = f"<td id='{cell_id}'>"
            pattern_with_title = re.compile(f"<td id='{re.escape(cell_id)}' title='[^']*'>")
            
            if pattern_without_title in content:
                content = content.replace(pattern_without_title, f"<td id='{cell_id}' title='{tooltip}'>", 1)
            elif pattern_with_title.search(content):
                content = pattern_with_title.sub(f"<td id='{cell_id}' title='{tooltip}'>", content, count=1)
        
        current_date += timedelta(days=1)

# Write the updated content
with open('index2026.php', 'w') as f:
    f.write(content)

print(f"✅ Procesadas {len(bookings)} reservas")
print(f"✅ Colores usados: {len(set(booking_colors.values()))} de {len(COLORS)} disponibles")
for i, color in enumerate(COLORS):
    count = list(booking_colors.values()).count(color)
    if count > 0:
        print(f"   - {color}: usado en {count} reserva(s)")

