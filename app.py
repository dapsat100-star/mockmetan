# -*- coding: utf-8 -*-
# DAP ATLAS — Mockup OGMP 2.0 L5 (Painel lateral + área 50/50 p/ imagens)
# ✅ Datas RGB/SWIR incluídas

from datetime import datetime, timezone
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
p_logo = Path("dapatlas_fundo_branco.png")
if p_logo.exists() and p_logo.stat().st_size > 0:
    logo_uri = "data:image/png;base64," + b64encode(p_logo.read_bytes()).decode("ascii")
logo_html = (
    f"<img src='{logo_uri}' alt='DAP ATLAS' style='width:82px;height:82px;object-fit:contain;'/>"
    if logo_uri else "<div style='font-weight:900;color:#000'>DA</div>"
)

# ============== DEFAULT DATA =================
unidade         = "Rio de Janeiro"
data_medicao    = "12/07/2025 — 10:42 (UTC)"
rate_kgph       = 180
uncert_pct      = 10
spark_history   = [160, 170, 150, 180, 175, 182, 180]
passes          = [
    {"sat":"GHGSat-C10","t":"13/07/2025 – 09:12","ang":"52°"},
    {"sat":"GHGSat-C12","t":"14/07/2025 – 10:03","ang":"47°"},
    {"sat":"GHGSat-C11","t":"15/07/2025 – 08:55","ang":"49°"},
]

# imagens e datas fictícias
img_rgb  = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/FPSO_P-74.jpg/640px-FPSO_P-74.jpg"
img_swir = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Methane_plume_example.png/480px-Methane_plume_example.png"
rgb_dt   = "29/04/2025 — 08:06 (UTC)"
swir_dt  = "29/04/2025 — 10:36 (UTC)"
colorbar_max = 1000

# ============== HTML MOCKUP ==============
html = f"""
<!doctype html>
<html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
:root {{
  --panel-w:{PANEL_W_PX}px; --gap:{PANEL_GAP_PX}px;
  --primary:{PRIMARY}; --bg:{BG_DARK}; --card:{CARD_DARK};
  --text:{TEXT}; --muted:{MUTED}; --border:{BORDER};
}}
*{{box-sizing:border-box}}
body{{margin:0;height:100vh;width:100vw;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Helvetica Neue,Arial,Noto Sans,sans-serif}}
.stage{{display:flex;flex-direction:row;height:100vh;width:100vw}}

/* LEFT side — images 50% */
.left-panel{{
  flex:1;
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  padding:10px;
  background:#111827;
}}
.left-panel img{{max-width:95%;max-height:45%;border-radius:10px;margin-bottom:10px;object-fit:contain;border:1px solid var(--border)}}

/* RIGHT side — SaaS panel */
.side-panel{{
  width:var(--panel-w); background:var(--card); border:1px solid var(--border);
  border-radius:18px; box-shadow:0 18px 44px rgba(0,0,0,.45);
  padding:14px; display:flex; flex-direction:column; gap:12px; overflow:auto;
  backdrop-filter:saturate(140%) blur(6px);
  margin:var(--gap);
}}
.header{{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}}
.brand{{display:flex;gap:12px;align-items:center}}
.brand .logo{{width:82px;height:82px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;border:1px solid var(--border)}}
.brand .txt .name{{font-weight:900;letter-spacing:.2px}}
.brand .txt .sub{{font-size:.86rem;color:var(--muted)}}
.badge{{justify-self:end;background:rgba(0,227,165,.12);color:var(--primary);border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}}
.hr{{height:1px;background:var(--border);margin:6px 0 10px 0}}
.block{{border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.4)}}
.block .title{{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center}}
.block .body{{padding:10px}}
table.minimal{{width:100%;border-collapse:collapse}}
table.minimal th, table.minimal td{{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}}
table.minimal th{{color:#9fb0d4;font-weight:700}}
.footer{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem}}
</style>
</head>
<body>
<div class="stage">

  <!-- LEFT: 50% -->
  <div class="left-panel">
    <div>
      <img src="{img_rgb}" alt="RGB"/>
      <div style="text-align:center;color:#b9c6e6;font-size:.85rem;margin-bottom:8px">
        Satélite RGB — Data/Hora: {rgb_dt}
      </div>
    </div>
    <div>
      <img src="{img_swir}" alt="SWIR"/>
      <div style="text-align:center;color:#b9c6e6;font-size:.85rem">
        Satélite SWIR (CH₄) — Data/Hora: {swir_dt}
      </div>
    </div>
  </div>

  <!-- RIGHT: SaaS -->
  <div class="side-panel" id="panel">
    <div class="header">
      <div class="brand">
        <div class="logo">{logo_html}</div>
        <div class="txt">
          <div class="name">Relatório OGMP 2.0 • L5</div>
          <div class="sub">Monitoramento de Emissões de Metano (CH₄)</div>
        </div>
      </div>
      <div class="badge">DAP ATLAS</div>
    </div>
    <div class="hr"></div>

    <div class="block">
      <div class="body">
        <div style="font-weight:800;font-size:1rem;margin-bottom:4px">Unidade: {unidade}</div>
        <div style="font-size:.9rem;color:#b9c6e6">Data da Medição: {data_medicao}</div>
      </div>
    </div>

    <div class="block">
      <div class="title">Resultados SWIR</div>
      <div class="body">
        <table class="minimal">
          <tr><th>Detecção da Pluma</th><td>Sim</td></tr>
          <tr><th>Identificação da Pluma</th><td>Sim</td></tr>
          <tr><th>Concentração (kgCH₄/h)</th><td>{rate_kgph}</td></tr>
          <tr><th>Incerteza (%)</th><td>±{uncert_pct}</td></tr>
        </table>
      </div>
    </div>

    <div class="block">
      <div class="title">Dados Meteorológicos</div>
      <div class="body">
        <table class="minimal">
          <tr><th>Velocidade do Vento (m/s)</th><td>5.2 ± 2.0</td></tr>
          <tr><th>Direção do Vento (°)</th><td>270 (de onde sopra)</td></tr>
        </table>
      </div>
    </div>

    <div class="footer">
      <div>© {datetime.now().year} MAVIPE Sistemas Espaciais</div>
      <div></div>
    </div>
  </div>
</div>
</body></html>
"""

components.html(html, height=1000, scrolling=False)
