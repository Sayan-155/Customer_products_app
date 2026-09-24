// browse.js -- powers the index/browse page: loads filter options,
// fetches the motorcycle list from the API on every filter change,
// and renders result cards.

const grid = document.getElementById("moto-grid");
const resultCount = document.getElementById("result-count");
const emptyState = document.getElementById("empty-state");

const searchInput = document.getElementById("search-input");
const brandFilter = document.getElementById("brand-filter");
const categoryFilter = document.getElementById("category-filter");
const sortSelect = document.getElementById("sort-select");
const clearBtn = document.getElementById("clear-filters");

let debounceTimer = null;

async function loadMeta() {
  const res = await fetch("/api/meta");
  const meta = await res.json();
  for (const b of meta.brands) {
    const opt = document.createElement("option");
    opt.value = b;
    opt.textContent = b;
    brandFilter.appendChild(opt);
  }
  for (const c of meta.categories) {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    categoryFilter.appendChild(opt);
  }
}

function buildQuery() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.set("q", searchInput.value.trim());
  if (brandFilter.value) params.set("brand", brandFilter.value);
  if (categoryFilter.value) params.set("category", categoryFilter.value);

  const [sort, order] = sortSelect.value.split("-");
  params.set("sort", sort);
  params.set("order", order);
  return params.toString();
}

function cardTemplate(m) {
  const compareIds = getCompareIds();
  const alreadyAdded = compareIds.includes(m.id);
  return `
    <div class="card" data-id="${m.id}">
      <div class="emoji">${m.image_emoji || "🏍️"}</div>
      <span class="cat-tag">${m.category}</span>
      <h3>${m.brand} ${m.model}</h3>
      <div class="spec-row"><span>Engine</span><b>${m.engine_cc} cc</b></div>
      <div class="spec-row"><span>Power</span><b>${m.power_hp} hp</b></div>
      <div class="spec-row"><span>Weight</span><b>${m.weight_kg} kg</b></div>
      <div class="spec-row"><span>Top speed</span><b>${m.top_speed_kmh} km/h</b></div>
      <div class="price">$${m.price_usd.toLocaleString()}</div>
      <div class="card-actions">
        <a class="btn" href="/motorcycle/${m.id}">Details</a>
        <button class="btn ${alreadyAdded ? "added" : "primary"} add-compare-btn" data-id="${m.id}">
          ${alreadyAdded ? "Added ✓" : "+ Compare"}
        </button>
      </div>
    </div>
  `;
}

async function loadMotorcycles() {
  const qs = buildQuery();
  const res = await fetch(`/api/motorcycles?${qs}`);
  const data = await res.json();

  resultCount.textContent = `${data.length} motorcycle${data.length === 1 ? "" : "s"} found`;
  grid.innerHTML = data.map(cardTemplate).join("");
  emptyState.style.display = data.length === 0 ? "block" : "none";

  grid.querySelectorAll(".add-compare-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.id, 10);
      const result = addToCompare(id);
      if (result.ok) {
        btn.textContent = "Added ✓";
        btn.classList.remove("primary");
        btn.classList.add("added");
      } else if (result.reason === "full") {
        alert(`You can compare up to ${MAX_COMPARE} motorcycles at a time. Remove one on the Compare page first.`);
      }
    });
  });
}

function scheduleReload() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(loadMotorcycles, 200);
}

searchInput.addEventListener("input", scheduleReload);
brandFilter.addEventListener("change", loadMotorcycles);
categoryFilter.addEventListener("change", loadMotorcycles);
sortSelect.addEventListener("change", loadMotorcycles);
clearBtn.addEventListener("click", () => {
  searchInput.value = "";
  brandFilter.value = "";
  categoryFilter.value = "";
  sortSelect.value = "brand-asc";
  loadMotorcycles();
});

loadMeta().then(loadMotorcycles);
