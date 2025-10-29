#!/usr/bin/env python3
from datetime import datetime

# Parse booking data
bookings = [
    {"name": "Diaz Evelyn", "cabin": 1, "checkin": "2025-10-31", "checkout": "2025-11-01"},
    {"name": "Skrypnik Andrea", "cabin": 6, "checkin": "2025-10-31", "checkout": "2025-11-01"},
    {"name": "Nahal Maria", "cabin": 5, "checkin": "2025-11-01", "checkout": "2025-11-02"},
    {"name": "Saez Laura (1)", "cabin": 6, "checkin": "2025-11-20", "checkout": "2025-11-26"},
    {"name": "Saez Laura (2)", "cabin": 7, "checkin": "2025-11-20", "checkout": "2025-11-26"},
    {"name": "Saez Laura (3)", "cabin": 8, "checkin": "2025-11-20", "checkout": "2025-11-26"},
    {"name": "Perez Daniela", "cabin": 1, "checkin": "2025-11-21", "checkout": "2025-11-23"},
    {"name": "Zalieckas Juan", "cabin": 1, "checkin": "2025-11-22", "checkout": "2025-11-29", "people": 2},  # CONFLICTO
    {"name": "Perez Daniel (1)", "cabin": 1, "checkin": "2025-12-29", "checkout": "2026-01-07"},
    {"name": "Perez Daniel (2)", "cabin": 3, "checkin": "2025-12-29", "checkout": "2026-01-07"},
    {"name": "Barale Eugenia", "cabin": 2, "checkin": "2026-01-03", "checkout": "2026-01-07"},
    {"name": "Pascual Pamela", "cabin": 3, "checkin": "2026-01-05", "checkout": "2026-01-08", "people": 4},  # CONFLICTO
    {"name": "Peragallo Paula", "cabin": 3, "checkin": "2026-01-09", "checkout": "2026-01-22"},
    {"name": "Cura Maximiliano", "cabin": 1, "checkin": "2026-01-10", "checkout": "2026-01-16"},
    {"name": "Roza Vanina", "cabin": 2, "checkin": "2026-01-12", "checkout": "2026-01-19"},
    {"name": "Gomez Luciano", "cabin": 7, "checkin": "2026-01-19", "checkout": "2026-01-23"},
    {"name": "Benítez Daniela", "cabin": 2, "checkin": "2026-01-20", "checkout": "2026-01-24"},
    {"name": "Gutierrez Sonia", "cabin": 5, "checkin": "2026-01-21", "checkout": "2026-01-26"},
    {"name": "Fassi Melisa", "cabin": 2, "checkin": "2026-01-25", "checkout": "2026-01-30"},
]

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def dates_overlap(start1, end1, start2, end2):
    """Check if two date ranges overlap"""
    return start1 <= end2 and start2 <= end1

# Check availability for Zalieckas (22-nov to 29-nov)
print("=" * 60)
print("ZALIECKAS JUAN (22-nov a 29-nov, 2 personas)")
print("Necesita cabaña 1-4 (más grandes)")
print("=" * 60)

zalieckas_start = parse_date("2025-11-22")
zalieckas_end = parse_date("2025-11-29")

for cabin in [1, 2, 3, 4]:
    conflicts_found = []
    for booking in bookings:
        if booking["cabin"] == cabin and booking["name"] != "Zalieckas Juan":
            start = parse_date(booking["checkin"])
            end = parse_date(booking["checkout"])
            if dates_overlap(start, end, zalieckas_start, zalieckas_end):
                conflicts_found.append(booking["name"])
    
    if not conflicts_found:
        print(f"✅ Cabaña {cabin}: DISPONIBLE")
    else:
        print(f"❌ Cabaña {cabin}: OCUPADA por {', '.join(conflicts_found)}")

# Check availability for Pascual Pamela (5-ene to 8-ene)
print("\n" + "=" * 60)
print("PASCUAL PAMELA (5-ene a 8-ene, 4 personas)")
print("Necesita cabaña 1-4 (más grandes)")
print("=" * 60)

pascual_start = parse_date("2026-01-05")
pascual_end = parse_date("2026-01-08")

for cabin in [1, 2, 3, 4]:
    conflicts_found = []
    for booking in bookings:
        if booking["cabin"] == cabin and booking["name"] != "Pascual Pamela":
            start = parse_date(booking["checkin"])
            end = parse_date(booking["checkout"])
            if dates_overlap(start, end, pascual_start, pascual_end):
                conflicts_found.append(booking["name"])
    
    if not conflicts_found:
        print(f"✅ Cabaña {cabin}: DISPONIBLE")
    else:
        print(f"❌ Cabaña {cabin}: OCUPADA por {', '.join(conflicts_found)}")

