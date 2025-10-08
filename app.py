# -*- coding: utf-8 -*-
# DAP ATLAS — OGMP 2.0 L5 (mock SaaS) • Frame 1920x1080 para slides 16:9

from datetime import datetime, timezone
from base64 import b64encode
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — Slide 1920x1080", page_icon="🛰️", layout="wide")

# ================== CONFIG SLIDE ==================
FRAME_W, FRAME_H = 1920, 1080       # tamanho exato do frame 16:9

# ================== THEME ==================
PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

# ================== DADOS MOCK ==================
unidade      = "Rio de Janeiro"
data_medicao = "12/07/2025 — 10:42 (UTC)"

# Horas das cenas (para as tarjas sobre as imagens)
rgb_dt_iso  = "2025-04-29T08:06:00Z"
swir_dt_iso = "2025-04-29T10:36:00Z"

def human_utc(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z","+00:00")).astimezone(timezone.utc)
        return dt.strftime("%d/%m/%Y — %H:%M (UTC)")
    except Exception:
        return iso

rgb_label  = f"RGB: {human_utc(rgb_dt_iso)}"
swir_label = f"SWIR: {human_utc(swir_dt_iso)}"

# diferença em minutos
try:
    t_rgb  = datetime.fromisoformat(rgb_dt_iso.replace("Z","+00:00"))
    t_swir = datetime.fromisoformat(swir_dt_iso.replace("Z","+00:00"))
    diff_min = int(abs((t_swir - t_rgb).total_seconds()) // 60)
except Exception:
    diff_min = 0

# KPIs simples (mock)
rate_kgph  = 180
uncert_pct = 10

# ================== MÍDIA ==================
def as_data_uri(p: Path) -> str:
    if not (p.exists() and p.stat().st_size > 0): return ""
    ext = p.suffix.lower().lstrip(".")
    mime = "image/png" if ext == "png" else ("image/jpeg" if ext in ("jpg","jpeg") else "image/png")
    return f"data:{mime};base64," + b64encode(p.read_bytes()).decode("ascii")

# IMAGEM DA ÁREA VISUAL:
# 1) se existir "composite.png" (ou .jpg), ela ocupa a área 50/50 inteira
# 2) senão, usa left.png e right.png, cada uma numa metade
composite_uri = ""
for name in ("composite.png","composite.jpg","composite.jpeg",
             "Screenshot 2025-10-07 201921.png"):   # seu arquivo já citado
    composite_uri = as_data_uri(Path(name))
    if composite_uri: break

left_uri  = as_data_uri(Path("left.png"))
right_uri = as_data_uri(Path("right.png"))

# LOGO (troque o nome aqui se desejar um arquivo diferente)
logo_uri = as_data_uri(Path("dapatlas_fundo_branco.png"))

# ================== HTML ==================
html = f"""
<!doctype html>
<html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
<style>
:root {{
  --w:{FRAME_W}px; --h:{FRAME_H}px;
  --panel-w:560px; --gap:24px;
  --primary:{PRIMARY}; --bg:{BG_DARK}; --card:{CARD_DARK};
  --text:{TEXT}; --muted:{MUTED}; --border:{BORDER};
}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif}}
/* Frame fixo 1920x1080 e centralizado */
.frame{{width:var(--w);height:var(--h);margin:0 auto;position:relative;
  outline:1px solid rgba(255,255,255,.08);border-radius:12px;overflow:hidden;
  background:radial-gradient(1000px 600px at 70% 40%,rgba(255,255,255,.04),transparent 60%),
             radial-gradient(800px 500px at 30% 70%,rgba(255,255,255,.03),transparent 60%)}}

/* Área visual esquerda (occupy all left of panel) */
.split-wrap{{
  position:absolute; left:var(--gap); top:var(--gap);
  bottom:var(--gap); right:calc(var(--panel-w) + var(--gap)*2);
  border:1px solid var(--border); border-radius:12px; overflow:hidden;
  box-shadow:0 18px 44px rgba(0,0,0,.35); background:#0d1426;
}}
/* grade 50/50 */
.grid50{{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:0;width:100%;height:100%}}
.cell{{position:relative;overflow:hidden}}
.cell img{{width:100%;height:100%;object-fit:cover;display:block}}
/* tarjas de hora */
.tag{{position:absolute; top:10px; left:10px; padding:6px 10px; border-radius:8px;
  background:rgba(0,0,0,.45); color:#eaf2ff; font-weight:700; font-size:12.5px;
  border:1px solid rgba(255,255,255,.18); backdrop-filter:blur(6px) saturate(140%)}}

/* Se usar composite única, só desenhamos uma imagem e dividimos com pseudo-borda */
.grid50.composite::before{{content:"";position:absolute;left:50%;top:0;width:1px;height:100%;background:rgba(255,255,255,.14)}}

/* Painel lateral */
.panel{{position:absolute; top:var(--gap); right:var(--gap); bottom:var(--gap); width:var(--panel-w);
  background:var(--card); border:1px solid var(--border); border-radius:18px; box-shadow:0 18px 44px rgba(0,0,0,.45);
  padding:14px; display:flex; flex-direction:column; gap:12px; overflow:auto; backdrop-filter:blur(6px) saturate(140%)}}

.header{{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}}
.brand{{display:flex;gap:12px;align-items:center}}
.logo{{width:82px;height:82px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;border:1px solid var(--border)}}
.logo img{{width:100%;height:100%;object-fit:contain;display:block}}
.name{{font-weight:900;letter-spacing:.2px}}
.sub{{font-size:.86rem;color:var(--muted)}}
.badge{{justify-self:end;background:rgba(0,227,165,.12);color:var(--primary);border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}}
.hr{{height:1px;background:var(--border);margin:6px 0 10px}}

.block{{border:1px solid var(--border);border-radius:12px;overflow:hidden}}
.block .body{{padding:10px 12px}}
.kval{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.kpi{{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:12px;padding:12px;text-align:center}}
.kpi .label{{color:#b9c6e6;font-size:.9rem}}
.kpi .value{{font-weight:900;font-size:1.6rem}}

.footer{{margin-top:auto;color:#a9b8df;font-size:.85rem;display:flex;justify-content:space-between}}
.badge-info{{display:inline-block;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.06);border:1px solid var(--border);font-weight:700}}
</style>
</head>
<body>
  <div class="frame">

    <!-- Área visual 50/50 -->
    <div class="split-wrap">
      {"".join([
        f'<div class="grid50 composite"><img src="{composite_uri}" alt="composite" style="width:100%;height:100%;object-fit:cover;filter:none"/>',
        f'<div class="tag">{rgb_label}</div>',
        f'<div class="tag" style="left:calc(50% + 10px)">{swir_label}</div>',
        "</div>"
      ]) if composite_uri else
      "".join([
        '<div class="grid50">',
          f'<div class="cell"><img src="{left_uri}" alt="RGB"/><div class="tag">{rgb_label}</div></div>',
          f'<div class="cell"><img src="{right_uri}" alt="SWIR"/><div class="tag">{swir_label}</div></div>',
        '</div>'
      ])
      }
    </div>

    <!-- Painel lateral -->
    <div class="panel">
      <div class="header">
        <div class="brand">
          <div class="logo">{('<img src="'+logo_uri+'" alt="DAP ATLAS"/>') if logo_uri else '<div style="font-weight:900;color:#000">DA</div>'}</div>
          <div>
            <div class="name">Relatório OGMP 2.0 • L5</div>
            <div class="sub">Monitoramento de Emissões de Metano (CH₄)</div>
          </div>
        </div>
        <div class="badge">DAP ATLAS</div>
      </div>
      <div class="hr"></div>

      <div class="block">
        <div class="body">
          <div style="font-weight:800">Unidade: {unidade}</div>
          <div style="color:#b9c6e6;margin-top:2px">Data da Medição: {data_medicao}</div>
          <div style="margin-top:8px"><span class="badge-info">Diferença entre passagens: {diff_min} min</span></div>
        </div>
      </div>

      <div class="kval">
        <div class="kpi">
          <div class="label">Taxa</div>
          <div class="value">{rate_kgph} <span style="font-size:.95rem;color:#cbd6f2;font-weight:700">kg CH₄/h</span></div>
        </div>
        <div class="kpi">
          <div class="label">Incerteza</div>
          <div class="value">{uncert_pct} <span style="font-size:.95rem;color:#cbd6f2;font-weight:700">%</span></div>
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

# importante: definimos APENAS a altura (Streamlit não aceita width no components.html).
# O conteúdo HTML interno tem 1920px de largura e fica centralizado no container.
components.html(html, height=FRAME_H, scrolling=False)

