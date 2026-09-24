"""
seed_data.py
Populates motorcycles.db with a representative catalog of bikes
spanning multiple brands and categories, so the app has real data
to browse and compare out of the box.

Specs below are approximate/representative figures for demo purposes
(commonly published class-level specs), not scraped or copied from
any single source. Edit MOTORCYCLES below to add/correct entries.
"""

from database import init_db, get_connection, is_empty

# (brand, model, year, category, engine_cc, cylinders, power_hp, torque_nm,
#  top_speed_kmh, weight_kg, seat_height_mm, fuel_capacity_l, mileage_kmpl,
#  transmission, abs, price_usd, image_emoji)
MOTORCYCLES = [
    ("Honda", "CBR600RR", 2024, "Sport", 599, 4, 118, 66, 260, 194, 820, 18.1, 16, "6-speed", "Yes", 12599, "🏍️"),
    ("Honda", "CB650R", 2024, "Naked", 649, 4, 94, 63, 220, 202, 810, 15.4, 20, "6-speed", "Yes", 9199, "🏍️"),
    ("Honda", "Africa Twin", 2024, "Adventure", 1084, 2, 101, 105, 200, 226, 850, 18.8, 16, "6-speed", "Yes", 14999, "🏍️"),
    ("Honda", "Rebel 500", 2024, "Cruiser", 471, 2, 46, 43, 165, 190, 690, 11.2, 24, "6-speed", "Yes", 6799, "🏍️"),
    ("Honda", "Gold Wing", 2024, "Touring", 1833, 6, 125, 170, 200, 390, 745, 21.1, 13, "7-speed DCT", "Yes", 27500, "🏍️"),
    ("Yamaha", "YZF-R6", 2020, "Sport", 599, 4, 118, 61, 262, 190, 850, 17, 15, "6-speed", "Optional", 12299, "🏍️"),
    ("Yamaha", "MT-07", 2024, "Naked", 689, 2, 73, 67, 210, 184, 805, 14, 22, "6-speed", "Yes", 8199, "🏍️"),
    ("Yamaha", "MT-09", 2024, "Naked", 890, 3, 117, 93, 240, 193, 825, 14, 18, "6-speed", "Yes", 10799, "🏍️"),
    ("Yamaha", "Tenere 700", 2024, "Adventure", 689, 2, 72, 68, 200, 204, 875, 16, 19, "6-speed", "Yes", 10799, "🏍️"),
    ("Yamaha", "V Star 250", 2024, "Cruiser", 249, 2, 21, 20, 130, 158, 690, 10, 30, "5-speed", "No", 4699, "🏍️"),
    ("Kawasaki", "Ninja ZX-6R", 2024, "Sport", 636, 4, 127, 69, 265, 196, 830, 17, 16, "6-speed", "Yes", 11399, "🏍️"),
    ("Kawasaki", "Ninja ZX-10R", 2024, "Sport", 998, 4, 203, 114, 300, 207, 835, 17, 14, "6-speed", "Yes", 17999, "🏍️"),
    ("Kawasaki", "Z900", 2024, "Naked", 948, 4, 123, 99, 240, 212, 820, 17, 17, "6-speed", "Yes", 9399, "🏍️"),
    ("Kawasaki", "Versys 650", 2024, "Adventure", 649, 2, 67, 61, 200, 216, 840, 21, 21, "6-speed", "Yes", 9199, "🏍️"),
    ("Kawasaki", "Vulcan S", 2024, "Cruiser", 649, 2, 61, 63, 180, 226, 705, 14, 22, "6-speed", "No", 7699, "🏍️"),
    ("Suzuki", "GSX-R750", 2024, "Sport", 750, 4, 150, 86, 270, 190, 810, 16, 15, "6-speed", "Yes", 13299, "🏍️"),
    ("Suzuki", "GSX-R1000", 2024, "Sport", 999, 4, 202, 117, 299, 203, 825, 16, 14, "6-speed", "Yes", 16099, "🏍️"),
    ("Suzuki", "SV650", 2024, "Naked", 645, 2, 75, 64, 200, 197, 785, 13.8, 20, "6-speed", "Yes", 7599, "🏍️"),
    ("Suzuki", "V-Strom 650", 2024, "Adventure", 645, 2, 71, 62, 200, 216, 835, 20, 20, "6-speed", "Yes", 9199, "🏍️"),
    ("Suzuki", "Boulevard M109R", 2024, "Cruiser", 1783, 2, 123, 160, 215, 320, 705, 19.5, 15, "5-speed", "No", 14599, "🏍️"),
    ("Ducati", "Panigale V4", 2024, "Sport", 1103, 4, 214, 124, 300, 198, 830, 16, 12, "6-speed", "Yes", 24895, "🏍️"),
    ("Ducati", "Monster 937", 2024, "Naked", 937, 2, 111, 93, 240, 188, 820, 14, 17, "6-speed", "Yes", 12995, "🏍️"),
    ("Ducati", "Multistrada V4", 2024, "Adventure", 1158, 4, 170, 125, 260, 232, 840, 22, 15, "6-speed", "Yes", 24095, "🏍️"),
    ("Ducati", "Diavel V4", 2024, "Cruiser", 1158, 4, 168, 126, 270, 224, 785, 17, 14, "6-speed", "Yes", 26195, "🏍️"),
    ("Harley-Davidson", "Sportster S", 2024, "Cruiser", 1252, 2, 121, 127, 200, 228, 750, 11.8, 16, "6-speed", "Yes", 16999, "🏍️"),
    ("Harley-Davidson", "Fat Boy", 2024, "Cruiser", 1868, 2, 93, 155, 170, 317, 665, 18.9, 13, "6-speed", "Yes", 22499, "🏍️"),
    ("Harley-Davidson", "Road Glide", 2024, "Touring", 1923, 2, 105, 169, 180, 373, 685, 22.7, 14, "6-speed", "Yes", 27999, "🏍️"),
    ("Harley-Davidson", "Nightster", 2024, "Cruiser", 975, 2, 89, 95, 175, 221, 705, 11.7, 17, "6-speed", "Yes", 11249, "🏍️"),
    ("Royal Enfield", "Classic 350", 2024, "Cruiser", 349, 1, 20, 27, 120, 195, 805, 13, 35, "5-speed", "Yes", 4699, "🏍️"),
    ("Royal Enfield", "Himalayan 450", 2024, "Adventure", 452, 1, 40, 40, 150, 196, 825, 17, 30, "6-speed", "Yes", 5799, "🏍️"),
    ("Royal Enfield", "Continental GT 650", 2024, "Sport", 648, 2, 47, 52, 170, 198, 793, 12.5, 25, "6-speed", "Yes", 6399, "🏍️"),
    ("KTM", "390 Duke", 2024, "Naked", 399, 1, 44, 39, 167, 159, 820, 13.4, 28, "6-speed", "Yes", 5799, "🏍️"),
    ("KTM", "890 Duke R", 2024, "Naked", 889, 2, 121, 99, 240, 179, 834, 14, 20, "6-speed", "Yes", 12199, "🏍️"),
    ("KTM", "1290 Super Duke R", 2024, "Naked", 1301, 2, 180, 140, 275, 189, 835, 16, 15, "6-speed", "Yes", 19999, "🏍️"),
    ("KTM", "390 Adventure", 2024, "Adventure", 399, 1, 43, 37, 160, 172, 855, 14.5, 27, "6-speed", "Yes", 7199, "🏍️"),
    ("KTM", "1290 Super Adventure", 2024, "Adventure", 1301, 2, 160, 138, 230, 232, 869, 23, 16, "6-speed", "Yes", 21499, "🏍️"),
    ("BMW", "S 1000 RR", 2024, "Sport", 999, 4, 210, 113, 299, 197, 824, 16.5, 14, "6-speed", "Yes", 17895, "🏍️"),
    ("BMW", "R 1250 GS", 2024, "Adventure", 1254, 2, 136, 143, 220, 249, 850, 20, 17, "6-speed", "Yes", 18895, "🏍️"),
    ("BMW", "F 900 R", 2024, "Naked", 895, 2, 105, 92, 220, 211, 815, 13, 20, "6-speed", "Yes", 9195, "🏍️"),
    ("BMW", "K 1600 GTL", 2024, "Touring", 1649, 6, 160, 175, 220, 348, 750, 26.5, 14, "6-speed", "Yes", 28995, "🏍️"),
    ("Triumph", "Street Triple 765 RS", 2024, "Naked", 765, 3, 128, 80, 250, 189, 825, 15, 18, "6-speed", "Yes", 12595, "🏍️"),
    ("Triumph", "Tiger 900 Rally Pro", 2024, "Adventure", 888, 3, 106, 87, 210, 201, 850, 20, 19, "6-speed", "Yes", 16195, "🏍️"),
    ("Triumph", "Bonneville T120", 2024, "Cruiser", 1200, 2, 79, 105, 190, 224, 790, 14.5, 21, "6-speed", "Yes", 13300, "🏍️"),
    ("Triumph", "Rocket 3 R", 2024, "Cruiser", 2458, 3, 165, 221, 225, 291, 773, 18, 12, "6-speed", "Yes", 22500, "🏍️"),
    ("Aprilia", "RSV4 Factory", 2024, "Sport", 1099, 4, 217, 125, 300, 202, 851, 18.5, 13, "6-speed", "Yes", 26999, "🏍️"),
    ("Aprilia", "Tuono V4", 2024, "Naked", 1077, 4, 175, 121, 260, 191, 825, 18.5, 15, "6-speed", "Yes", 18999, "🏍️"),
]


def seed():
    init_db()
    if not is_empty():
        print("Database already has data -- skipping seed. "
              "Delete motorcycles.db and re-run to reseed.")
        return

    conn = get_connection()
    conn.executemany(
        """
        INSERT INTO motorcycles
        (brand, model, year, category, engine_cc, cylinders, power_hp,
         torque_nm, top_speed_kmh, weight_kg, seat_height_mm,
         fuel_capacity_l, mileage_kmpl, transmission, abs, price_usd, image_emoji)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        MOTORCYCLES,
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM motorcycles").fetchone()[0]
    conn.close()
    print(f"Seeded {count} motorcycles into the database.")


if __name__ == "__main__":
    seed()
