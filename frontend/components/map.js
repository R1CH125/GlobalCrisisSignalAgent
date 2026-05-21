function scoreColor(score) {
  if (score >= 0.9) return "#ff4d3d";
  if (score >= 0.8) return "#ff7a45";
  if (score >= 0.7) return "#ffb347";
  if (score >= 0.6) return "#ffd166";
  if (score >= 0.3) return "#9dd76a";
  return "#4ed487";
}

function project(latitude, longitude) {
  const x = ((longitude + 180) / 360) * 940 + 30;
  const y = ((90 - latitude) / 180) * 440 + 20;
  return { x, y };
}

export function renderMap(root, regions) {
  const markers = regions
    .map((region) => {
      const { x, y } = project(region.lat ?? region.latitude ?? 0, region.lon ?? region.longitude ?? 0);
      const color = scoreColor(region.score || 0);
      const radius = 8 + Math.round((region.score || 0) * 10);
      return `
        <g class="marker">
          <circle cx="${x}" cy="${y}" r="${radius}" fill="${color}" fill-opacity="0.82"></circle>
          <circle cx="${x}" cy="${y}" r="${radius + 8}" fill="none" stroke="${color}" stroke-opacity="0.24"></circle>
          <text x="${x + 12}" y="${y - 10}" fill="#e6f0fa" font-size="12" font-family="Menlo, monospace">${region.region}</text>
          <text x="${x + 12}" y="${y + 8}" fill="${color}" font-size="11" font-family="Menlo, monospace">score ${Number(region.score || 0).toFixed(2)}</text>
        </g>
      `;
    })
    .join("");

  root.innerHTML = `
    <svg viewBox="0 0 1000 500" role="img" aria-label="Global crisis map">
      <defs>
        <linearGradient id="ocean" x1="0" x2="1">
          <stop offset="0%" stop-color="#0a1623"></stop>
          <stop offset="100%" stop-color="#10263f"></stop>
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="1000" height="500" rx="24" fill="url(#ocean)"></rect>
      <path d="M98 142l82-44 116 26 79-26 95 51 65-12 91 42 85-23 66 58-13 54-83 23-29 47-127 16-90-24-86 21-114-33-79-65z" fill="#163149" stroke="#335a79" stroke-width="2"></path>
      <path d="M206 290l68 26 54 61-25 48-82-12-54-71 16-42z" fill="#163149" stroke="#335a79" stroke-width="2"></path>
      <path d="M718 300l76 18 54 65-30 58-99-17-42-70z" fill="#163149" stroke="#335a79" stroke-width="2"></path>
      <path d="M794 131l60-17 69 34-35 47-56 9-45-27z" fill="#163149" stroke="#335a79" stroke-width="2"></path>
      ${markers}
    </svg>
    <div class="map-legend">
      <span><i style="background:#4ed487"></i>0.0-0.3</span>
      <span><i style="background:#9dd76a"></i>0.3-0.6</span>
      <span><i style="background:#ffd166"></i>0.6-0.7</span>
      <span><i style="background:#ffb347"></i>0.7-0.8</span>
      <span><i style="background:#ff7a45"></i>0.8-0.9</span>
      <span><i style="background:#ff4d3d"></i>0.9-1.0</span>
    </div>
  `;
}
