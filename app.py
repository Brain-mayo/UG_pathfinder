import sqlite3                                       # Python's built-in database tool
from flask import Flask, render_template, jsonify   # 👈 jsonify is new

app = Flask(__name__)
DATABASE = "campus.db"       # the database file (created automatically)


# ---------------------------------------------------------------
# Starter places: (name, category, latitude, longitude, hint)
#
# ⚠️ These coordinates are APPROXIMATE guesses. We'll fix them later
#    using a "click the map to get coordinates" trick in Step 5.
#
# Categories: study, class, food, hostel, health, sport, gate
# ---------------------------------------------------------------
STARTER_PLACES = [
    # 📚 Study
    ("Balme Library",        "study", 5.65177, -0.18706, "Big building with a tall tower."),
    ("24 Hour Reading Room", "study", 5.65200, -0.18636, "Open 24 hours. Good for late-night studying."),

    # 🏫 Lecture halls
    ("Great Hall",           "class",  5.65063, -0.19617, "Big hall on top of the hill."),
    ("JQB",                  "class",  5.65230, -0.18198, "Jones Quartey Building. Many lecture rooms."),
    ("Central Cafeteria",    "class",   5.64689, -0.18705, "the on a top floor."),

    #Medical Center
    ("Student Medical Examination Center","health", 5.64702, -0.18732, "Provide medical services to students."),
    

    # 🍲 Food
    ("Night Market",         "food",    5.64247, -0.18629, "Many food sellers. Busy at night."),
    
    # 🛏️ Halls and hostels
    ("Legon Hall",           "hostel", 5.64915, -0.18821, "Hall of residence."),
    ("Akuafo Hall",          "hostel", 5.64913, -0.18593, "Hall of residence."),
    ("Akuafo Hall Annex A",  "hostel",  5.64788, -0.18569, "Hall of residence."),
    ("Akuafo Hall Annex B",  "hostel", 5.64690, -0.18567, "Hall of residence."),
    ("Akuafo Hall Annex C",  "hostel", 5.64738, -0.18528, "Hall of residence."),
    ("Akuafo Hall Annex D",  "hostel", 5.64743, -0.18589, "Hall of residence."),
    ("Commonwealth Hall",    "hostel", 5.65070, -0.19156, "Hall of residence near the hill."),
    ("Mensah Sarbah Hall",   "hostel", 5.64622, -0.18705, "Hall of residence."),
    ("Volta Hall",           "hostel", 5.65146, -0.18937, "Hall of residence."),
    ("Volta Hall Annex",     "hostel", 5.65236, -0.18933, "Hall of residence."),
    ("Jubilee Hall",         "hostel", 5.64042, -0.18596, "Hall of residence."),
    ("Elizabeth Sey Hall",   "hostel",  5.63601, -0.18709, "Hall of residence."),
    ("Dr Hilla Limann Hall",    "hostel", 5.63746, -0.18428, "Hall of residence."),
    ("Alexander Kwapong Hall",    "hostel", 5.63684, -0.18539, "Hall of residence."),
    ("Jean Nelson Aka Hall", "hostel", 5.63546, -0.18822, "Hall of residence."),
    ("Pentagon Hostel Block A", "hostel",5.65745, -0.18235 , "Private hostel."),
    ("Pentagon Hostel Block B", "hostel", 5.65879, -0.18209, "Private hostel."),
    ("Pentagon Hostel Block C", "hostel",5.65822, -0.18088 , "Private hostel."),
    ("Pentagon Adisa Ababa Hostel", "hostel",5.65640, -0.18220, "Private hostel."),
    ("Pentagon Dar es Salaam ", "hostel",5.65642, -0.18182, "Private hostel."),
    ("Pentagon Kampala Hostel", "hostel",5.65640, -0.18103, "Private hostel."),
    ("Pentagon Nairobi Hostel", "hostel",5.65637, -0.18060, "Private hostel."),
    ("Evandy Hostel",        "hostel", 5.66279, -0.18159, "Private hostel."),
    ("TF Hostel",            "hostel", 5.66612, -0.18223, "Private hostel."),
    ("Bani Hostel",          "hostel", 5.66279, -0.17972, "Hostel."),
    ("International Students Hostel 1", "hostel", 5.63981, -0.18504, "ISH. Hostel."),
    ("International Students Hostel 2", "hostel", 5.64157, -0.18598, "ISH. Hostel."),

    # 🏥 Health
    ("UG Hospital",          "health", 5.63239, -0.18605, "Go here if you are sick."),

    # ⚽ Sports
    ("Sports Stadium",       "sport",  5.63913, -0.18008, "Big field with a running track."),
    ("Athletics Track",      "sport",  5.64793, -0.18667, "Where athletes train and compete."),
    ("Athletics Field",      "sport",  5.64830, -0.18713, "Where athletes train and compete."),
    ("Athletic Basketball Court",     "sport",  5.64790, -0.18632, "Where basketball players train and compete."),

    # 🚪 Gates
    ("Main Gate",            "gate",   5.63800, -0.18500, "Main entrance to the university."),
]


def get_db():
    """Open a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row    # lets us use row["name"] instead of row[1]
    return conn


def setup_database():
    """Create the places table, and fill it if it's empty."""
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            category  TEXT NOT NULL,
            lat       REAL NOT NULL,
            lng       REAL NOT NULL,
            hint      TEXT
        )
    """)

    # How many places are already saved?
    count = conn.execute("SELECT COUNT(*) FROM places").fetchone()[0]

    if count == 0:
        conn.executemany(
            "INSERT INTO places (name, category, lat, lng, hint) VALUES (?, ?, ?, ?, ?)",
            STARTER_PLACES,
        )
        conn.commit()      # SAVE the changes (very important!)
        print(f"✅ Added {len(STARTER_PLACES)} places to the database.")

    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/places")
def get_places():
    """Send all the places to the browser as JSON."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM places ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

setup_database()      # create the database when the app starts

if __name__ == "__main__":
    app.run(debug=True)   # ⚠️ Set debug=False in production!