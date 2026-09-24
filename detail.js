// detail.js -- fetches and renders a single motorcycle's full spec sheet.

const root = document.getElementById("detail-root");
const motoId = parseInt(root.dataset.motoId, 10);

const SPEC_FIELDS = [
  ["Year", "year", ""],
  ["Category", "category", ""],
  ["Engine", "engine_cc", " cc"],
  ["Cylinders", "cylinders", ""],
  ["Power", "power_hp", " hp"],
  ["Torque", "torque_nm", " Nm"],
  ["Top speed", "top_speed_kmh", " km/h"],
  ["Weight", "weight_kg", " kg"],
  ["Seat height", "seat_height_mm", " mm"],
  ["Fuel capacity", "fuel_capacity_l", " L"],
  ["Mileage", "mileage_kmpl", " km/l"],
  ["Transmission", "transmission", ""],
  ["ABS", "abs", ""],
];

async function loadDetail() {
  const res = await fetch(`/api/motorcycles/${motoId}`);
  if (!res.ok) {
    root.innerHTML = `<p class="muted">Motorcycle not found.</p>`;
    return;
  }
  const m = await res.json();

  const specCards = SPEC_FIELDS.map(
    ([label, key, suffix]) => `
      <div class="spec-card">
        <div class="label">${label}</div>
        <div class="value">${m[key] ?? "—"}${m[key] != null ? suffix : ""}</div>
      </div>`
  ).join("");

  root.innerHTML = `
    <div class="detail-head">
      <div class="emoji">${m.image_emoji || "🏍️"}</div>
      <div>
        <h1>${m.brand} ${m.model}</h1>
        <span class="cat-tag">${m.category}</span>
      </div>
    </div>
    <div class="spec-card" style="max-width:260px;">
      <div class="label">Price</div>
      <div class="value">$${m.price_usd.toLocaleString()}</div>
    </div>
    <div class="spec-grid">${specCards}</div>
    <div class="card-actions" style="max-width:300px; margin-top:24px;">
      <button class="btn primary" id="add-compare-detail">+ Add to compare</button>
      <a class="btn" href="/compare">Go to compare</a>
    </div>
  `;

  document.getElementById("add-compare-detail").addEventListener("click", (e) => {
    const result = addToCompare(m.id);
    if (result.ok) {
      e.target.textContent = "Added ✓";
    } else if (result.reason === "full") {
      alert(`You can compare up to ${MAX_COMPARE} motorcycles at a time.`);
    } else {
      e.target.textContent = "Already added ✓";
    }
  });
}

loadDetail();
