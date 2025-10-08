# -*- coding: utf-8 -*-
# DAP ATLAS — Mock SaaS (figura única + painel)
# PNG 8K (app e figura) + PDF A4/A3 vetorial

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
        return dt.strftime("%d/%m/%Y — %H:%M (Hora Local)")
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

# ===================== FIGURA (autodetect) =====================
candidates = [
    "Screenshot 2025-10-08 114722.png",
    "Screenshot_2025-10-08_114722.png",
    "fig_swir.png", "split_combo.png", "swir.png", "figure.png",
    "WhatsApp Image 2025-10-08 at 1.51.03 AM.jpeg",
]
fig_path = next((p for n in candidates if (p := Path(n)).exists() and p.stat().st_size > 0), None)
img_uri = as_data_uri(fig_path) if fig_path else ""

# ===================== DADOS MOCK / JSON =====================
unidade        = "Rio de Janeiro"
data_medicao_iso = "2025-04-29T10:36:00Z"
data_medicao   = fmt_dt_iso(data_medicao_iso)
hora_local     = "10h36"
resolucao_m    = 25
rate_kgph      = 180
uncert_pct     = 5
estado_mar     = "Calmo"
plataforma     = "FPSO"
objetos        = ["Equipamentos Auxiliares"]
flare_ativo    = True
detec_pluma    = True
ident_pluma    = True
dir_vento_graus= 270
vento_media_ms = 5.2
vento_erro_ms  = 2.0
passes = [
    {"sat":"GHGSat-C10","t":"29/04/2025 – 10:36","ang":"52°"},
    {"sat":"GHGSat-C12","t":"30/04/2025 – 10:08","ang":"47°"},
]

# JSON opcional
mfile = Path("sample_measurement.json")
if mfile.exists() and mfile.stat().st_size > 0:
    try:
        M = json.loads(mfile.read_text(encoding="utf-8"))
    except:
        M = {}
    if M:
        unidade = M.get("unidade", unidade)
        if M.get("data_medicao"):
            data_medicao_iso = M["data_medicao"]
            data_medicao = fmt_dt_iso(data_medicao_iso)
        rate_kgph        = M.get("taxa_kgch4_h", rate_kgph)
        uncert_pct       = M.get("incerteza_pct", uncert_pct)
        estado_mar       = M.get("estado_mar", estado_mar)
        plataforma       = M.get("plataforma", plataforma)
        objetos          = M.get("objetos_detectados", objetos)
        flare_ativo      = bool(M.get("flare_ativo", flare_ativo))
        detec_pluma      = bool(M.get("detec_pluma", detec_pluma))
        ident_pluma      = bool(M.get("ident_pluma", ident_pluma))
        dir_vento_graus  = M.get("dir_vento_graus", dir_vento_graus)
        vento_media_ms   = M.get("vento_media_ms", vento_media_ms)
        vento_erro_ms    = M.get("vento_erro_ms", vento_erro_ms)
        resolucao_m      = M.get("resolucao_m", resolucao_m)
        if M.get("img_swir"):
            v = M["img_swir"]
            if isinstance(v, str) and v.startswith("data:image/"):
                img_uri = v
            else:
                p = Path(str(v))
                if p.exists():
                    img_uri = as_data_uri(p)

# Tabelas painel
swir_rows = f"""
<tr><th>Detecção da Pluma de Metano</th><td>{"Sim" if detec_pluma else "Não"}</td></tr>
<tr><th>Identificação da Pluma de Metano</th><td>{"Sim" if ident_pluma else "Não"}</td></tr>
<tr><th>Concentração de Metano (kgCH₄/hr)</th><td>{rate_kgph}</td></tr>
<tr><th>Incerteza (%)</th><td>±{uncert_pct}%</td></tr>
"""
rgb_rows = f"""
<tr><th>Estado do Mar</th><td>{estado_mar}</td></tr>
<tr><th>Plataforma</th><td>{plataforma}</td></tr>
<tr><th>Objetos Detectados</th><td>{", ".join(objetos)}</td></tr>
<tr><th>Flare Ativo</th><td>{'Sim 🟢' if flare_ativo else 'Não ⚪'}</td></tr>
"""
met_rows = f"""
<tr><th>Velocidade Média do Vento (m/s)</th><td>{vento_media_ms} ±{vento_erro_ms}</td></tr>
<tr><th>Direção do Vento (deg)</th><td>{dir_vento_graus} (de onde sopra)</td></tr>
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
body{margin:0;height:100vh;width:100vw;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Helvetica Neue,Arial,Noto Sans,sans-serif}
.stage{min-height:100vh;width:100vw;position:relative}

/* ===== Figura (esquerda) ===== */
.visual-wrap{
  position:absolute; top:var(--gap); bottom:100px; left:var(--gap);
  right:calc(var(--panel-w) + var(--gap)*2);
  border:1px solid var(--border); border-radius:12px; overflow:hidden;
  box-shadow:0 18px 44px rgba(0,0,0,.35); background:#0f172a;
  display:flex; flex-direction:column;
}
.v-header{
  background:#1f497d; color:#e8f0ff; padding:8px 12px; font-weight:800; font-size:1.5rem;
  border-bottom:1px solid rgba(255,255,255,.2); position:relative;
}
.v-body{position:relative; flex:1; background:#0b1327; overflow:hidden}
.v-body .img-holder{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
}
.v-body img{max-width:100%; max-height:100%; object-fit:contain; background:#0b1327;}
.v-footer{padding:8px 10px; color:#b9c6e6; font-size:.82rem; background:#0e172b; border-top:1px solid var(--border)}

/* ações no header da figura */
.vh-actions{position:absolute; right:10px; top:6px; display:flex; gap:8px}
.pill{
  height:30px; padding:0 12px; border-radius:999px; border:1px solid rgba(255,255,255,.25);
  background:rgba(0,0,0,.28); color:#fff; font-weight:800; font-size:.82rem; cursor:pointer;
  backdrop-filter: blur(3px) saturate(130%);
}

/* ===== Timeline ===== */
.timeline{
  position:absolute; left:var(--gap); right:calc(var(--panel-w) + var(--gap)*2);
  bottom:var(--gap); height:84px; border:1px solid var(--border); border-radius:10px;
  background:#0f1a2e; display:flex; flex-direction:column; justify-content:space-between;
  padding:8px 10px; box-shadow:0 10px 24px rgba(0,0,0,.35);
}
.ticks{display:flex; gap:20px; align-items:center; overflow:auto; color:#cfe7ff; font-size:.85rem}

/* ===== Painel direito ===== */
.side-panel{
  position:absolute; top:var(--gap); right:var(--gap); bottom:var(--gap);
  width:var(--panel-w); background:var(--card); border:1px solid var(--border);
  border-radius:18px; box-shadow:0 18px 44px rgba(0,0,0,.45);
  padding:14px; display:flex; flex-direction:column; gap:12px; overflow:auto;
  backdrop-filter:saturate(140%) blur(6px);
}
.header{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}
.brand{display:flex;gap:12px;align-items:center}
.brand .logo{width:82px;height:82px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;border:1px solid var(--border)}
.brand .txt .name{font-weight:900;letter-spacing:.2px}
.brand .txt .sub{font-size:.86rem;color:#9fb0d4}
.badge{justify-self:end;background:rgba(0,227,165,.12);color:#00E3A5;border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}
.hr{height:1px;background:var(--border);margin:6px 0 10px 0}
.block{border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.4)}
.block .title{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center;font-size:1.5rem}
.block .body{padding:10px}
table.minimal{width:100%;border-collapse:collapse}
table.minimal th, table.minimal td{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:1.5rem}
table.minimal th{color:#9fb0d4;font-weight:700}
.footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem}
</style>
</head>
<body>
<div class="stage" id="stage">

  <!-- FIGURA -->
  <div class="visual-wrap" id="visual">
    <div class="v-header">
      Satélite CHGSAT – Sensor SWIR
      <div class="vh-actions">
        <button id="btnExport8K" class="pill" title="Exportar PNG 8K do dashboard">PNG 8K</button>
        <button id="btnExport8KFig" class="pill" title="Exportar PNG 8K apenas da figura">PNG 8K (Figura)</button>
        <button id="btnPdfA4" class="pill" title="Exportar PDF A4 (paisagem)">PDF A4</button>
        <button id="btnPdfA3" class="pill" title="Exportar PDF A3 (paisagem)">PDF A3</button>
      </div>
    </div>

    <div class="v-body" id="vbody">
      <div class="img-holder" id="imgHolder">
        <img id="theImage" src="__IMG__" alt="figura"/>
      </div>
    </div>

    <div class="v-footer">
      Imagem ilustrativa criada para demonstração de capacidade tecnológica. Não representa medições reais nem está vinculada a contratos, clientes ou operações comerciais.
    </div>
  </div>

  <!-- TIMELINE -->
  <div class="timeline">
    <div style="color:#9fb0d4;font-weight:800;">Linha do tempo (passagens)</div>
    <div class="ticks" id="tl"></div>
  </div>

  <!-- PAINEL DIREITO -->
  <div class="side-panel" id="panel">
    <div class="header">
      <div class="brand">
        <div class="logo">__LOGO_HTML__</div>
        <div class="txt">
          <div class="name">Relatório OGMP 2.0 • L5</div>
          <div class="sub">Unidade: __UNIDADE__</div>
        </div>
      </div>
      <div class="badge">SENSOR SWIR</div>
    </div>
    <div class="hr"></div>

    <!-- Bloco Aquisição -->
    <div class="block"><div class="title">Aquisição</div>
      <div class="body"><table class="minimal">
        <tr><th>Data da Aquisição</th><td>__DATA_MED__</td></tr>
        <tr><th>Hora</th><td>__HORA__</td></tr>
        <tr><th>Resolução</th><td>__RES__ m</td></tr>
      </table></div>
    </div>

    <div class="block"><div class="title">Resultados derivados do satélite SWIR</div>
      <div class="body"><table class="minimal">__SWIR_ROWS__</table></div></div>

    <div class="block"><div class="title">Resultados derivados do satélite RGB</div>
      <div class="body"><table class="minimal">__RGB_ROWS__</table></div></div>

    <div class="block"><div class="title">Dados Meteorológicos — GEOS</div>
      <div class="body"><table class="minimal">__MET_ROWS__</table></div></div>

    <div class="footer"><div>© __YEAR__ MAVIPE Sistemas Espaciais</div><div></div></div>
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

// ========= PNG 8K (Hi-DPI + zoom-out opcional)
async function exportPNG8K(el, fname, opts={}){
  const longSide = opts.longSide || 7680;
  const capScale = opts.capScale || 6;
  const zoomOut  = opts.zoomOut  ?? 0.67; // 67% costuma melhorar nitidez

  const rect = el.getBoundingClientRect();
  const w = Math.max(1, Math.ceil(rect.width));
  const h = Math.max(1, Math.ceil(rect.height));
  const base = Math.max(w, h);
  const dpr = Math.max(1, window.devicePixelRatio || 1);
  let scale = Math.min(capScale, (longSide / base) * (dpr > 1 ? dpr : 1));

  const body = document.body;
  const hasZoom = (typeof body.style.zoom !== 'undefined');
  const prevZoom = body.style.zoom;
  if (hasZoom && zoomOut && zoomOut > 0 && zoomOut < 1){
    body.style.zoom = (zoomOut*100) + '%';
    await new Promise(r => requestAnimationFrame(()=>requestAnimationFrame(r)));
  }

  try{
    const canvas = await html2canvas(el, { backgroundColor:null, useCORS:true, logging:false, scale });
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
    if (hasZoom) body.style.zoom = prevZoom || '';
  }
}
document.getElementById('btnExport8K')?.addEventListener('click', ()=> exportPNG8K(document.getElementById('stage'),  'dap-atlas_app_8k_{ts}_{w}x{h}.png', {longSide:7680, capScale:6, zoomOut:0.67}) );
document.getElementById('btnExport8KFig')?.addEventListener('click', ()=> exportPNG8K(document.getElementById('visual'), 'dap-atlas_fig_8k_{ts}_{w}x{h}.png',  {longSide:7680, capScale:6, zoomOut:0.67}) );

// ======== PDF vetorial via janela de impressão ========
function printAsPDF(el, {size='A4', orientation='landscape'} = {}){
  const w = window.open('', '_blank', 'noopener,noreferrer,width=1200,height=800');
  const stage = el.cloneNode(true);

  // fundo branco suave para impressão
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
  .replace("__LOGO_HTML__", logo_html).replace("__UNIDADE__", unidade)
  .replace("__DATA_MED__", data_medicao).replace("__HORA__", hora_local).replace("__RES__", str(resolucao_m))
  .replace("__IMG__", img_uri or "")
  .replace("__SWIR_ROWS__", swir_rows).replace("__RGB_ROWS__", rgb_rows).replace("__MET_ROWS__", met_rows)
  .replace("__YEAR__", str(datetime.now().year))
  .replace("__PASSES_JSON__", json.dumps(passes, ensure_ascii=False))
)

components.html(html, height=1400, scrolling=False)
