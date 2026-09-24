// main.js -- shared helpers used on every page.
// The "compare list" (which bike ids the user picked) is kept in
// localStorage so it survives navigation between pages.

const COMPARE_KEY = "moto_compare_ids";
const MAX_COMPARE = 4;

function getCompareIds() {
  try {
    const raw = localStorage.getItem(COMPARE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function setCompareIds(ids) {
  localStorage.setItem(COMPARE_KEY, JSON.stringify(ids));
  updateCompareBadge();
}

function addToCompare(id) {
  const ids = getCompareIds();
  if (ids.includes(id)) return { ok: false, reason: "already-added" };
  if (ids.length >= MAX_COMPARE) return { ok: false, reason: "full" };
  ids.push(id);
  setCompareIds(ids);
  return { ok: true };
}

function removeFromCompare(id) {
  setCompareIds(getCompareIds().filter((x) => x !== id));
}

function updateCompareBadge() {
  const badge = document.getElementById("compare-count-badge");
  if (!badge) return;
  const count = getCompareIds().length;
  badge.textContent = count;
  badge.style.display = count > 0 ? "inline-block" : "none";
}

document.addEventListener("DOMContentLoaded", updateCompareBadge);
