"""
app.py
Flask backend for the Motorcycle Compare app.

Run locally with:
    python app.py
Then open http://127.0.0.1:5000 in a browser.

This app is intentionally built to run ONLY on localhost -- it uses
Flask's built-in dev server, a local SQLite file, and has no auth,
HTTPS, or environment config. It is a local tool, not something meant
to be pushed to a production host.
"""

from flask import Flask, jsonify, render_template, request
from database import get_connection, init_db, is_empty
import seed_data

app = Flask(__name__)


def row_to_dict(row):
    return dict(row)


def ensure_db_ready():
    init_db()
    if is_empty():
        seed_data.seed()


# ---------------------------------------------------------------- pages ----

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/motorcycle/<int:moto_id>")
def detail_page(moto_id):
    return render_template("detail.html", moto_id=moto_id)


@app.route("/compare")
def compare_page():
    return render_template("compare.html")


# ------------------------------------------------------------------ API ----

@app.route("/api/motorcycles")
def api_list_motorcycles():
    """
    List motorcycles with optional filtering, sorting, and search.
    Query params:
      q=          free-text search on brand/model
      brand=
      category=
      min_price= / max_price=
      min_cc=    / max_cc=
      sort=       one of price_usd, power_hp, weight_kg, top_speed_kmh,
                  mileage_kmpl, engine_cc, year (default: brand)
      order=      asc | desc (default asc)
    """
    conn = get_connection()

    clauses = []
    params = []

    q = request.args.get("q", "").strip()
    if q:
        clauses.append("(brand LIKE ? OR model LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])

    brand = request.args.get("brand", "").strip()
    if brand:
        clauses.append("brand = ?")
        params.append(brand)

    category = request.args.get("category", "").strip()
    if category:
        clauses.append("category = ?")
        params.append(category)

    for field, param_name, op in [
        ("price_usd", "min_price", ">="),
        ("price_usd", "max_price", "<="),
        ("engine_cc", "min_cc", ">="),
        ("engine_cc", "max_cc", "<="),
    ]:
        val = request.args.get(param_name)
        if val:
            try:
                clauses.append(f"{field} {op} ?")
                params.append(float(val))
            except ValueError:
                pass

    allowed_sort = {
        "price_usd", "power_hp", "weight_kg", "top_speed_kmh",
        "mileage_kmpl", "engine_cc", "year", "brand", "model",
    }
    sort = request.args.get("sort", "brand")
    if sort not in allowed_sort:
        sort = "brand"
    order = "DESC" if request.args.get("order", "asc").lower() == "desc" else "ASC"

    sql = "SELECT * FROM motorcycles"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += f" ORDER BY {sort} {order}, model ASC"

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/motorcycles/<int:moto_id>")
def api_get_motorcycle(moto_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM motorcycles WHERE id = ?", (moto_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(row_to_dict(row))


@app.route("/api/compare")
def api_compare():
    """?ids=1,2,3 -- returns full records for those ids, in that order."""
    ids_param = request.args.get("ids", "")
    ids = [int(i) for i in ids_param.split(",") if i.strip().isdigit()]
    if not ids:
        return jsonify([])

    conn = get_connection()
    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"SELECT * FROM motorcycles WHERE id IN ({placeholders})", ids
    ).fetchall()
    conn.close()

    by_id = {r["id"]: row_to_dict(r) for r in rows}
    ordered = [by_id[i] for i in ids if i in by_id]
    return jsonify(ordered)


@app.route("/api/meta")
def api_meta():
    """Distinct brands/categories, for populating filter dropdowns."""
    conn = get_connection()
    brands = [r[0] for r in conn.execute("SELECT DISTINCT brand FROM motorcycles ORDER BY brand")]
    categories = [r[0] for r in conn.execute("SELECT DISTINCT category FROM motorcycles ORDER BY category")]
    price_range = conn.execute("SELECT MIN(price_usd), MAX(price_usd) FROM motorcycles").fetchone()
    conn.close()
    return jsonify({
        "brands": brands,
        "categories": categories,
        "min_price": price_range[0],
        "max_price": price_range[1],
    })


if __name__ == "__main__":
    ensure_db_ready()
    app.run(debug=True, host="127.0.0.1", port=5000)
