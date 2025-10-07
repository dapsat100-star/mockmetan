# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar (OGMP 2.0 L5 • Metano) — versão sem f-string (sem conflitos de { }).

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
logo_html = f"<img src='{logo_uri}' alt='DAP ATLAS' style='width:82px;height:82px;object-fit:contain;'/>" if logo_uri else "<div style='font-weight:900;color:#000'>DA</div>"

# =============== DADOS MOCK ===============
sites = ["Site1", "Site2", "Site3"]
default_date = "2025-03-12"
meses = ["Jan","Fev","Mar","Abr","Mai","Jun"]
emissoes = [120,150,130,170,160,180]  # kg CH4/h (mock)
acumulado_ton = 150

# opções do select (HTML)
sites_options_html = "".join(f"<option>{s}</option>" for s in sites)

# ================= HTML COM PLACEHOLDERS =================
html = """
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

/* Controls row */
.controls{display:grid;grid-template-columns:1fr 1fr auto;gap:10px;align-items:end}
.ctrl label{display:block;font-size:.85rem;color:#cdd6f5;margin:0 0 6px}
.ctrl input[type=date], .ctrl select{width:100%;background:#0e172b;border:1px solid var(--border);border-radius:10px;color:#e6eefc;padding:10px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:11px 14px;border-radius:10px;
     font-weight:800;text-decoration:none;background:var(--primary);color:#05131a;border:1px solid rgba(0,0,0,.25)}

/* Section blocks */
.block{border:1px solid var(--border);border-radius:12px;overflow:hidden}
.block .title{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center}
.block .body{padding:10px}

/* Imagery */
.mapbox{height:220px;border:1px dashed rgba(255,255,255,.18);border-radius:10px;background:
  linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.02));display:flex;align-items:center;justify-content:center;color:#a9b8df}
.mapthumb{height:160px;border-radius:10px;overflow:hidden;margin-top:10px;background:#0f1a2e;border:1px solid var(--border);display:flex;align-items:center;justify-content:center;color:#9fb0d4}
.caption{font-size:.85rem;color:#a9b8df;margin-top:6px;text-align:left}

/* Measurements */
.kgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.kcard{background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:10px;overflow:hidden}
.kcard .khead{background:#0f1a2e;color:#e6eefc;padding:8px 10px;font-weight:800}
.krows{display:grid;grid-template-columns:1fr 1fr;gap:0}
.krows>div{padding:8px 10px;border-top:1px solid var(--border)}
.krows>div:nth-child(odd){border-right:1px solid var(--border)}
.krows label{display:block;font-size:.85rem;color:#b9c6e6;margin-bottom:4px}
.krows input{width:100%;padding:8px 10px;border-radius:8px;background:#0e172b;border:1px solid var(--border);color:#e6eefc}

/* Histórico */
.hist .accum{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-bottom:8px}
.hist .accum input{width:160px;text-align:center;background:#0e172b;border:1px solid var(--border);color:#e6eefc;border-radius:8px;padding:8px}
.chart{height:220px;border:1px solid var(--border);border-radius:10px;background:#0f1a2e;display:flex;align-items:center;justify-content:center;position:relative}
.chart svg{width:95%;height:85%}
.chart .ylabel{position:absolute;left:8px;top:6px;color:#cbd6f2;font-size:.85rem;transform:rotate(-90deg);transform-origin:left top}
.chart .xlabel{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);color:#cbd6f2;font-size:.85rem}
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

    <!-- CONTROLS -->
    <div class="controls">
      <div class="ctrl">
        <label>Data da Medição por Satélite de Metano</label>
        <input id="inp-date" type="date" value="__DEFAULT_DATE__"/>
      </div>
      <div class="ctrl">
        <label>Site</label>
        <select id="inp-site">__SITES_OPTIONS__</select>
      </div>
      <div class="ctrl">
        <label>&nbsp;</label>
        <a class="btn" href="#" onclick="exportPDF();return false;">GERAR PDF ➜</a>
      </div>
    </div>

    <!-- IMAGERY -->
    <div class="block">
      <div class="title">Imagery</div>
      <div class="body">
        <div class="mapbox">Mini-mapa / Mosaic (placeholder)</div>
        <div class="mapthumb">Thumb de satélite do passe</div>
        <div class="caption">25 de Fevereiro de 2025 — 11h42 (hora local)</div>
      </div>
    </div>

    <!-- MEASUREMENTS -->
    <div class="block">
      <div class="title">Measurements</div>
      <div class="body kgrid">
        <!-- Velocidade -->
        <div class="kcard">
          <div class="khead">Velocidade do Vento no momento da aquisição (m/s)</div>
          <div class="krows">
            <div>
              <label>ECMWF</label>
              <input id="vel-ecmwf" type="number" value="12" step="0.1"/>
            </div>
            <div>
              <label>Medição Local</label>
              <input id="vel-local" type="number" value="12" step="0.1"/>
            </div>
          </div>
        </div>
        <!-- Direção -->
        <div class="kcard">
          <div class="khead">Direção do Vento no momento da aquisição (°)</div>
          <div class="krows">
            <div>
              <label>ECMWF</label>
              <input id="dir-ecmwf" type="number" value="320" step="1"/>
            </div>
            <div>
              <label>Medição Local</label>
              <input id="dir-local" type="number" value="315" step="1"/>
            </div>
          </div>
        </div>
        <!-- Concentração -->
        <div class="kcard">
          <div class="khead">Concentração de Metano (kg/h)</div>
          <div class="krows">
            <div>
              <label>ECMWF</label>
              <input id="conc-ecmwf" type="number" value="12" step="0.1"/>
            </div>
            <div>
              <label>Medição Local</label>
              <input id="conc-local" type="number" value="12" step="0.1"/>
            </div>
          </div>
        </div>
        <!-- Erro Máximo -->
        <div class="kcard">
          <div class="khead">Erro Máximo de Medição (%)</div>
          <div class="krows">
            <div>
              <label>ECMWF</label>
              <input id="err-ecmwf" type="number" value="2" step="0.1"/>
            </div>
            <div>
              <label>Medição Local</label>
              <input id="err-local" type="number" value="1.3" step="0.1"/>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- HISTÓRICO -->
    <div class="block hist">
      <div class="title">Informações Históricas sobre o Site</div>
      <div class="body">
        <div class="accum">
          <div style="font-weight:800">Acumulado emitido até a data de medição (ton)</div>
          <input id="accum" type="number" value="__ACUMULADO__" step="1"/>
        </div>
        <div class="chart">
          <div class="ylabel">Emissão (kg CH₄/h)</div>
          <div class="xlabel">Mês</div>
          <svg id="chart"></svg>
        </div>
      </div>
    </div>

    <div style="margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem">
      <div>© __YEAR__ MAVIPE Sistemas Espaciais</div>
      <div>DAP ATLAS</div>
    </div>
  </div>
</div>

<!-- libs para exportação -->
<script src="https://cdn.jsdelivr.net/npm/dom-to-image-more@2.8.0/dist/dom-to-image-more.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/svg2pdf.js@2.2.3/dist/svg2pdf.umd.min.js"></script>

<script>
// ====== Gráfico simples (SVG) ======
const meses   = __MESES__;
const valores = __EMISSOES__;

// desenha linha com eixos simples
(function draw(){
  const svg = document.getElementById('chart');
  const W = svg.clientWidth || 480, H = svg.clientHeight || 200;
  const pad = 22;
  const minV = Math.min(...valores)*0.95, maxV = Math.max(...valores)*1.05;

  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.innerHTML = '';

  // eixo X
  for(let i=0;i<meses.length;i++){
    const x = pad + i*( (W-pad*2)/(meses.length-1) );
    const t = document.createElementNS('http://www.w3.org/2000/svg','text');
    t.setAttribute('x', x); t.setAttribute('y', H-6);
    t.setAttribute('text-anchor','middle'); t.setAttribute('font-size','11');
    t.setAttribute('fill','#cbd6f2'); t.textContent = meses[i];
    svg.appendChild(t);
  }

  // escala Y
  function y(v){ return H-pad - ( (v-minV)/(maxV-minV) )*(H-pad*2); }
  function x(i){ return pad + i*( (W-pad*2)/(meses.length-1) ); }

  // grid horizontal
  for(let g=0; g<4; g++){
    const gy = pad + g*((H-pad*2)/3);
    const line = document.createElementNS('http://www.w3.org/2000/svg','line');
    line.setAttribute('x1', pad); line.setAttribute('x2', W-pad);
    line.setAttribute('y1', gy);  line.setAttribute('y2', gy);
    line.setAttribute('stroke','rgba(255,255,255,.12)'); line.setAttribute('stroke-width','1');
    svg.appendChild(line);
  }

  // polyline
  const pts = valores.map((v,i)=>`${x(i)},${y(v)}`).join(' ');
  const pl = document.createElementNS('http://www.w3.org/2000/svg','polyline');
  pl.setAttribute('points', pts);
  pl.setAttribute('fill','none'); pl.setAttribute('stroke','#4EA8DE'); pl.setAttribute('stroke-width','3');
  svg.appendChild(pl);

  // pontos
  valores.forEach((v,i)=>{
    const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx', x(i)); c.setAttribute('cy', y(v)); c.setAttribute('r','4');
    c.setAttribute('fill','#FFD166'); svg.appendChild(c);
  });
})();

// ====== Exportação do painel ======
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
    x:(pageW-width*scale)/2, y:(pageH-height*scale)/2, scale:scale
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

# ====== SUBSTITUIÇÕES SEGURAS (sem f-string) ======
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
    .replace("__DEFAULT_DATE__", default_date)
    .replace("__SITES_OPTIONS__", sites_options_html)
    .replace("__ACUMULADO__", str(acumulado_ton))
    .replace("__YEAR__", str(datetime.now().year))
    .replace("__MESES__", str(meses))
    .replace("__EMISSOES__", str(emissoes))
)

components.html(html, height=980, scrolling=False)
