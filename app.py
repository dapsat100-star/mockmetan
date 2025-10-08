# -*- coding: utf-8 -*-
# DAP ATLAS — Mock SaaS (figura única + painel)
# Toolbar vertical à DIREITA, próxima ao painel lateral.

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
        return dt.strftime("%d/%m/%Y — %H:%M (UTC)")
    except Exception:
        return iso

# ===================== LOGO =====================
logo_uri = ""
p_logo = Path("dapatlas_fundo_branco.png")
if p_logo.exists() and p_logo.stat().st_size>0:
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
fig_path = next((p for n in candidates if (p:=Path(n)).exists() and p.stat().st_size>0), None)
img_uri = as_data_uri(fig_path) if fig_path else ""

# ===================== DADOS MOCK / JSON =====================
unidade      = "Rio de Janeiro"
data_medicao_iso = "2025-04-29T10:36:00Z"
data_medicao = fmt_dt_iso(data_medicao_iso)
hora_local   = "10h36"
resolucao_m  = 25
rate_kgph    = 180
uncert_pct   = 12
estado_mar   = "Calmo"
plataforma   = "FPSO"
objetos      = ["Possível flotel"]
flare_ativo  = True
detec_pluma  = True
ident_pluma  = True
dir_vento_graus = 270
vento_media_ms  = 5.2
vento_erro_ms   = 2.0
cb_max = 1000
passes = [
    {"sat":"GHGSat-C10","t":"29/04/2025 – 10:36","ang":"52°"},
    {"sat":"GHGSat-C12","t":"30/04/2025 – 10:08","ang":"47°"},
]

# JSON opcional
mfile = Path("sample_measurement.json")
if mfile.exists() and mfile.stat().st_size>0:
    try: M = json.loads(mfile.read_text(encoding="utf-8"))
    except: M = {}
    if M:
        unidade = M.get("unidade", unidade)
        if M.get("data_medicao"):
            data_medicao_iso = M["data_medicao"]; data_medicao = fmt_dt_iso(data_medicao_iso)
        rate_kgph    = M.get("taxa_kgch4_h", rate_kgph)
        uncert_pct   = M.get("incerteza_pct", uncert_pct)
        estado_mar   = M.get("estado_mar", estado_mar)
        plataforma   = M.get("plataforma", plataforma)
        objetos      = M.get("objetos_detectados", objetos)
        flare_ativo  = bool(M.get("flare_ativo", flare_ativo))
        detec_pluma  = bool(M.get("detec_pluma", detec_pluma))
        ident_pluma  = bool(M.get("ident_pluma", ident_pluma))
        dir_vento_graus = M.get("dir_vento_graus", dir_vento_graus)
        vento_media_ms  = M.get("vento_media_ms", vento_media_ms)
        vento_erro_ms   = M.get("vento_erro_ms", vento_erro_ms)
        cb_max          = M.get("colorbar_max_ppb", cb_max)
        resolucao_m     = M.get("resolucao_m", resolucao_m)
        if M.get("img_swir"):
            v = M["img_swir"]
            if isinstance(v, str) and v.startswith("data:image/"): img_uri = v
            else:
                p = Path(str(v))
                if p.exists(): img_uri = as_data_uri(p)

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
  background:#1f497d; color:#e8f0ff; padding:8px 12px; font-weight:800; font-size:.92rem;
  border-bottom:1px solid rgba(255,255,255,.2)
}
.v-body{position:relative; flex:1; background:#0b1327; overflow:hidden}
.v-body .img-holder{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  transform-origin:center center; /* zoom/pan */
}
.v-body img{max-width:100%; max-height:100%; object-fit:contain; background:#0b1327;}
.colorbar{
  position:absolute; right:10px; bottom:12px; width:18px; height:52%;
  border:1px solid rgba(255,255,255,.3);
  background: linear-gradient(to top, #2a0845 0%, #00d4ff 40%, #7b2cff 70%, #ff005e 100%);
  border-radius:6px;
}
.cb-label{
  position:absolute; right:36px; bottom:60px; color:#e6eefc; font-weight:800; letter-spacing:.2px;
  transform: rotate(-90deg); transform-origin:right bottom; font-size:.8rem; white-space:nowrap;
}
.v-footer{padding:8px 10px; color:#b9c6e6; font-size:.82rem; background:#0e172b; border-top:1px solid var(--border)}

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
.block .title{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center}
.block .body{padding:10px}
table.minimal{width:100%;border-collapse:collapse}
table.minimal th, table.minimal td{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}
table.minimal th{color:#9fb0d4;font-weight:700}
.footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem}

/* ===== Toolbar flutuante (DIREITA) ===== */
.toolbar{
  position:absolute; top:20px;
  right:calc(var(--panel-w) + var(--gap) + 8px); /* cola na lateral do painel */
  left:auto; display:flex; flex-direction:column; align-items:flex-end; gap:8px; z-index:30;
}
.toolbtn{
  height:36px; min-width:36px; padding:0 10px; border-radius:10px; border:1px solid rgba(255,255,255,.2);
  background:rgba(0,0,0,.28); color:#fff; display:flex; align-items:center; gap:8px; cursor:pointer;
  backdrop-filter: blur(3px) saturate(130%); font-weight:800; font-size:.86rem;
}
.toolbtn svg{width:18px;height:18px}
.badge-pill{
  position:absolute; top:12px; right:12px; background:rgba(0,227,165,.15); color:#baffdf;
  border:1px solid rgba(0,227,165,.35); padding:6px 10px; border-radius:999px; font-weight:800; z-index:30;
}

/* Quando o painel estiver oculto, encosta na borda da figura */
.hide-panel .toolbar{ right:var(--gap) }

/* Toggle painel escondido */
.hide-panel .side-panel{display:none}
.hide-panel .visual-wrap{right:var(--gap)}
.hide-panel .timeline{right:var(--gap)}
</style>
</head>
<body>
<div class="stage" id="stage">

  <div class="badge-pill">Mock • v1.2</div>

  <!-- FIGURA -->
  <div class="visual-wrap" id="visual">
    <!-- Toolbar ações -->
    <div class="toolbar">
      <button class="toolbtn" id="btnZoomIn"  title="Zoom +">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 1 0 14 15.5l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-5 0A4.5 4.5 0 1 1 15 9.5 4.505 4.505 0 0 1 10.5 14zm1-3h-2v2h-1v-2H6v-1h2V8h1v2h2z"/></svg>Zoom
      </button>
      <button class="toolbtn" id="btnZoomOut" title="Zoom −">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 1 0 14 15.5l.27.28v.79l5 4.99L20.49 19l-4.99-5zM7 10h7v1H7z"/></svg>
      </button>
      <button class="toolbtn" id="btnPan" title="Arrastar imagem">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2l2 4h-4l2-4zm0 20l-2-4h4l-2 4zM2 12l4-2v4l-4-2zm20 0l-4 2v-4l4 2zM8 8h8v8H8z"/></svg>Pan
      </button>
      <button class="toolbtn" id="btnTogglePanel" title="Mostrar/ocultar painel">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M3 4h18v16H3V4zm2 2v12h10V6H5zm12 0v12h2V6h-2z"/></svg>Painel
      </button>
      <button class="toolbtn" id="btnExportFig" title="Exportar PNG da figura">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M5 20h14v-2H5v2zM5 4v8h4l-5 5-5-5h4V4h2zm14 8V4h-2v8h-4l5 5 5-5h-4z"/></svg>PNG Área
      </button>
      <button class="toolbtn" id="btnExportAll" title="Exportar PNG do dashboard">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M3 5h18v4H3V5zm0 6h8v8H3v-8zm10 0h8v8h-8v-8z"/></svg>PNG Dashboard
      </button>
      <button class="toolbtn" id="btnInfo" title="Sobre">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M11 17h2v-6h-2v6zm0-8h2V7h-2v2z"/><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/></svg>Info
      </button>
    </div>

    <div class="v-header">Satélite CHGSAT – Sensor SWIR</div>

    <div class="v-body" id="vbody">
      <div class="img-holder" id="imgHolder" style="transform:scale(1) translate(0px,0px)">
        <img id="theImage" src="__IMG__" alt="figura"/>
      </div>
      <div class="colorbar"></div>
      <div class="cb-label">Enhanced Background (ppb) — 0 … __CB_MAX__</div>
    </div>

    <div class="v-footer">
      Imagem demonstrativa de capacidade utilizando dados reais da GHGSat. Uso exclusivamente ilustrativo.
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
        <tr><th>Data da Aquisição (UTC)</th><td>__DATA_MED__</td></tr>
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

// ========= zoom / pan
let scale=1, tx=0, ty=0, panning=false, startX=0, startY=0, panEnabled=false;
const imgHolder = document.getElementById('imgHolder');
const vbody = document.getElementById('vbody');
function applyTransform(){ imgHolder.style.transform = `scale(${scale}) translate(${tx}px,${ty}px)`; }
document.getElementById('btnZoomIn').onclick = ()=>{ scale = Math.min(6, scale*1.2); applyTransform(); }
document.getElementById('btnZoomOut').onclick= ()=>{ scale = Math.max(0.5, scale/1.2); applyTransform(); }
document.getElementById('btnPan').onclick    = ()=>{
  panEnabled = !panEnabled;
  alert(panEnabled ? 'Arraste com o mouse sobre a imagem para mover.' : 'Pan desativado.');
};
vbody.addEventListener('mousedown', (e)=>{ if(!panEnabled) return; panning=true; startX=e.clientX; startY=e.clientY; });
vbody.addEventListener('mousemove', (e)=>{ if(!panning) return; tx += (e.clientX-startX)/scale; ty += (e.clientY-startY)/scale; startX=e.clientX; startY=e.clientY; applyTransform(); });
vbody.addEventListener('mouseup', ()=>{ panning=false; });
vbody.addEventListener('mouseleave', ()=>{ panning=false; });

// ========= toggle painel
document.getElementById('btnTogglePanel').onclick = ()=>{
  document.body.classList.toggle('hide-panel');
};

// ========= exportações
function exportPNGOf(el, fname){
  html2canvas(el, {backgroundColor:null, useCORS:true, logging:false, scale:3}).then(canvas=>{
    canvas.toBlob(function(blob){
      const a=document.createElement('a'); const ts=new Date().toISOString().slice(0,19).replace(/[:T]/g,'-');
      a.href=URL.createObjectURL(blob); a.download=fname.replace('{ts}', ts).replace('{w}', canvas.width).replace('{h}', canvas.height);
      document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(a.href);
    }, 'image/png');
  });
}
document.getElementById('btnExportFig').onclick = ()=> exportPNGOf(document.getElementById('visual'), 'dap-atlas_fig_{ts}_{w}x{h}.png');
document.getElementById('btnExportAll').onclick = ()=> exportPNGOf(document.getElementById('stage'),  'dap-atlas_app_{ts}_{w}x{h}.png');

// ========= info
document.getElementById('btnInfo').onclick = ()=>{
  alert('Mock SaaS DAP ATLAS — toolbar vertical à direita, painel com Aquisição/Resultados/Meteo. Badge: SENSOR SWIR.');
};
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
  .replace("__CB_MAX__", str(cb_max))
  .replace("__SWIR_ROWS__", swir_rows).replace("__RGB_ROWS__", rgb_rows).replace("__MET_ROWS__", met_rows)
  .replace("__YEAR__", str(datetime.now().year))
  .replace("__PASSES_JSON__", json.dumps(passes, ensure_ascii=False))
)
# Reposicionar toolbar para o canto superior direito, colada ao painel lateral
# Override definitivo: fixa a toolbar colada à direita (com !important)
html = html.replace(
    "</head>",
    """
<style id="toolbar-dock-patch">
  /* força a dockagem na direita, acima da imagem */
  .toolbar{
    position:absolute !important;
    top:20px !important;
    left:auto !important;
    right:calc(var(--panel-w) + var(--gap) + 8px) !important;
    display:flex !important;
    flex-direction:column !important;
    align-items:flex-end !important;
    gap:8px !important;
    z-index:1000 !important;
  }
  /* quando o painel estiver oculto, encosta na borda da figura */
  .hide-panel .toolbar{
    right:calc(var(--gap) + 8px) !important;
  }
</style>
</head>
"""
)




components.html(html, height=1000, scrolling=False)


