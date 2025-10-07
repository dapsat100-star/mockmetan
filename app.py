# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar (OGMP 2.0 L5 • Metano)
# Limpo: KPIs (sparkline + gauge), abas, sem export/copy, sem “quadrado vermelho”.

from datetime import datetime
from base64 import b64encode
from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — OGMP 2.0 L5", page_icon="🛰️", layout="wide")

# ============== THEME =================
PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

PANEL_W_PX   = 560
PANEL_GAP_PX = 24

# ============== LOGO ==================
logo_uri = ""
p = Path("dapatlas_fundo_branco.png")
if p.exists() and p.stat().st_size > 0:
    logo_uri = "data:image/png;base64," + b64encode(p.read_bytes()).decode("ascii")
logo_html = (
    f"<img src='{logo_uri}' alt='DAP ATLAS' style='width:82px;height:82px;object-fit:contain;'/>"
    if logo_uri else "<div style='font-weight:900;color:#000'>DA</div>"
)

# ============== DADOS =================
unidade         = "Rio de Janeiro"
data_medicao    = "12/07/2025 — 10:42 (UTC)"   # exemplo
rate_kgph       = 180                          # kg CH4/h
uncert_pct      = 10                           # %
spark_history   = [160, 170, 150, 180, 175, 182, 180]  # mock
passes = [
    {"sat":"GHGSat-C10","t":"13/07/2025 – 09:12","ang":"52°"},
    {"sat":"GHGSat-C12","t":"14/07/2025 – 10:03","ang":"47°"},
    {"sat":"GHGSat-C11","t":"15/07/2025 – 08:55","ang":"49°"},
]
passes_rows = "\n".join(f"<tr><td>{p['sat']}</td><td>{p['t']}</td><td>{p['ang']}</td></tr>" for p in passes)

# ============== HTML (placeholders) ==============
html = r"""
<!doctype html>
<html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
:root {
  --panel-w:__PANEL_W__px; --gap:__PANEL_GAP__px;
  --primary:__PRIMARY__; --bg:__BG__; --card:__CARD__;
  --text:__TEXT__; --muted:__MUTED__; --border:__BORDER__;
}
*{box-sizing:border-box}
body{margin:0;height:100vh;width:100vw;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Helvetica Neue,Arial,Noto Sans,sans-serif}

.stage{min-height:100vh;width:100vw;position:relative}
.side-panel{
  position:absolute; top:var(--gap); right:var(--gap); bottom:var(--gap);
  width:var(--panel-w); background:var(--card); border:1px solid var(--border);
  border-radius:18px; box-shadow:0 18px 44px rgba(0,0,0,.45);
  padding:14px; display:flex; flex-direction:column; gap:12px; overflow:auto;
  backdrop-filter:saturate(140%) blur(6px);
}

/* Header */
.header{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}
.brand{display:flex;gap:12px;align-items:center}
.brand .logo{width:82px;height:82px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;border:1px solid var(--border)}
.brand .txt .name{font-weight:900;letter-spacing:.2px}
.brand .txt .sub{font-size:.86rem;color:var(--muted)}
.badge{justify-self:end;background:rgba(0,227,165,.12);color:var(--primary);border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}

.hr{height:1px;background:var(--border);margin:6px 0 10px 0}

.block{border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.4)}
.block .title{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center}
.block .body{padding:10px}

/* KPIs */
.kpi2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.kpi{background:rgba(255,255,255,.04); border:1px solid var(--border);
  border-radius:12px; padding:14px 12px; text-align:center; position:relative}
.kpi .label{color:#b9c6e6;font-size:.9rem;margin-bottom:4px}
.kpi .value{font-weight:900;font-size:1.6rem;color:#ffffff;line-height:1}
.kpi .unit{font-size:.95rem;color:#cbd6f2;margin-left:4px}

/* sparkline & delta */
.spark{width:100%;height:20px;margin-top:6px}
.badge-pos,.badge-neg{display:inline-block;margin-left:8px;padding:3px 8px;border-radius:999px;font-weight:800;font-size:.8rem}
.badge-pos{background:rgba(52,211,153,.16);color:#34d399;border:1px solid rgba(52,211,153,.35)}
.badge-neg{background:rgba(248,113,113,.16);color:#f87171;border:1px solid rgba(248,113,113,.35)}

/* Gauge */
.gbox{display:flex;gap:10px;align-items:center;justify-content:center;margin-top:6px}
.gauge{width:72px;height:72px}
.gauge .bg{fill:none;stroke:rgba(255,255,255,.15);stroke-width:6}
.gauge .val{fill:none;stroke:#34D399;stroke-width:6;transform:rotate(-90deg);transform-origin:50% 50%}


/* Tabs */
.tabs{margin-top:4px}
.tabs input{display:none}
.tabs label{
  display:inline-block; padding:8px 12px; margin-right:8px; border:1px solid var(--border);
  border-bottom:none; border-top-left-radius:10px; border-top-right-radius:10px;
  color:var(--muted); background:rgba(255,255,255,.02); cursor:pointer; font-weight:700; font-size:.92rem
}
.tabs input:checked + label{color:#08121f; background:var(--primary); border-color:var(--primary)}
.tab-content{border:1px solid var(--border); border-radius:0 12px 12px 12px; padding:12px; margin-top:-1px}

table.minimal{width:100%;border-collapse:collapse}
table.minimal th, table.minimal td{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}
table.minimal th{color:#9fb0d4;font-weight:700}

/* passes */
.mapbox{height:220px;border:1px dashed rgba(255,255,255,.18);border-radius:10px;background:
  linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.02));display:flex;align-items:center;justify-content:center;color:#a9b8df}
.timeline{display:flex;gap:12px;overflow:auto;padding:8px;border:1px solid var(--border);border-radius:10px;background:#0f1a2e;margin-top:10px}
.badge-pass{min-width:190px;padding:8px 10px;border-radius:10px;background:rgba(255,255,255,.04);border:1px solid var(--border)}
.badge-pass b{color:#e6eefc}
.badge-pass small{color:#b9c6e6}

.footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem}
</style>
</head>
<body>
<div class="stage">
  <div class="side-panel" id="panel">

    <!-- HEADER -->
    <div class="header">
      <div class="brand">
        <div class="logo">__LOGO_HTML__</div>
        <div class="txt">
          <div class="name">Relatório OGMP 2.0 • L5</div>
          <div class="sub">Monitoramento de Emissões de Metano (CH₄)</div>
        </div>
      </div>
      <div class="badge">DAP ATLAS</div>
    </div>
    <div class="hr"></div>

    <!-- Unidade + Data -->
    <div class="block">
      <div class="body" style="padding:10px 12px">
        <div style="font-weight:800;font-size:1rem;margin-bottom:4px">Unidade: __UNIDADE__</div>
        <div style="font-size:.9rem;color:#b9c6e6">Data da Medição: __DATA_MEDICAO__</div>
      </div>
    </div>

    <!-- TABS -->
    <div class="tabs">
      <input type="radio" name="tab" id="tab-medicao" checked>
      <label for="tab-medicao">Medição Atual</label>

      <input type="radio" name="tab" id="tab-passes">
      <label for="tab-passes">Próximos Passes</label>

      <input type="radio" name="tab" id="tab-meta">
      <label for="tab-meta">Metadados</label>

      <input type="radio" name="tab" id="tab-resumo">
      <label for="tab-resumo">Resumo</label>

      <!-- Medição Atual (KPIs + sparkline + gauge) -->
      <div class="tab-content" id="content-medicao">
        <div class="kpi2">
          <div class="kpi" id="kpi-rate">
            <div class="label">Taxa</div>
            <div><span class="value" id="rate-val">__RATE__</span><span class="unit">kg CH₄/h</span>
              <span id="rate-delta" class="badge-pos" style="display:none"></span>
            </div>
            <svg class="spark" viewBox="0 0 100 28" preserveAspectRatio="none" id="sp-rate"></svg>
          </div>
          <div class="kpi">
            <div class="label">Incerteza de Medição</div>
            <div style="display:flex;align-items:center;justify-content:center;gap:6px">
              <span class="value" id="unc-val">__UNC__</span><span class="unit">%</span>
            </div>
            <div class="gbox">
              <svg viewBox="0 0 42 42" class="gauge"><circle class="bg" cx="21" cy="21" r="16"/>
              <circle class="val" cx="21" cy="21" r="16" stroke-dasharray="0,100"/></svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Próximos Passes -->
      <div class="tab-content" id="content-passes" style="display:none">
        <div class="section-title" style="font-weight:800;margin:2px 0 8px">Previsão de Passes</div>
        <div id="map-passes" class="mapbox">Mini-mapa de footprints</div>
        <div class="timeline" id="tl"></div>
        <div style="height:10px"></div>
        <table class="minimal">
          <thead><tr><th>Satélite</th><th>Data/Hora (UTC)</th><th>Ângulo</th></tr></thead>
          <tbody>__PASSES_ROWS__</tbody>
        </table>
      </div>

      <!-- Metadados -->
      <div class="tab-content" id="content-meta" style="display:none">
        <table class="minimal">
          <tr><th>Gerado em</th><td>__AGORA__</td></tr>
          <tr><th>Sistema</th><td>DAP ATLAS — OGMP 2.0</td></tr>
        </table>
      </div>

      <!-- Resumo -->
      <div class="tab-content" id="content-resumo" style="display:none">
        <p>Relatório OGMP 2.0 (Nível 5) com KPIs de emissão instantânea e incerteza. Dados fictícios para demonstração.</p>
      </div>
    </div>

    <div class="footer">
      <div>© __YEAR__ MAVIPE Sistemas Espaciais</div>
      <div></div>
    </div>

  </div>
</div>

<script>
// Troca das abas
const elMed  = document.getElementById('content-medicao');
const elPass = document.getElementById('content-passes');
const elMeta = document.getElementById('content-meta');
const elRes  = document.getElementById('content-resumo');

function show(which){
  elMed.style.display  = (which==='med') ? 'block' : 'none';
  elPass.style.display = (which==='pas') ? 'block' : 'none';
  elMeta.style.display = (which==='met') ? 'block' : 'none';
  elRes.style.display  = (which==='res') ? 'block' : 'none';
}
document.getElementById('tab-medicao').onchange = ()=>show('med');
document.getElementById('tab-passes').onchange  = ()=>show('pas');
document.getElementById('tab-meta').onchange    = ()=>show('met');
document.getElementById('tab-resumo').onchange  = ()=>show('res');

// ====== KPI Sparkline + Delta ======
const dataSpark = __SPARK__;
(function drawSpark(){
  const el = document.getElementById('sp-rate');
  const data = dataSpark && dataSpark.length ? dataSpark : [__RATE__];
  const W=100,H=28, pad=2, min=Math.min(...data), max=Math.max(...data);
  const x=i=>pad+i*((W-pad*2)/(data.length-1 || 1));
  const y=v=>H-pad - ((v-min)/(max-min || 1))*(H-pad*2);
  el.innerHTML = `<polyline fill="none" stroke="#4EA8DE" stroke-width="2"
    points="${data.map((v,i)=>`${x(i)},${y(v)}`).join(' ')}"/>`;

  if(data.length>1){
    const prevAvg = data.slice(0,-1).reduce((a,b)=>a+b,0)/(data.length-1);
    const last = data[data.length-1]; const delta = ((last - prevAvg)/Math.max(prevAvg,1e-6))*100;
    const tag = document.getElementById('rate-delta');
    tag.textContent = (delta>=0? '↑ ':'↓ ') + Math.abs(delta).toFixed(1) + '%';
    tag.className = (delta>=0)? 'badge-pos' : 'badge-neg';
    tag.style.display = 'inline-block';
  }
})();

// ====== Gauge de Incerteza ======
(function gauge(){
  const unc = Number(document.getElementById('unc-val').textContent) || 0;
  const dash = Math.max(0, Math.min(100, unc*3.6)); // 0-100
  document.querySelector('.gauge .val').setAttribute('stroke-dasharray', `${dash},100`);
})();

// ====== Passes: mini-mapa + timeline ======
const passes = __PASSES_JSON__;

(function miniMap(){
  const div = document.getElementById('map-passes');
  const W=300, H=220;
  let svg = `<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:100%"><rect x="0" y="0" width="${W}" height="${H}" fill="#0e172b"/>`;
  passes.forEach((p,i)=>{
    const cx = 60 + i*90, cy = 110 + (i%2? -20:20);
    const ang = parseInt((p.ang||'0').replace('°',''))||45;
    const r = 25 + Math.min(35, Math.max(0,(ang-30)));
    const col = i%3===0? '#4EA8DE' : (i%3===1? '#34d399' : '#F59E0B');
    svg += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${col}20" stroke="${col}" />`;
  });
  svg += `</svg>`;
  div.innerHTML = svg;
})();

(function timeline(){
  const tl = document.getElementById('tl');
  tl.innerHTML = passes.map(p=>`<div class="badge-pass"><b>${p.sat}</b><br><small>${p.t} • ${p.ang}</small></div>`).join('');
})();
</script>
</body></html>
"""

# ====== Substituições ======
html = (html
  .replace("__PANEL_W__", str(PANEL_W_PX))
  .replace("__PANEL_GAP__", str(PANEL_GAP_PX))
  .replace("__PRIMARY__", PRIMARY)
  .replace("__BG__", BG_DARK)
  .replace("__CARD__", CARD_DARK)
  .replace("__TEXT__", TEXT)
  .replace("__MUTED__", MUTED)
  .replace("__BORDER__", BORDER)
  .replace("__LOGO_HTML__", logo_html)
  .replace("__UNIDADE__", unidade)
  .replace("__DATA_MEDICAO__", data_medicao)
  .replace("__RATE__", str(rate_kgph))
  .replace("__UNC__", str(uncert_pct))
  .replace("__PASSES_ROWS__", passes_rows)
  .replace("__PASSES_JSON__", json.dumps(passes, ensure_ascii=False))
  .replace("__SPARK__", json.dumps(spark_history))
  .replace("__AGORA__", datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"))
  .replace("__YEAR__", str(datetime.now().year))
)

components.html(html, height=980, scrolling=False)


