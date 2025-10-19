# -*- coding: utf-8 -*-
# DAP ATLAS — Mock SaaS (single figure + panel)
# PNG 8K (app & figure) + Vector PDF A4/A3 + larger typography + stable export

from datetime import datetime, timezone
from base64 import b64encode
from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — Mock SaaS", page_icon="🛰️", layout="wide")

PRIMARY, BG, CARD, TEXT, MUTED, BORDER = (
    "#00E3A5", "#0b1221", "#10182b", "#FFFFFF", "#9fb0c9", "rgba(255,255,255,.10)"
)
PANEL_W_PX, PANEL_GAP_PX = 540, 20

def as_data_uri(path: Path) -> str:
    return "data:image/" + path.suffix.lstrip(".") + ";base64," + b64encode(path.read_bytes()).decode("ascii")

def fmt_dt_iso(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z","+00:00")).astimezone(timezone.utc)
        return dt.strftime("%d/%m/%Y — %H:%M (Local Time)")
    except Exception:
        return iso

# ===================== LOGO =====================
logo_uri = ""
p_logo = Path("dapatlas_fundo_branco.png")
if p_logo.exists() and p_logo.stat().st_size > 0:
    logo_uri = as_data_uri(p_logo)
logo_html = (
    f"<img src='{logo_uri}' alt='DAP ATLAS' style='width:82px;height:82px;object-fit:contain;'/>"
    if logo_uri else "<div style='font-weight:900;color:#000'>DA</div>"
)

# ===================== FIGURE (auto-detect) =====================
# Prioritizes HQ image; WhatsApp last
candidates = [
    "figure_highres.png", "figure_highres.jpg", "figure_highres.tif",
    "fig_swir.png", "split_combo.png", "swir.png", "figure.png",
    "Screenshot_2025-10-08_114722.png", "Screenshot 2025-10-08 114722.png",
    "WhatsApp Image 2025-10-08 at 1.51.03 AM.jpeg",
]
fig_path = next((p for n in candidates if (p := Path(n)).exists() and p.stat().st_size > 0), None)
img_uri = as_data_uri(fig_path) if fig_path else ""

# ===================== MOCK DATA / JSON =====================
unit             = "XPTO"
measurement_iso  = "2025-04-29T10:36:00Z"
measurement_date = fmt_dt_iso(measurement_iso)
local_time       = "10:36"
resolution_m     = 25
rate_kgph        = 180
uncert_pct       = 5
sea_state        = "Calm"
platform         = "FPSO"
objects          = ["Auxiliary Equipment"]
flare_active     = True
plume_detected   = True
plume_identified = True
wind_dir_deg     = 270
wind_avg_ms      = 5.2
wind_err_ms      = 2.0
passes = [
    {"sat":"GHGSat-C10","t":"29/04/2025 – 10:36","ang":"52°"},
    {"sat":"GHGSat-C12","t":"30/04/2025 – 10:08","ang":"47°"},
]

# Optional JSON override
mfile = Path("sample_measurement.json")
if mfile.exists() and mfile.stat().st_size > 0:
    try:
        M = json.loads(mfile.read_text(encoding="utf-8"))
    except:
        M = {}
    if M:
        unit = M.get("unidade", unit)
        if M.get("data_medicao"):
            measurement_iso = M["data_medicao"]
            measurement_date = fmt_dt_iso(measurement_iso)
        rate_kgph        = M.get("taxa_kgch4_h", rate_kgph)
        uncert_pct       = M.get("incerteza_pct", uncert_pct)
        sea_state        = M.get("estado_mar", sea_state)
        platform         = M.get("plataforma", platform)
        objects          = M.get("objetos_detectados", objects)
        flare_active     = bool(M.get("flare_ativo", flare_active))
        plume_detected   = bool(M.get("detec_pluma", plume_detected))
        plume_identified = bool(M.get("ident_pluma", plume_identified))
        wind_dir_deg     = M.get("dir_vento_graus", wind_dir_deg)
        wind_avg_ms      = M.get("vento_media_ms", wind_avg_ms)
        wind_err_ms      = M.get("vento_erro_ms", wind_err_ms)
        resolution_m     = M.get("resolucao_m", resolution_m)
        if M.get("img_swir"):
            v = M["img_swir"]
            if isinstance(v, str) and v.startswith("data:image:"):
                img_uri = v
            else:
                p = Path(str(v))
                if p.exists():
                    img_uri = as_data_uri(p)

# Right-panel tables
swir_rows = f"""
<tr><th>Methane Plume Detection</th><td>{"Yes" if plume_detected else "No"}</td></tr>
<tr><th>Methane Plume Identification</th><td>{"Yes" if plume_identified else "No"}</td></tr>
<tr><th>Methane Concentration (kgCH₄/hr)</th><td>{rate_kgph}</td></tr>
<tr><th>Uncertainty (%)</th><td>±{uncert_pct}%</td></tr>
"""
rgb_rows = f"""
<tr><th>Sea State</th><td>{sea_state}</td></tr>
<tr><th>Platform</th><td>{platform}</td></tr>
<tr><th>Detected Objects</th><td>{", ".join(objects)}</td></tr>
<tr><th>Active Flare</th><td>{'Yes 🟢' if flare_active else 'No ⚪'}</td></tr>
"""
met_rows = f"""
<tr><th>Wind Speed (m/s)</th><td>{wind_avg_ms} ±{wind_err_ms}</td></tr>
<tr><th>Wind Direction (deg)</th><td>{wind_dir_deg} (from where it blows)</td></tr>
"""

# ===================== HTML =====================
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
html, body{
  margin:0;height:100vh;width:100vw;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Helvetica Neue,Arial,Noto Sans,sans-serif;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; text-rendering: optimizeLegibility;
}
.stage{min-height:100vh;width:100vw;position:relative}

/* ===== Figure (left) ===== */
.visual-wrap{
  position:absolute; top:var(--gap); bottom:100px; left:var(--gap);
  right:calc(var(--panel-w) + var(--gap)*2);
  border:1px solid var(--border); border-radius:12px; overflow:hidden;
  box-shadow:0 18px 44px rgba(0,0,0,.35); background:#0f172a;
  display:flex; flex-direction:column;
}
.v-header{
  background:#1f497d; color:#e8f0ff; padding:10px 12px; font-weight:800; font-size:1.8rem;
  border-bottom:1px solid rgba(255,255,255,.2); position:relative;
}
.v-body{position:relative; flex:1; background:#0b1327; overflow:hidden}
.v-body .img-holder{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
}
.v-body img{max-width:100%; max-height:100%; object-fit:contain; background:#0b1327;}
.v-footer{
  padding:12px 16px; color:#cfdaf5; font-size:1.05rem; line-height:1.4;
  background:#0e172b; border-top:1px solid var(--border); text-align:center;
}

/* Actions in the figure header */
.vh-actions{position:absolute; right:10px; top:6px; display:flex; gap:8px}
.pill{
  height:30px; padding:0 12px; border-radius:999px; border:1px solid rgba(255,255,255,.25);
  background:rgba(0,0,0,.28); color:#fff; font-weight:800; font-size:1.1rem; cursor:pointer;
  backdrop-filter: blur(3px) saturate(130%);
}

/* ===== Timeline ===== */
.timeline{
  position:absolute; left:var(--gap); right:calc(var(--panel-w) + var(--gap)*2);
  bottom:var(--gap); height:84px; border:1px solid var(--border); border-radius:10px;
  background:#0f1a2e; display:flex; flex-direction:column; justify-content:space-between;
  padding:8px 10px; box-shadow:0 10px 24px rgba(0,0,0,.35);
}
.ticks{display:flex; gap:20px; align-items:center; overflow:auto; color:#cfe7ff; font-size:.9rem}

/* ===== Right Panel ===== */
.side-panel{
  position:absolute; top:var(--gap); right:var(--gap); bottom:var(--gap);
  width:var(--panel-w); background:var(--card); border:1px solid var(--border);
  border-radius:18px; box-shadow:0 18px 44px rgba(0,0,0,.45);
  padding:16px; display:flex; flex-direction:column; gap:14px; overflow:auto;
  backdrop-filter:saturate(140%) blur(6px);
  font-size: 1.8rem;   /* larger overall panel font */
  line-height: 1.5;    /* more legible text */
}
.header{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}
.brand{display:flex;gap:12px;align-items:center}
.brand .logo{width:82px;height:82px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;border:1px solid var(--border)}
.brand .txt .name{font-weight:900;letter-spacing:.2px; font-size:1.3rem}
.brand .txt .sub{font-size:1rem;color:#9fb0d4}
.badge{justify-self:end;background:rgba(0,227,165,.12);color:#00E3A5;border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.95rem;white-space:nowrap}
.hr{height:1px;background:var(--border);margin:6px 0 10px 0}
.block{border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.4)}
.block .title{
  background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center;
  font-size:1.25rem; letter-spacing:.3px;
}
.block .body{padding:12px}
table.minimal{width:100%;border-collapse:collapse}
table.minimal th, table.minimal td{
  border-bottom:1px solid var(--border);padding:10px 8px;text-align:left;font-size:1.1rem; line-height:1.4;
}
table.minimal th{color:#c5d1ec;font-weight:700}
.footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.9rem}

/* ===== Export mode: prevent text overlap, remove effects ===== */
.exporting *{
  letter-spacing:0 !important; word-spacing:0 !important; text-shadow:none !important;
  filter:none !important; backdrop-filter:none !important;
}
.exporting .block .title,
.exporting table.minimal th, .exporting table.minimal td,
.exporting .v-header, .exporting .footer { line-height:1.4 !important; }
.exporting .vh-actions { display:none !important; }
</style>
</head>
<body>
<div class="stage" id="stage">

  <!-- FIGURE -->
  <div class="visual-wrap" id="visual">
    <div class="v-header">
      Satellite CHGSAT – SWIR Sensor
      <div class="vh-actions">
        <button id="btnExport8K" class="pill" title="Export 8K PNG of the dashboard">PNG 8K</button>
        <button id="btnExport8KFig" class="pill" title="Export 8K PNG of the figure only">PNG 8K (Figure)</button>
        <button id="btnPdfA4" class="pill" title="Export A4 PDF (landscape)">PDF A4</button>
        <button id="btnPdfA3" class="pill" title="Export A3 PDF (landscape)">PDF A3</button>
      </div>
    </div>

    <div class="v-body" id="vbody">
      <div class="img-holder" id="imgHolder">
        <img id="theImage" src="__IMG__" alt="figure"/>
      </div>
    </div>

    <div class="v-footer">
      Illustrative image created to demonstrate technological capability. It does not represent real measurements and is not linked to contracts, clients, or operations.
    </div>
  </div>

  <!-- TIMELINE -->
  <div class="timeline">
    <div style="color:#9fb0d4;font-weight:800;">Timeline (passes)</div>
    <div class="ticks" id="tl"></div>
  </div>

  <!-- RIGHT PANEL -->
  <div class="side-panel" id="panel">
    <div class="header">
      <div class="brand">
        <div class="logo">__LOGO_HTML__</div>
        <div class="txt">
          <div class="name">OGMP 2.0 Report • L5</div>
        </div>
      </div>
      <div class="badge">SWIR SENSOR</div>
    </div>
    <div class="hr"></div>

    <!-- Unit -->
    <div class="block">
      <div class="title">Unit</div>
      <div class="body" style="text-align:center; font-size:1.3rem; font-weight:800; color:#00E3A5;">
        __UNIDADE__
      </div>
    </div>

    <!-- Acquisition -->
    <div class="block"><div class="title">Acquisition</div>
      <div class="body"><table class="minimal">
        <tr><th>Acquisition Date</th><td>__DATA_MED__</td></tr>
        <tr><th>Time</th><td>__HORA__</td></tr>
        <tr><th>Resolution</th><td>__RES__ m</td></tr>
      </table></div>
    </div>

    <div class="block"><div class="title">Results Derived from SWIR Satellite</div>
      <div class="body"><table class="minimal">__SWIR_ROWS__</table></div></div>

    <div class="block"><div class="title">Results Derived from RGB Satellite</div>
      <div class="body"><table class="minimal">__RGB_ROWS__</table></div></div>

    <div class="block"><div class="title">Meteorological Data — GEOS</div>
      <div class="body"><table class="minimal">__MET_ROWS__</table></div></div>

    <div class="footer"><div>© __YEAR__ MAVIPE Space Systems</div><div></div></div>
  </div>
</div>

<!-- libs -->
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>

<script>
// ========= timeline mock
const passes=__PASSES_JSON__;
(function(){
  const tl = document.getElementById('tl');
  tl.innerHTML = passes.map(p=>`<div style="min-width:210px;padding:6px 10px;border-radius:9px;border:1px solid rgba(255,255,255,.18);
     background:rgba(255,255,255,.04)"><b style="color:#e6eefc">${p.sat||'-'}</b><br>
     <small>${(p.t||'-')} • ${(p.ang||'-')}</small></div>`).join('');
})();

// ========= PNG 8K (stable, avoids zoom-out; prevents overlap)
async function exportPNG8K(el, fname, opts={}){
  const longSide = opts.longSide || 7680;
  const capScale = opts.capScale || 5;  // 5 tends to be more stable than 6
  const rect = el.getBoundingClientRect();
  const w = Math.max(1, Math.ceil(rect.width));
  const h = Math.max(1, Math.ceil(rect.height));
  const base = Math.max(w, h);
  const dpr = Math.max(1, window.devicePixelRatio || 1);
  const scale = Math.min(capScale, (longSide / base) * (dpr > 1 ? dpr : 1));

  document.body.classList.add('exporting'); // export mode: consistent line-height, no shadows

  try{
    const canvas = await html2canvas(el, {
      backgroundColor:null,
      useCORS:true,
      logging:false,
      scale,
      foreignObjectRendering:true,
      windowWidth: Math.max(el.scrollWidth, w),
      windowHeight: Math.max(el.scrollHeight, h)
    });
    await new Promise((resolve) => {
      canvas.toBlob(function(blob){
        const a=document.createElement('a'); const ts=new Date().toISOString().slice(0,19).replace(/[:T]/g,'-');
        a.href=URL.createObjectURL(blob);
        a.download=fname.replace('{ts}', ts).replace('{w}', canvas.width).replace('{h}', canvas.height);
        document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(a.href);
        resolve();
      }, 'image/png');
    });
  } finally {
    document.body.classList.remove('exporting');
  }
}
document.getElementById('btnExport8K')?.addEventListener('click', ()=> exportPNG8K(document.getElementById('stage'),  'dap-atlas_app_8k_{ts}_{w}x{h}.png', {longSide:7680, capScale:5}) );
document.getElementById('btnExport8KFig')?.addEventListener('click', ()=> exportPNG8K(document.getElementById('visual'), 'dap-atlas_fig_8k_{ts}_{w}x{h}.png',  {longSide:7680, capScale:5}) );

// ======== Vector PDF via print window ========
function printAsPDF(el, {size='A4', orientation='landscape'} = {}){
  const w = window.open('', '_blank', 'noopener,noreferrer,width=1200,height=800');
  const stage = el.cloneNode(true);

  stage.style.background = '#ffffff';
  stage.querySelectorAll('.visual-wrap, .side-panel, .timeline').forEach(n=>{ n.style.boxShadow = 'none'; });

  const css = `
    <style>
      @page { size: ${size} ${orientation}; margin: 10mm; }
      @media print {
        html, body { background:#fff !important; }
        body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        #root { width: 100%; }
      }
      #root { display:flex; justify-content:center; }
      #root > .stage-print { width: 100%; }
      * { overflow: visible !important; }
    </style>
  `;

  w.document.write(`
    <html>
      <head><meta charset="utf-8"/>${css}</head>
      <body>
        <div id="root"><div class="stage-print"></div></div>
        <script>
          setTimeout(()=>{ window.print(); setTimeout(()=>window.close(), 300); }, 250);
        <\/script>
      </body>
    </html>
  `);
  w.document.close();
  w.document.querySelector('.stage-print').appendChild(stage);
}
document.getElementById('btnPdfA4')?.addEventListener('click', ()=>{ printAsPDF(document.getElementById('stage'), {size:'A4', orientation:'landscape'}); });
document.getElementById('btnPdfA3')?.addEventListener('click', ()=>{ printAsPDF(document.getElementById('stage'), {size:'A3', orientation:'landscape'}); });
</script>
</body></html>
"""

# ===== REPLACE TOKENS =====
html = (html
  .replace("__PANEL_W__", str(PANEL_W_PX)).replace("__PANEL_GAP__", str(PANEL_GAP_PX))
  .replace("__PRIMARY__", PRIMARY).replace("__BG__", BG).replace("__CARD__", CARD)
  .replace("__TEXT__", TEXT).replace("__MUTED__", MUTED).replace("__BORDER__", BORDER)
  .replace("__LOGO_HTML__", logo_html).replace("__UNIDADE__", unit)
  .replace("__DATA_MED__", measurement_date).replace("__HORA__", local_time).replace("__RES__", str(resolution_m))
  .replace("__IMG__", img_uri or "")
  .replace("__SWIR_ROWS__", swir_rows).replace("__RGB_ROWS__", rgb_rows).replace("__MET_ROWS__", met_rows)
  .replace("__YEAR__", str(datetime.now().year))
  .replace("__PASSES_JSON__", json.dumps(passes, ensure_ascii=False))
)

components.html(html, height=1400, scrolling=False)



