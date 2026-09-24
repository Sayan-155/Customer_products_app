# MotoCompare

A local, full-stack Python app for browsing and comparing motorcycles.
**This is a local-only tool** — it's built to run on your own machine with
`python app.py` and Flask's built-in dev server. It isn't set up for
deployment (no production WSGI server, no auth, no HTTPS, no environment
config), by design.

## Stack

- **Backend:** Flask (Python), REST API
- **Database:** SQLite (single local file, auto-created and seeded on first run)
- **Frontend:** Server-rendered HTML (Jinja2 templates) + vanilla JS calling the API
- **Data:** ~45 motorcycles across 12 brands (Honda, Yamaha, Kawasaki, Suzuki,
  Ducati, Harley-Davidson, Royal Enfield, KTM, BMW, Triumph, Aprilia), with
  approximate/representative specs for demo purposes. Edit `seed_data.py`
  to correct, add, or remove entries — it's just a plain Python list.

## Features

- Browse all motorcycles as cards, with search, brand/category filters, and sorting
- Full spec detail page for each motorcycle
- Compare up to 4 motorcycles side by side, with the best value in each
  spec row (price, power, weight, top speed, mileage) highlighted
- The "compare list" is kept in your browser's localStorage, so it
  persists as you navigate between pages

## Setup

```bash
cd motoapp
python -m venv venv          # optional but recommended
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The first time it runs, it will automatically create `motorcycles.db`
and seed it with the catalog in `seed_data.py`. To start over with fresh
data, just delete `motorcycles.db` and restart the app.

## Project structure

```
motoapp/
├── app.py              # Flask app: page routes + REST API
├── database.py          # SQLite connection + schema
├── seed_data.py          # Motorcycle catalog (edit this to change data)
├── requirements.txt
├── templates/
│   ├── base.html         # Shared layout/nav
│   ├── index.html        # Browse page
│   ├── detail.html        # Single motorcycle page
│   └── compare.html      # Side-by-side comparison page
└── static/
    ├── css/style.css
    └── js/
        ├── main.js         # Shared compare-list logic (localStorage)
        ├── browse.js        # Browse page: filters, search, sort
        ├── detail.js        # Detail page rendering
        └── compare.js        # Comparison table rendering
```

## API reference

| Endpoint | Description |
|---|---|
| `GET /api/motorcycles` | List motorcycles. Supports `q`, `brand`, `category`, `min_price`, `max_price`, `min_cc`, `max_cc`, `sort`, `order` |
| `GET /api/motorcycles/<id>` | Full spec for one motorcycle |
| `GET /api/compare?ids=1,2,3` | Records for the given ids, in order |
| `GET /api/meta` | Distinct brands/categories, price range (for filter dropdowns) |

## Extending it

- Add more bikes: append tuples to `MOTORCYCLES` in `seed_data.py`, delete
  `motorcycles.db`, and restart.
- Add a new spec field: add the column in `database.py`'s `SCHEMA`, extend
  the tuples in `seed_data.py`, and add it to `SPEC_FIELDS` in
  `static/js/detail.js` and/or `COMPARE_ROWS` in `static/js/compare.js`.
- Swap in real-time data: replace `seed_data.py` with calls to a
  motorcycle-spec API or a scraper of your choice, on a schedule you control.
