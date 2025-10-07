# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar (OGMP 2.0 L5 • Metano) — KPIs + Unidade/Data + Aba de Próximos Passes
# Export: S = SVG, P = PDF

from datetime import datetime
from base64 import b64encode
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — OGMP 2.0 L5", page_icon="🛰️", layout="wide")

# ================= THEME =================
PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

PANEL_W_PX   = 560
PANEL_GAP_PX = 24

# =============== LOGO (opcional) ===============
logo_uri = ""
p = Path("dapatlas_fundo_branco.png")
if p.exists() and p.stat().st_size > 0:
    logo_uri = "data:image/png;base64," + b64encode(p.read_bytes()).decode("ascii")
logo_html = (
    f"<img src='{logo_uri}' alt='DAP ATLAS' style='width:82px;height:82px;object-fit:contain;'/>"
    if logo_uri else "<div style='font-weight:900;color:#000'>DA</div>"
)

# =============== DADOS (mock) ===============
unidade         = "Rio de Janeiro"
data_medicao    = "12/07/2025 — 10:42 (UTC)"   # exemplo inventado
rate_kgph       = 180                          # kg CH4/h
uncert_pct      = 10                           # %

# Próximos passes (exemplo)
passes = [
    ("GHGSat-C10", "13/07/2025 – 09:12", "52°"),
    ("GHGSat-C12", "14/07/2025 – 10:03", "47°"),
    ("GHGSat-C11", "15/07/2025 – 08:55", "49°"),
]

# =============== HTML com PLACEHOLDERS (sem f-string) ===============
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

.block{border:1px solid var(--border);border-radius:12px;overflow:hidden}
.block .title{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center}
.block .body{padding:10px}

/* KPIs */
.kpi2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.kpi{
  background:rgba(255,255,255,.04); border:1px solid var(--border);
  border-radius:12px; padding:14px 12px; text-align:center
}
.kpi .label{color:#b9c6e6;font-size:.9rem;margin-bottom:4px}
.kpi .value{font-weight:900;font-size:1.6rem;color:#ffffff;line-height:1}
.kpi .unit{font-size:.95rem;color:#cbd6f2;margin-left:4px}

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

      <!-- Medição Atual (KPIs) -->
      <div class="tab-content" id="content-medicao">
        <div class="kpi2">
          <div class="kpi">
            <div class="label">Taxa</div>
            <div><span class="value">__RATE__</span><span class="unit">kg CH₄/h</span></div>
          </div>
          <div class="kpi">
            <div class="label">Incerteza de Medição</div>
            <div><span class="value">__UNC__</span><span class="unit">%</span></div>
          </div>
        </div>
      </div>

      <!-- Próximos Passes -->
      <div class="tab-content" id="content-passes" style="display:none">
        <div class="section-title" style="font-weight:800;margin:2px 0 8px">Previsão de Passes</div>
        <table class="minimal">
          <thead><tr><th>Satélite</th><th>Data/Hora (UTC)</th><th>Ângulo</th></tr></thead>
          <tbody>
            __PASSES_ROWS__
          </tbody>
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
      <div>Atalhos: S = SVG • P = PDF</div>
    </div>

  </div>
</div>

<!-- libs para exportação -->
<script src="https://cdn.jsdelivr.net/npm/dom-to-image-more@2.8.0/dist/dom-to-image-more.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/svg2pdf.js@2.2.3/dist/svg2pdf.umd.min.js"></script>

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

// Exportação do painel
const PANEL = document.getElementById('panel');

async function exportSVG(){
  const dataUrl = await domtoimage.toSvg(PANEL, { bgcolor: '__CARD__', quality: 1 });
  const a = document.createElement('a'); a.href = dataUrl; a.download = 'OGMP_L5_Sidebar.svg'; a.click();
}
async function exportPDF(){
  const svgUrl  = await domtoimage.toSvg(PANEL, { bgcolor: '__CARD__', quality: 1 });
  const svgText = await (await fetch(svgUrl)).text();
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({ unit: 'pt', format: 'a4', orientation: 'p' });

  const parser = new DOMParser();
  const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');
  const svgEl  = svgDoc.documentElement;

  const pageW = pdf.internal.pageSize.getWidth();
  const pageH = pdf.internal.pageSize.getHeight();
  const width  = PANEL.offsetWidth;
  const height = PANEL.offsetHeight;
  const scale = Math.min(pageW/width, pageH/height);

  window.svg2pdf(svgEl, pdf, {
    x:(pageW-width*scale)/2, y:(pageH-height*scale)/2, scale: scale
  });
  pdf.save('OGMP_L5_Sidebar.pdf');
}

// atalhos S/P
document.addEventListener('keydown', (e)=>{
  if(e.key==='s'||e.key==='S') exportSVG();
  if(e.key==='p'||e.key==='P') exportPDF();
});
</script>
</body></html>
"""

# ----- monta linhas da tabela de passes -----
rows = "\n".join(f"<tr><td>{sat}</td><td>{dt}</td><td>{ang}</td></tr>" for sat, dt, ang in passes)

# ----- substituições seguras -----
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
  .replace("__PASSES_ROWS__", rows)
  .replace("__AGORA__", datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"))
  .replace("__YEAR__", str(datetime.now().year))
)

components.html(html, height=980, scrolling=False)

