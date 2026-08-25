// Generates assets/stats.svg from the GitHub GraphQL API.
// Run with --demo to render mock data (no token needed) for local checks.

import { writeFileSync, mkdirSync } from "node:fs";

const LOGIN = process.env.LOGIN || "MuizKmz";
const DEMO = process.argv.includes("--demo");

const QUERY = `query($login:String!){
  user(login:$login){
    followers{ totalCount }
    pullRequests{ totalCount }
    contributionsCollection{ contributionCalendar{ totalContributions } }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      totalCount
      nodes{
        stargazerCount
        languages(first:10, orderBy:{field:SIZE,direction:DESC}){
          edges{ size node{ name color } }
        }
      }
    }
  }
}`;

async function fetchStats() {
  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.GH_TOKEN}`,
      "Content-Type": "application/json",
      "User-Agent": "profile-stats",
    },
    body: JSON.stringify({ query: QUERY, variables: { login: LOGIN } }),
  });
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
  const { data, errors } = await res.json();
  if (errors) throw new Error(JSON.stringify(errors));

  const u = data.user;
  const byLang = new Map();
  let stars = 0;
  for (const repo of u.repositories.nodes) {
    stars += repo.stargazerCount;
    for (const { size, node } of repo.languages.edges) {
      const cur = byLang.get(node.name) || { size: 0, color: node.color };
      cur.size += size;
      byLang.set(node.name, cur);
    }
  }
  const langs = [...byLang.entries()]
    .map(([name, v]) => ({ name, size: v.size, color: v.color || "#7d8590" }))
    .sort((a, b) => b.size - a.size)
    .slice(0, 6);

  return {
    repos: u.repositories.totalCount,
    stars,
    contributions: u.contributionsCollection.contributionCalendar.totalContributions,
    followers: u.followers.totalCount,
    prs: u.pullRequests.totalCount,
    langs,
  };
}

const DEMO_DATA = {
  repos: 6, stars: 3, contributions: 842, followers: 0, prs: 12,
  langs: [
    { name: "TypeScript", size: 52, color: "#3178c6" },
    { name: "JavaScript", size: 24, color: "#f1e05a" },
    { name: "Python",     size: 12, color: "#3572A5" },
    { name: "Vue",        size: 6,  color: "#41b883" },
    { name: "CSS",        size: 4,  color: "#563d7c" },
    { name: "Shell",      size: 2,  color: "#89e051" },
  ],
};

const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;" }[c]));

const fmt = (n) => (n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, "") + "k" : String(n));

function render(d) {
  const MONO = "ui-monospace, SFMono-Regular, 'DejaVu Sans Mono', Menlo, Consolas, monospace";

  const stats = [
    { v: d.repos,         l: "REPOSITORIES", c: "#22d3ee" },
    { v: d.contributions, l: "CONTRIBUTIONS", c: "#a78bfa" },
    { v: d.stars,         l: "STARS EARNED",  c: "#22d3ee" },
    { v: d.prs,           l: "PULL REQUESTS", c: "#a78bfa" },
  ];

  const cells = stats.map((s, i) => {
    const x = 70 + (i % 2) * 210;
    const y = 118 + Math.floor(i / 2) * 62;
    return `  <g class="cell c${i}">
    <text x="${x}" y="${y}" font-size="30" font-weight="700" fill="${s.c}">${esc(fmt(s.v))}</text>
    <text x="${x}" y="${y + 18}" font-size="10" letter-spacing="1.6" fill="#64748b">${s.l}</text>
  </g>`;
  }).join("\n");

  const total = d.langs.reduce((a, l) => a + l.size, 0) || 1;
  const BAR_X = 570, BAR_W = 370, BAR_Y = 104;
  let cursor = BAR_X;
  const segs = d.langs.map((l, i) => {
    const w = Math.max((l.size / total) * BAR_W, 3);
    const seg = `  <rect class="seg s${i}" x="${cursor.toFixed(1)}" y="${BAR_Y}" width="${w.toFixed(1)}" height="12" fill="${esc(l.color)}"/>`;
    cursor += w;
    return seg;
  }).join("\n");

  const legend = d.langs.map((l, i) => {
    const x = BAR_X + (i % 2) * 190;
    const y = 148 + Math.floor(i / 2) * 24;
    const pct = ((l.size / total) * 100).toFixed(1);
    return `  <g class="cell c${i}">
    <circle cx="${x + 4}" cy="${y - 4}" r="4" fill="${esc(l.color)}"/>
    <text x="${x + 16}" y="${y}" font-size="11" fill="#94a3b8">${esc(l.name)} <tspan fill="#475569">${pct}%</tspan></text>
  </g>`;
  }).join("\n");

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240" width="1000" height="240" role="img" aria-label="GitHub statistics for ${esc(LOGIN)}">
<title>GitHub statistics for ${esc(LOGIN)}</title>
<defs>
  <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#080d1a"/><stop offset="0.5" stop-color="#0c1226"/><stop offset="1" stop-color="#080a14"/>
  </linearGradient>
  <linearGradient id="srule" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="300" y2="0">
    <stop offset="0" stop-color="#22d3ee" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#e8fbff" stop-opacity="0.9"/>
    <stop offset="1" stop-color="#22d3ee" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-320 0; 1020 0" dur="4.5s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="barclip"><rect x="${BAR_X}" y="${BAR_Y}" width="${BAR_W}" height="12" rx="6"/></clipPath>
  <style>
    .cell { animation: rise .8s ease-out backwards; }
    .seg  { animation: grow .9s cubic-bezier(.2,.7,.3,1) backwards; transform-box: fill-box; transform-origin: left center; }
    .c0{animation-delay:.05s}.c1{animation-delay:.15s}.c2{animation-delay:.25s}
    .c3{animation-delay:.35s}.c4{animation-delay:.45s}.c5{animation-delay:.55s}
    .s0{animation-delay:.10s}.s1{animation-delay:.20s}.s2{animation-delay:.30s}
    .s3{animation-delay:.40s}.s4{animation-delay:.50s}.s5{animation-delay:.60s}
    @keyframes rise { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:none } }
    @keyframes grow { from { transform:scaleX(0) } to { transform:scaleX(1) } }
    @media (prefers-reduced-motion: reduce) { .cell,.seg { animation:none } }
  </style>
</defs>

<rect width="1000" height="240" rx="16" fill="#090e1c"/>
<rect width="1000" height="240" rx="16" fill="url(#sbg)"/>

<g font-family="${MONO}">
  <text x="70" y="56" font-size="12" letter-spacing="3.4" fill="#5eead4">GITHUB  STATISTICS</text>
  <text x="930" y="56" font-size="12" letter-spacing="1" fill="#475569" text-anchor="end">@${esc(LOGIN)}</text>
  <rect x="70" y="70" width="860" height="1" fill="#1e293b"/>
  <rect x="70" y="69.5" width="860" height="2" fill="url(#srule)"/>

${cells}

  <text x="570" y="88" font-size="10" letter-spacing="1.6" fill="#64748b">TOP LANGUAGES</text>
  <rect x="${BAR_X}" y="${BAR_Y}" width="${BAR_W}" height="12" rx="6" fill="#111a2e"/>
  <g clip-path="url(#barclip)">
${segs}
  </g>
${legend}
</g>
<rect x="0.75" y="0.75" width="998.5" height="238.5" rx="16" fill="none" stroke="#1e293b" stroke-width="1.5"/>
</svg>
`;
}

const data = DEMO ? DEMO_DATA : await fetchStats();
mkdirSync("assets", { recursive: true });
writeFileSync("assets/stats.svg", render(data));
console.log("wrote assets/stats.svg", DEMO ? "(demo data)" : JSON.stringify(data).slice(0, 160));
