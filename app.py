# -*- coding: utf-8 -*-
# DAP ATLAS — OGMP 2.0 L5 (mock SaaS)
# DUAS IMAGENS (esq/dir) com chips de horário em cada lado
from datetime import datetime, timezone
from base64 import b64encode
from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — OGMP 2.0 L5", page_icon="🛰️", layout="wide")

# ===== Theme
PRIMARY, BG, CARD, TEXT, MUTED, BORDER = "#00E3A5", "#0b1221", "#10182b", "#FFFFFF", "#9fb0c9", "rgba(255,255,255,.10)"
PANEL_W_PX, PANEL_GAP_PX = 560, 24

def as_data_uri(path: Path) -> str:
    return "data:image/" + path.suffix.lstrip(".") + ";base64," + b64encode(path.read_bytes()).decode("ascii")

def fmt_dt_iso(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z","+00:00")).astimezone(timezone.utc)
        return dt.strftime("%d/%m/%Y — %H:%M (UTC)")
    except Exception:
        return iso

def diff_minutes(a: str, b: str) -> int | None:
    try:
        d1 = datetime.fromisoformat(a.replace("Z","+00:00")).astimezone(timezone.utc)
        d2 = datetime.fromisoformat(b.replace("Z","+00:00")).astimezone(timezone.utc)
        return int(abs((d2-d1).total_seconds())//60)
    except Exception:
        return None

# ===== Logo
logo_uri = ""
p_logo = Path("dapatlas_fundo_branco.png")
if p_logo.exists() and p_logo.stat().st_size>0:
    logo_uri = as_data_uri(p_logo)
logo_html = f"<img src='{logo_uri}' alt='DAP ATLAS' style='width:82px;height:82px;object-fit:contain;'/>" if logo_uri else "<div style='font-weight:900;color:#000'>DA</div>"

# ===== Visual: OU imagem combinada OU duas imagens
COMBINED_PATH = Path("split_combo.png")  # se existir, usa combinada; senão, usa esquerda/direita
combined_uri = as_data_uri(COMBINED_PATH) if COMBINED_PATH.exists() and COMBINED_PATH.stat().st_size>0 else ""

left_path, right_path = Path("left.png"), Path("right.png")
left_uri  = as_data_uri(left_path)  if left_path.exists()  and left_path.stat().st_size>0  else ""
right_uri = as_data_uri(right_path) if right_path.exists() and right_path.stat().st_size>0 else ""

# ===== Dados padrão
unidade      = "Rio de Janeiro"
data_medicao = "12/07/2025 — 10:42 (UTC)"
rate_kgph    = 180
uncert_pct   = 10
spark_hist   = [160,170,150,180,175,182,180]
passes       = [{"sat":"GHGSat-C10","t":"13/07/2025 – 09:12","ang":"52°"},
                {"sat":"GHGSat-C12","t":"14/07/2025 – 10:03","ang":"47°"},
                {"sat":"GHGSat-C11","t":"15/07/2025 – 08:55","ang":"49°"}]
img_rgb, img_swir = "", ""
cb_max = 1000

# Horários das metades (chips)
rgb_iso  = "2025-04-29T08:06:00Z"   # aquis. da imagem da ESQUERDA
swir_iso = "2025-04-29T10:36:00Z"   # aquis. da imagem da DIREITA
rgb_h, swir_h = fmt_dt_iso(rgb_iso), fmt_dt_iso(swir_iso)
delta_min = diff_minutes(rgb_iso, swir_iso) or 0

# ===== Carrega JSON opcional (se quiser injetar dinamicamente)
M = {}
mfile = Path("sample_measurement.json")
if mfile.exists() and mfile.stat().st_size>0:
    try: M = json.loads(mfile.read_text(encoding="utf-8"))
    except: M = {}

if M:
    unidade      = M.get("unidade", unidade)
    if M.get("data_medicao"): data_medicao = fmt_dt_iso(M["data_medicao"])
    rate_kgph    = M.get("taxa_kgch4_h", rate_kgph)
    uncert_pct   = M.get("incerteza_pct", uncert_pct)
    passes       = M.get("passes", passes)
    img_rgb      = M.get("img_rgb", img_rgb)
    img_swir     = M.get("img_swir", img_swir)
    cb_max       = M.get("colorbar_max_ppb", cb_max)
    rgb_iso      = M.get("rgb_datetime_iso", rgb_iso)
    swir_iso     = M.get("swir_datetime_iso", swir_iso)
    rgb_h, swir_h = fmt_dt_iso(rgb_iso), fmt_dt_iso(swir_iso)
    delta_min    = diff_minutes(rgb_iso, swir_iso) or delta_min

passes_rows = "\n".join(f"<tr><td>{p.get('sat','-')}</td><td>{p.get('t','-').replace('T',' ').replace('Z',' UTC')}</td><td>{p.get('ang','-')}</td></tr>" for p in passes)

swir_rows = f"""
<tr><th>Detecção da Pluma</th><td>{'Sim' if M.get('detec_pluma', True) else 'Não'}</td></tr>
<tr><th>Identificação da Pluma</th><td>{'Sim' if M.get('ident_pluma', True) else 'Não'}</td></tr>
<tr><th>Concentração (kgCH₄/h)</th><td>{M.get('taxa_kgch4_h', rate_kgph)}</td></tr>
<tr><th>Incerteza (%)</th><td>±{M.get('incerteza_pct', uncert_pct)}</td></tr>
"""
rgb_rows = f"""
<tr><th>Estado do Mar</th><td>{M.get('estado_mar','Calmo')}</td></tr>
<tr><th>Plataforma</th><td>{M.get('plataforma','FPSO')}</td></tr>
<tr><th>Objetos Detectados</th><td>{', '.join(M.get('objetos_detectados', ['Possível flotel']))}</td></tr>
<tr><th>Flare Ativo</th><td>{'Sim' if M.get('flare_ativo', True) else 'Não'}</td></tr>
"""
met_rows = f"""
<tr><th>Velocidade do Vento (m/s)</th><td>{M.get('vento_media_ms', 5.2)} ± {M.get('vento_erro_ms', 2.0)}</td></tr>
<tr><th>Direção do Vento (°)</th><td>{M.get('dir_vento_graus', 270)} (de onde sopra)</td></tr>
"""

# ===== HTML
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

/* ===== Área visual (esquerda) ===== */
.split-wrap{
  position:absolute; top:var(--gap); bottom:var(--gap); left:var(--gap);
  right:calc(var(--panel-w) + var(--gap)*2);
  border:1px solid var(--border); border-radius:12px; overflow:hidden;
  box-shadow:0 18px 44px rgba(0,0,0,.35); background:#0f172a;
}

/* MODO 1: imagem única já dividida */
.split-one{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#0e1629}
.split-one img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block}
.split-one::before{content:""; position:absolute; left:50%; top:0; width:1px; height:100%; background:rgba(255,255,255,.12)}

/* Chips de horário */
.chip{
  position:absolute; top:10px; padding:8px 12px; border-radius:999px; font-size:1.0rem; font-weight:800;
  color:#eaf2ff; background:rgba(10,18,34,.78); border:1px solid rgba(255,255,255,.18);
  backdrop-filter:saturate(140%) blur(4px)
}
.chip.left{left:10px}
.chip.right{right:10px}

/* MODO 2 (fallback): duas células COM chips */
.split-grid{height:100%; width:100%; display:grid; grid-template-columns:1fr 1fr; gap:0; position:relative}
.split-grid .cell{position:relative; overflow:hidden; background:#0e1629; display:flex; align-items:center; justify-content:center}
.split-grid img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block}
.split-grid::before{content:""; position:absolute; left:50%; top:0; width:1px; height:100%; background:rgba(255,255,255,.12)}

/* ===== Painel lateral ===== */
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
.kpi{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:12px;padding:14px 12px;text-align:center;position:relative}
.kpi .label{color:#b9c6e6;font-size:.9rem;margin-bottom:4px}
.kpi .value{font-weight:900;font-size:1.6rem}
.kpi .unit{font-size:.95rem;color:#cbd6f2;margin-left:4px}
.spark{width:100%;height:20px;margin-top:6px}
.badge-pos,.badge-neg{display:inline-block;margin-left:8px;padding:3px 8px;border-radius:999px;font-weight:800;font-size:.8rem}
.badge-pos{background:rgba(52,211,153,.16);color:#34d399;border:1px solid rgba(52,211,153,.35)}
.badge-neg{background:rgba(248,113,113,.16);color:#f87171;border:1px solid rgba(248,113,113,.35)}
.gbox{display:flex;gap:10px;align-items:center;justify-content:center;margin-top:6px}
.gauge{width:72px;height:72px}
.gauge .bg{fill:none;stroke:rgba(255,255,255,.15);stroke-width:6}
.gauge .val{fill:none;stroke:#34D399;stroke-width:6;transform:rotate(-90deg);transform-origin:50% 50%}

/* Tabs */
.tabs{margin-top:4px}
.tabs input{display:none}
.tabs label{display:inline-block;padding:8px 12px;margin-right:8px;border:1px solid var(--border);border-bottom:none;border-top-left-radius:10px;border-top-right-radius:10px;color:#9fb0d4;background:rgba(255,255,255,.02);cursor:pointer;font-weight:700;font-size:.92rem}
.tabs input:checked + label{color:#08121f;background:var(--primary);border-color:var(--primary)}
.tab-content{border:1px solid var(--border);border-radius:0 12px 12px 12px;padding:12px;margin-top:-1px}

table.minimal{width:100%;border-collapse:collapse}
table.minimal th, table.minimal td{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}
table.minimal th{color:#9fb0d4;font-weight:700}

.mapbox{height:220px;border:1px dashed rgba(255,255,255,.18);border-radius:10px;background:linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.02));display:flex;align-items:center;justify-content:center;color:#a9b8df}
.timeline{display:flex;gap:12px;overflow:auto;padding:8px;border:1px solid var(--border);border-radius:10px;background:#0f1a2e;margin-top:10px}
.badge-pass{min-width:190px;padding:8px 10px;border-radius:10px;background:rgba(255,255,255,.04);border:1px solid var(--border)}
.badge-pass b{color:#e6eefc}

.footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#a9b8df;font-size:.85rem}
</style>
</head>
<body>
<div class="stage">

  <!-- VISUAL AREA -->
  <div class="split-wrap">
    __COMBINED_OR_GRID__
  </div>

  <!-- SIDE PANEL -->
  <div class="side-panel" id="panel">
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

    <div class="block">
      <div class="body" style="padding:10px 12px">
        <div style="font-weight:800;font-size:1rem;margin-bottom:4px">Unidade: __UNIDADE__</div>
        <div style="font-size:.9rem;color:#b9c6e6">Data da Medição: __DATA_MEDICAO__</div>
        <div style="margin-top:8px">
          <span style="background:rgba(78,168,222,.18);border:1px solid rgba(78,168,222,.35);color:#cfe7ff;padding:6px 10px;border-radius:999px;font-weight:800;font-size:.85rem;">
            Diferença entre passagens: __DELTA_MIN__ min
          </span>
        </div>
      </div>
    </div>

    <div class="tabs">
      <input type="radio" name="tab" id="tab-medicao" checked><label for="tab-medicao">Medição Atual</label>
      <input type="radio" name="tab" id="tab-passes"><label for="tab-passes">Próximos Passes</label>
      <input type="radio" name="tab" id="tab-result"><label for="tab-result">Resultados</label>
      <input type="radio" name="tab" id="tab-meta"><label for="tab-meta">Metadados</label>
      <input type="radio" name="tab" id="tab-resumo"><label for="tab-resumo">Resumo</label>

      <div class="tab-content" id="content-medicao">
        <div class="kpi2">
          <div class="kpi">
            <div class="label">Taxa</div>
            <div><span class="value" id="rate-val">__RATE__</span><span class="unit">kg CH₄/h</span><span id="rate-delta" class="badge-pos" style="display:none"></span></div>
            <svg class="spark" viewBox="0 0 100 28" preserveAspectRatio="none" id="sp-rate"></svg>
          </div>
          <div class="kpi">
            <div class="label">Incerteza de Medição</div>
            <div style="display:flex;align-items:center;justify-content:center;gap:6px">
              <span class="value" id="unc-val">__UNC__</span><span class="unit">%</span>
            </div>
            <div class="gbox">
              <svg viewBox="0 0 42 42" class="gauge"><circle class="bg" cx="21" cy="21" r="16"/><circle class="val" cx="21" cy="21" r="16" stroke-dasharray="0,100"/></svg>
            </div>
          </div>
        </div>
      </div>

      <div class="tab-content" id="content-passes" style="display:none">
        <div id="map-passes" class="mapbox">Mini-mapa de footprints</div>
        <div class="timeline" id="tl"></div>
        <div style="height:10px"></div>
        <table class="minimal"><thead><tr><th>Satélite</th><th>Data/Hora (UTC)</th><th>Ângulo</th></tr></thead><tbody>__PASSES_ROWS__</tbody></table>
      </div>

      <div class="tab-content" id="content-result" style="display:none">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
          <div class="block"><div class="title">Satélite RGB</div>
            <div class="body" style="padding:0">
              <img src="__IMG_RGB__" style="width:100%;height:auto;display:block;__IMG_RGB_STYLE__;border-bottom:1px solid var(--border)"/>
              <div style="padding:8px 10px;color:#b9c6e6;font-size:.85rem"><b>Data/Hora de Aquisição:</b> __RGB_HUMAN__<br>Imagem de referência visual</div>
            </div>
          </div>
          <div class="block"><div class="title">Satélite SWIR (CH₄)</div>
            <div class="body" style="padding:0;position:relative">
              <img src="__IMG_SWIR__" style="width:100%;height:auto;display:block;__IMG_SWIR_STYLE__"/>
              <div style="position:absolute;right:8px;top:8px;background:#0f1a2e;border:1px solid var(--border);border-radius:8px;padding:6px 8px;font-size:.85rem">0 – __CB_MAX__ ppb</div>
              <div style="padding:8px 10px;color:#b9c6e6;font-size:.85rem"><b>Data/Hora de Aquisição:</b> __SWIR_HUMAN__<br>Realce qualitativo (EABB)</div>
            </div>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px">
          <div class="block"><div class="title">Resultados SWIR</div><div class="body"><table class="minimal">__SWIR_ROWS__</table></div></div>
          <div class="block"><div class="title">Resultados RGB</div><div class="body"><table class="minimal">__RGB_ROWS__</table></div></div>
          <div class="block"><div class="title">Dados Meteorológicos</div><div class="body"><table class="minimal">__MET_ROWS__</table></div></div>
        </div>
      </div>

      <div class="tab-content" id="content-meta" style="display:none">
        <table class="minimal"><tr><th>Gerado em</th><td>__AGORA__</td></tr><tr><th>Sistema</th><td>DAP ATLAS — OGMP 2.0</td></tr></table>
      </div>

      <div class="tab-content" id="content-resumo" style="display:none">
        <p>Mockup do painel OGMP 2.0 L5 com área visual e KPIs.</p>
      </div>
    </div>

    <div class="footer"><div>© __YEAR__ MAVIPE Sistemas Espaciais</div><div></div></div>
  </div>
</div>

<script>
// abas
const elMed=document.getElementById('content-medicao'), elPas=document.getElementById('content-passes'),
      elResu=document.getElementById('content-result'), elMeta=document.getElementById('content-meta'),
      elRes=document.getElementById('content-resumo');
function show(w){elMed.style.display=(w==='med')?'block':'none'; elPas.style.display=(w==='pas')?'block':'none';
  elResu.style.display=(w==='resu')?'block':'none'; elMeta.style.display=(w==='met')?'block':'none'; elRes.style.display=(w==='res')?'block':'none';}
document.getElementById('tab-medicao').onchange=()=>show('med');
document.getElementById('tab-passes').onchange =()=>show('pas');
document.getElementById('tab-result').onchange =()=>show('resu');
document.getElementById('tab-meta').onchange   =()=>show('met');
document.getElementById('tab-resumo').onchange =()=>show('res');

// sparkline + delta
const dataSpark=__SPARK__;
(function(){
  const el=document.getElementById('sp-rate'), data=dataSpark&&dataSpark.length?dataSpark:[__RATE__];
  const W=100,H=28,p=2,min=Math.min(...data),max=Math.max(...data);
  const x=i=>p+i*((W-p*2)/(data.length-1||1)), y=v=>H-p-((v-min)/(max-min||1))*(H-p*2);
  el.innerHTML=`<polyline fill="none" stroke="#4EA8DE" stroke-width="2" points="${data.map((v,i)=>`${x(i)},${y(v)}`).join(' ')}"/>`;
  if(data.length>1){const prev=data.slice(0,-1).reduce((a,b)=>a+b,0)/(data.length-1), last=data[data.length-1];
    const d=((last-prev)/Math.max(prev,1e-6))*100, tag=document.getElementById('rate-delta');
    tag.textContent=(d>=0?'↑ ':'↓ ')+Math.abs(d).toFixed(1)+'%'; tag.className=(d>=0)?'badge-pos':'badge-neg'; tag.style.display='inline-block';}
})();

// gauge
(function(){const unc=Number(document.getElementById('unc-val').textContent)||0;
  document.querySelector('.gauge .val').setAttribute('stroke-dasharray', `${Math.max(0,Math.min(100,unc*3.6))},100`);
})();

// passes mock
const passes=__PASSES_JSON__;
(function(){
  const div=document.getElementById('map-passes'), W=300,H=220;
  let svg=`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:100%"><rect x="0" y="0" width="${W}" height="${H}" fill="#0e172b"/>`;
  passes.forEach((p,i)=>{const cx=60+i*90, cy=110+(i%2?-20:20), ang=parseInt((p.ang||'0').replace('°',''))||45;
    const r=25+Math.min(35,Math.max(0,(ang-30))), col=i%3===0?'#4EA8DE':(i%3===1?'#34d399':'#F59E0B');
    svg+=`<circle cx="${cx}" cy="${cy}" r="${r}" fill="${col}20" stroke="${col}"/>`;});
  div.innerHTML=svg+`</svg>`;
  document.getElementById('tl').innerHTML=passes.map(p=>`<div class="badge-pass"><b>${p.sat}</b><br><small>${p.t} • ${p.ang}</small></div>`).join('');
})();
</script>
</body></html>
"""

# ===== decidir o bloco visual (com chips nos dois modos)
if combined_uri:
    combined_block = (
        f"<div class='split-one'>"
        f"<img src='{combined_uri}' alt='split'/>"
        f"<span class='chip left'>RGB: {fmt_dt_iso(rgb_iso)}</span>"
        f"<span class='chip right'>SWIR: {fmt_dt_iso(swir_iso)}</span>"
        f"</div>"
    )
else:
    left_html  = f"<img src='{left_uri}'  alt='Left'/>"  if left_uri  else "<div style='color:#9fb0d4'>left.png</div>"
    right_html = f"<img src='{right_uri}' alt='Right'/>" if right_uri else "<div style='color:#9fb0d4'>right.png</div>"
    # >>> chips adicionados em CADA célula <<<
    combined_block = (
        "<div class='split-grid'>"
          f"<div class='cell'>{left_html}<span class='chip left'>RGB: {fmt_dt_iso(rgb_iso)}</span></div>"
          f"<div class='cell'>{right_html}<span class='chip right'>SWIR: {fmt_dt_iso(swir_iso)}</span></div>"
        "</div>"
    )

# ===== Replace
html = (html
  .replace("__PANEL_W__", str(PANEL_W_PX)).replace("__PANEL_GAP__", str(PANEL_GAP_PX))
  .replace("__PRIMARY__", PRIMARY).replace("__BG__", BG).replace("__CARD__", CARD)
  .replace("__TEXT__", TEXT).replace("__MUTED__", MUTED).replace("__BORDER__", BORDER)
  .replace("__LOGO_HTML__", logo_html).replace("__UNIDADE__", unidade)
  .replace("__DATA_MEDICAO__", data_medicao).replace("__DELTA_MIN__", str(delta_min))
  .replace("__RATE__", str(rate_kgph)).replace("__UNC__", str(uncert_pct))
  .replace("__PASSES_ROWS__", passes_rows).replace("__PASSES_JSON__", json.dumps(passes, ensure_ascii=False))
  .replace("__SPARK__", json.dumps(spark_hist)).replace("__AGORA__", datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"))
  .replace("__YEAR__", str(datetime.now().year)).replace("__IMG_RGB__", img_rgb or "").replace("__IMG_SWIR__", img_swir or "")
  .replace("__CB_MAX__", str(cb_max)).replace("__SWIR_ROWS__", swir_rows).replace("__RGB_ROWS__", rgb_rows)
  .replace("__MET_ROWS__", met_rows).replace("__IMG_RGB_STYLE__", "display:block" if img_rgb else "display:none")
  .replace("__IMG_SWIR_STYLE__", "display:block" if img_swir else "display:none")
  .replace("__RGB_HUMAN__", fmt_dt_iso(rgb_iso)).replace("__SWIR_HUMAN__", fmt_dt_iso(swir_iso))
  .replace("__COMBINED_OR_GRID__", combined_block)
)

components.html(html, height=1000, scrolling=False)
