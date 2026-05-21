function renderFeedItem(alert) {
  const report = alert.report || {};
  return `
    <article class="feed-item">
      <div class="feed-meta">${report.created_at || "pending"} | ${report.alert_level || "Unscored"}</div>
      <h3>${report.region || "No region"} | score ${report.crisis_score ?? "0.0"}</h3>
      <p>${(report.crisis_type || []).join(", ") || "No classification yet"}</p>
      <p>${(report.signals || []).slice(0, 2).join(" | ")}</p>
    </article>
  `;
}

export function renderFeed(root, alerts) {
  if (!alerts.length) {
    root.innerHTML = `<div class="empty-state">No alerts have fired yet. Run the demo or a monitoring cycle.</div>`;
    return;
  }
  root.innerHTML = alerts.slice(0, 8).map(renderFeedItem).join("");
}
