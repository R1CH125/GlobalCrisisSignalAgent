import { renderBreakdown } from "/components/breakdown.js";
import { renderFeed } from "/components/feed.js";
import { renderMap } from "/components/map.js";

const state = {
  reports: [],
  alerts: [],
  regions: [],
  mode: "demo",
};

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function hydrateRegionCoordinates(reports) {
  return reports.map((report) => ({
    region: report.region,
    level: report.alert_level,
    score: report.crisis_score,
    lat: report.latitude || (report.region === "Northern Kenya" ? 3.52 : 0),
    lon: report.longitude || (report.region === "Northern Kenya" ? 37.62 : 0),
  }));
}

function updateHeader() {
  document.getElementById("reportCount").textContent = state.reports.length;
  document.getElementById("alertCount").textContent = state.alerts.length;
  document.getElementById("modeValue").textContent = state.mode;
  document.getElementById("topRegion").textContent = state.reports[0]?.region || "Awaiting scan";
}

function renderDashboard() {
  updateHeader();
  renderMap(document.getElementById("mapRoot"), state.regions);
  renderFeed(document.getElementById("feedRoot"), state.alerts);
  renderBreakdown(document.getElementById("breakdownRoot"), state.reports[0]);
}

async function loadDashboard() {
  const payload = await fetchJson("/api/dashboard");
  state.reports = payload.reports || [];
  state.alerts = payload.alerts || [];
  state.mode = payload.mode || "demo";
  state.regions = payload.reports?.length ? hydrateRegionCoordinates(payload.reports) : [];
  renderDashboard();

  if (!state.reports.length && state.mode === "demo") {
    await triggerDemo();
  }
}

async function triggerDemo() {
  await fetchJson("/api/demo", { method: "POST" });
  await loadDashboard();
}

async function triggerCycle() {
  await fetchJson("/api/run-once", { method: "POST" });
  await loadDashboard();
}

document.getElementById("runDemoButton").addEventListener("click", triggerDemo);

loadDashboard();
window.setInterval(loadDashboard, 10000);
