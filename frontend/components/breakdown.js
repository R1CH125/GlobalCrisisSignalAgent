export function renderBreakdown(root, report) {
  if (!report) {
    root.innerHTML = `<div class="empty-state">No report selected yet.</div>`;
    return;
  }

  const indicators = report.indicators || {};
  const reasoning = report.reasoning || {};
  root.innerHTML = `
    <article class="breakdown-card">
      <h3>${report.region}, ${report.country}</h3>
      <div class="breakdown-metrics">${(report.crisis_type || []).join(", ")} | confidence ${reasoning.confidence ?? report.confidence}</div>
      <div class="metric-row">
        <span class="metric-pill">Score ${report.crisis_score}</span>
        <span class="metric-pill">Spike ${Number(indicators.frequency_spike || 0).toFixed(2)}</span>
        <span class="metric-pill">Multi-source ${Number(indicators.multi_source_confirmation || 0).toFixed(2)}</span>
        <span class="metric-pill">Env corr ${Number(indicators.environmental_correlation || 0).toFixed(2)}</span>
      </div>
      <p>${(indicators.trigger_reasons || []).join(" | ") || "Waiting for trigger reasons."}</p>
      <ul>
        ${(report.signals || []).map((signal) => `<li>${signal}</li>`).join("")}
      </ul>
    </article>
  `;
}
