#!/usr/bin/env python3
from datetime import datetime, timedelta

# Parse booking data
bookings = [
    {"name": "Diaz Evelyn", "cabin": 1, "checkin": "2025-10-31", "checkout": "2025-11-01"},
    {"name": "Skrypnik Andrea", "cabin": 6, "checkin": "2025-10-31", "checkout": "2025-11-01"},
    {"name": "Nahal Maria", "cabin": 5, "checkin": "2025-11-01", "checkout": "2025-11-02"},
    {"name": "Saez Laura (1)", "cabin": 6, "checkin": "2025-11-20", "checkout": "2025-11-26"},
    {"name": "Saez Laura (2)", "cabin": 7, "checkin": "2025-11-20", "checkout": "2025-11-26"},
    {"name": "Saez Laura (3)", "cabin": 8, "checkin": "2025-11-20", "checkout": "2025-11-26"},
    {"name": "Perez Daniela", "cabin": 1, "checkin": "2025-11-21", "checkout": "2025-11-23"},
    {"name": "Zalieckas Juan", "cabin": 1, "checkin": "2025-11-22", "checkout": "2025-11-29"},
    {"name": "Perez Daniel (1)", "cabin": 1, "checkin": "2025-12-29", "checkout": "2026-01-07"},
    {"name": "Perez Daniel (2)", "cabin": 3, "checkin": "2025-12-29", "checkout": "2026-01-07"},
    {"name": "Barale Eugenia", "cabin": 2, "checkin": "2026-01-03", "checkout": "2026-01-07"},
    {"name": "Pascual Pamela", "cabin": 3, "checkin": "2026-01-05", "checkout": "2026-01-08"},
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
    # Note: checkout date is inclusive (last day of stay)
    return start1 <= end2 and start2 <= end1

# Group bookings by cabin
by_cabin = {}
for booking in bookings:
    cabin = booking["cabin"]
    if cabin not in by_cabin:
        by_cabin[cabin] = []
    by_cabin[cabin].append(booking)

# Find conflicts
conflicts = []
for cabin, cabin_bookings in by_cabin.items():
    if len(cabin_bookings) < 2:
        continue
    
    for i in range(len(cabin_bookings)):
        for j in range(i + 1, len(cabin_bookings)):
            b1 = cabin_bookings[i]
            b2 = cabin_bookings[j]
            
            start1 = parse_date(b1["checkin"])
            end1 = parse_date(b1["checkout"])
            start2 = parse_date(b2["checkin"])
            end2 = parse_date(b2["checkout"])
            
            if dates_overlap(start1, end1, start2, end2):
                conflicts.append({
                    "cabin": cabin,
                    "booking1": b1["name"],
                    "dates1": f"{b1['checkin']} a {b1['checkout']}",
                    "booking2": b2["name"],
                    "dates2": f"{b2['checkin']} a {b2['checkout']}",
                })

# Print results
if conflicts:
    print("CONFLICTOS ENCONTRADOS:\n")
    for conflict in conflicts:
        print(f"Cabaña {conflict['cabin']}:")
        print(f"  - {conflict['booking1']}: {conflict['dates1']}")
        print(f"  - {conflict['booking2']}: {conflict['dates2']}")
        print()
else:
    print("No se encontraron conflictos. Todas las reservas pueden agregarse.")

