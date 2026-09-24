// compare.js -- renders the picker slots and the side-by-side spec table
// for whatever motorcycles are currently in the compare list.

const picker = document.getElementById("compare-picker");
const tableWrap = document.getElementById("compare-table-wrap");

// [label, key, unit, "higher"|"lower" -> which direction counts as "best"]
const COMPARE_ROWS = [
  ["Price", "price_usd", "$", "lower"],
  ["Category", "category", "", null],
  ["Engine", "engine_cc", " cc", null],
  ["Power", "power_hp", " hp", "higher"],
  ["Torque", "torque_nm", " Nm", "higher"],
  ["Top speed", "top_speed_kmh", " km/h", "higher"],
  ["Weight", "weight_kg", " kg", "lower"],
  ["Seat height", "seat_height_mm", " mm", "lower"],
  ["Fuel capacity", "fuel_capacity_l", " L", "higher"],
  ["Mileage", "mileage_kmpl", " km/l", "higher"],
  ["Transmission", "transmission", "", null],
  ["ABS", "abs", "", null],
];

function renderPicker(ids) {
  const slots = [];
  for (let i = 0; i < MAX_COMPARE; i++) {
    if (ids[i] !== undefined) {
      slots.push(`<div class="compare-slot" data-id="${ids[i]}">
        <span id="slot-label-${ids[i]}">Loading…</span>
        <span class="remove" data-id="${ids[i]}">&times;</span>
      </div>`);
    } else {
      slots.push(`<div class="compare-slot"><span class="muted">Empty slot</span></div>`);
    }
  }
  picker.innerHTML = slots.join("");

  picker.querySelectorAll(".remove").forEach((el) => {
    el.addEventListener("click", () => {
      removeFromCompare(parseInt(el.dataset.id, 10));
      init();
    });
  });
}

function bestIndex(values, direction) {
  if (!direction) return -1;
  const nums = values.map((v) => (typeof v === "number" ? v : parseFloat(v)));
  if (nums.some((n) => Number.isNaN(n))) return -1;
  const target = direction === "higher" ? Math.max(...nums) : Math.min(...nums);
  return nums.indexOf(target);
}

function renderTable(motos) {
  if (motos.length === 0) {
    tableWrap.innerHTML = `<p class="muted" id="compare-empty">Add motorcycles from the browse page to compare them.</p>`;
    return;
  }

  let html = `<table class="compare-table"><tbody>`;
  html += `<tr><th>Model</th>${motos.map((m) => `<td>${m.image_emoji || "🏍️"} ${m.brand} ${m.model}</td>`).join("")}</tr>`;

  for (const [label, key, unit, direction] of COMPARE_ROWS) {
    const values = motos.map((m) => m[key]);
    const bestIdx = bestIndex(values, direction);
    html += `<tr><th>${label}</th>`;
    values.forEach((v, i) => {
      const display = key === "price_usd" ? `$${Number(v).toLocaleString()}` : `${v ?? "—"}${v != null ? unit : ""}`;
      html += `<td class="${i === bestIdx ? "best" : ""}">${display}</td>`;
    });
    html += `</tr>`;
  }

  html += `</tbody></table>`;
  html += `<p class="muted" style="margin-top:10px;">Highlighted values mark the best figure in each row (price lower is better; power/speed/mileage higher is better).</p>`;
  tableWrap.innerHTML = html;
}

async function init() {
  const ids = getCompareIds();
  renderPicker(ids);

  if (ids.length === 0) {
    renderTable([]);
    return;
  }

  const res = await fetch(`/api/compare?ids=${ids.join(",")}`);
  const motos = await res.json();

  motos.forEach((m) => {
    const labelEl = document.getElementById(`slot-label-${m.id}`);
    if (labelEl) labelEl.textContent = `${m.brand} ${m.model}`;
  });

  renderTable(motos);
}

init();
