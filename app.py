# -*- coding: utf-8 -*-
# DAP ATLAS — OGMP 2.0 L5 (mock SaaS) — Layout de UMA figura
# Figura principal (SWIR/RGB) à esquerda + parâmetros à direita (tabelas).
# Inclui: Export PNG (html2canvas) HD/4K/8K.

from datetime import datetime, timezone
from base64 import b64encode
from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — OGMP 2.0 L5", page_icon="🛰️", layout="wide")

# ===================== THEME / VARS =====================
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

# ===================== DADOS (defaults) =====================
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

# ===================== IMAGEM ÚNICA =====================
# Arquivo local (troque o nome conforme seu fluxo)
SINGLE_PATH = Path("fig_swir.png")  # ex.: sua figura final já combinada
if not SINGLE_PATH.exists():
    # fallback: também aceito nomes comuns
    for alt in ["split_combo.png", "swir.png", "figure.png", "WhatsApp Image 2025-10-08 at 1.51.03 AM.jpeg"]:
        p = Path(alt)
        if p.exists() and p.stat().st_size>0:
            SINGLE_PATH = p
            break
img_uri = as_data_uri(SINGLE_PATH) if SINGLE_PATH.exists() and SINGLE_PATH.stat().st_size>0 else ""

# ===================== JSON opcional =====================
M = {}
mfile = Path("sample_measurement.json")
if mfile.exists() and mfile.stat().st_size>0:
    try:
        M = json.loads(mfile.read_text(encoding="utf-8"))
    except:
        M = {}

def get_bool(d, k, default):
    v = d.get(k, default)
    if isinstance(v, str):
        return v.strip().lower() in ("1","true","sim","yes","y","on")
    return bool(v)

if M:
    unidade         = M.get("unidade", unidade)
    if M.get("data_medicao"):
        data_medicao_iso = M["data_medicao"]
        data_medicao = fmt_dt_iso(data_medicao_iso)
    rate_kgph       = M.get("taxa_kgch4_h", rate_kgph)
    uncert_pct      = M.get("incerteza_pct", uncert_pct)
    estado_mar      = M.get("estado_mar", estado_mar)
    plataforma      = M.get("plataforma", plataforma)
    objetos         = M.get("objetos_detectados", objetos)
    flare_ativo     = get_bool(M, "flare_ativo", flare_ativo)
    detec_pluma     = get_bool(M, "detec_pluma", detec_pluma)
    ident_pluma     = get_bool(M, "ident_pluma", ident_pluma)
    dir_vento_graus = M.get("dir_vento_graus", dir_vento_graus)
    vento_media_ms  = M.get("vento_media_ms", vento_media_ms)
    vento_erro_ms   = M.get("vento_erro_ms", vento_erro_ms)
    cb_max          = M.get("colorbar_max_ppb", cb_max)
    resolucao_m     = M.get("resolucao_m", resolucao_m)
    if M.get("img_swir"):
        # se vier data URI ou caminho
        v = M["img_swir"]
        if isinstance(v, str) and v.startswith("data:image/"):
            img_uri = v
        else:
            p = Path(str(v))
            if p.exists():
                img_uri = as_data_uri(p)

# Linhas de tabela (direita)
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

/* ===== Container da figura única ===== */
.visual-wrap{
  position:absolute; top:var(--gap); bottom:120px; left:var(--gap);
  right:calc(var(--panel-w) + var(--gap)*2);
  border:1px solid var(--border); border-radius:12px; overflow:hidden;
  box-shadow:0 18px 44px rgba(0,0,0,.35); background:#0f172a;
  display:flex; flex-direction:column;
}

/* Header azul da figura (satélite, data, hora, resolução) */
.v-header{
  background:#1f497d; color:#e8f0ff; padding:8px 12px; font-weight:700;
  border-bottom:1px solid rgba(255,255,255,.15); font-size:.92rem;
}
.v-header small{display:block;font-weight:600;opacity:.95}

/* Área da imagem */
.v-body{position:relative; flex:1; background:#0b1327; display:flex}
.v-body img{width:100%; height:100%; object-fit:contain; background:#0b1327;}

/* Barra vertical "colorbar" */
.colorbar{
  position:absolute; right:10px; top:50%; transform:translateY(-50%);
  width:18px; height:60%; border:1px solid rgba(255,255,255,.3);
  background: linear-gradient(to top, #000428 0%, #00d4ff 40%, #7b2cff 70%, #ff005e 100%);
  border-radius:6px;
}
.cb-label{
  position:absolute; right:36px; top:50%; transform:translateY(-50%) rotate(-90deg);
  transform-origin:right top;
  color:#e6eefc; font-weight:800; letter-spacing:.3px; white-space:nowrap; font-size:.8rem;
}

/* Legenda/Disclaimer */
.v-footer{
  padding:8px 10px; color:#b9c6e6; font-size:.82rem;
  background:#0e172b; border-top:1px solid var(--border);
}

/* Timeline inferior */
.timeline{
  position:absolute; left:var(--gap); right:calc(var(--panel-w) + var(--gap)*2);
  bottom:var(--gap); height:86px; border:1px solid var(--border); border-radius:10px;
  background:#0f1a2e; display:flex; flex-direction:column; justify-content:space-between;
  padding:8px 10px; box-shadow:0 10px 24px rgba(0,0,0,.35);
}
.ticks{display:flex; gap:24px; align-items:center; overflow:auto; color:#cfe7ff; font-size:.85rem}

/* ===== Painel lateral (parâmetros) ===== */
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
.brand .txt .sub{font-size:.86rem;color:var(--muted)}
.badge{justify-self:end;background:rgba(0,227,165,.12);color:var(--primary);border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}
.hr{height:1px;background:var(--border);margin:6px 0 10px 0}
.block{border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.4)}
.block .title{background:#0e1629;padding:10px;color:#fff;font-weight:900;text-align:center}
.block .body{padding:10px}
table.minimal{width:100%;border-collapse:collapse}
table.minimal th, table.minimal td{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}
table.minimal th{color:#9fb0d4;font-weight:700}

.footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem}

/* Título superior grande (opcional) */
.top-banner{
  position:fixed; left:var(--gap); right:calc(var(--panel-w) + var(--gap)*2);
  top:6px; text-align:center; color:#e6eefc;
  font-weight:900; letter-spacing:.4px; font-size:1.12rem;
}
</style>
</head>
<body>
<div class="stage">

  <div class="top-banner">MAVIPE SISTEMAS ESPACIAIS — DADOS DE EMISSÕES DE METANO</div>

  <!-- FIGURA ÚNICA -->
  <div class="visual-wrap">
    <div class="v-header">
      Satélite CHGSAT – Sensor SWIR
      <small>Data da Aquisição: __DATA_MED__ • Hora: __HORA__ • Resolução: __RES__m</small>
    </div>
    <div class="v-body">
      <img src="__IMG__" alt="figura"/>
      <div class="colorbar" title="Colorbar"></div>
      <div class="cb-label">ENHANCEMENT ABOVE BACKGROUND (ppb)  —  0 … __CB_MAX__</div>
    </div>
    <div class="v-footer">
      Imagem demonstrativa de capacidade utilizando dados reais da GHGSat. Empregada exclusivamente para fins ilustrativos,
      com o objetivo de representar o nível de precisão esperado na detecção e quantificação por satélite SWIR.
    </div>
  </div>

  <!-- TIMELINE (simplificada) -->
  <div class="timeline">
    <div style="color:#9fb0d4;font-weight:800;">Linha do tempo (passagens)</div>
    <div class="ticks" id="tl"></div>
  </div>

  <!-- PAINEL DIREITO (parâmetros) -->
  <div class="side-panel" id="panel">
    <div class="header">
      <div class="brand">
        <div class="logo">__LOGO_HTML__</div>
        <div class="txt">
          <div class="name">Relatório OGMP 2.0 • L5</div>
          <div class="sub">Unidade: __UNIDADE__</div>
        </div>
      </div>
      <div class="badge">DAP ATLAS</div>
    </div>
    <div class="hr"></div>

    <div class="block"><div class="title">Resultados derivados do satélite SWIR</div>
      <div class="body"><table class="minimal">__SWIR_ROWS__</table></div></div>

    <div class="block"><div class="title">Resultados derivados do satélite RGB</div>
      <div class="body"><table class="minimal">__RGB_ROWS__</table></div></div>

    <div class="block"><div class="title">Dados Meteorológicos — GEOS</div>
      <div class="body"><table class="minimal">__MET_ROWS__</table></div></div>

    <div class="footer"><div>© __YEAR__ MAVIPE Sistemas Espaciais</div><div></div></div>
  </div>
</div>

<script>
// timeline
const passes=__PASSES_JSON__;
(function(){
  const tl = document.getElementById('tl');
  tl.innerHTML = passes.map(p=>`<div style="min-width:210px;padding:6px 10px;border-radius:9px;border:1px solid rgba(255,255,255,.18);
     background:rgba(255,255,255,.04)"><b style="color:#e6eefc">${p.sat||'-'}</b><br>
     <small>${(p.t||'-')} • ${(p.ang||'-')}</small></div>`).join('');
})();
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

# ====== EXPORT PNG TOOLBAR ======
export_inject = """
<!-- ===== EXPORT TOOLBAR (HD/4K/8K) ===== -->
<div id="export-toolbar" style="
  position:fixed; z-index:9999; top:12px; right:12px; display:flex; gap:8px;
  font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Helvetica Neue,Arial,sans-serif;">
  <button onclick="exportPNG(2)"  style="padding:8px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.2);
    background:rgba(0,227,165,.15);color:#d7ffe0;font-weight:800;cursor:pointer;">PNG HD</button>
  <button onclick="exportPNG(3)"  style="padding:8px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.2);
    background:rgba(78,168,222,.18);color:#e6f3ff;font-weight:800;cursor:pointer;">PNG 4K</button>
  <button onclick="exportPNG(4)"  style="padding:8px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.2);
    background:rgba(255,255,255,.10);color:#ffffff;font-weight:800;cursor:pointer;">PNG 8K*</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  function exportPNG(scale){
    try{
      const target = document.querySelector('.stage'); // exporta TUDO (figura + painel)
      if(!target){ alert('Elemento .stage não encontrado.'); return; }
      html2canvas(target, {
        scale: scale || 2,
        backgroundColor: null,
        useCORS: true,
        logging: false
      }).then(canvas => {
        canvas.toBlob(function(blob){
          const a = document.createElement('a');
          const ts = new Date().toISOString().slice(0,19).replace(/[:T]/g,'-');
          a.href = URL.createObjectURL(blob);
          a.download = `dap-atlas_${ts}_${canvas.width}x${canvas.height}.png`;
          document.body.appendChild(a); a.click(); document.body.removeChild(a);
          URL.revokeObjectURL(a.href);
        }, 'image/png');
      }).catch(err=>{ console.error(err); alert('Falha ao exportar PNG.'); });
    }catch(e){ console.error(e); alert('Erro inesperado na exportação.'); }
  }
</script>
"""
html = html.replace("</body></html>", export_inject + "\n</body></html>")

# Render
components.html(html, height=1000, scrolling=False)


