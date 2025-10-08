# ===== bloco visual injetado =====
if combined_uri:
    combined_block = (
        f"<div class='split-one'>"
        f"<img src='{combined_uri}' alt='split'/>"
        f"<span class='chip left'>RGB: {fmt_dt_iso(rgb_iso).replace('(UTC)','(Hora Local)')}</span>"
        f"<span class='chip right'>SWIR: {fmt_dt_iso(swir_iso).replace('(UTC)','(Hora Local)')}</span>"
        f"</div>"
    )
else:
    # duas imagens — com foco e chips
    left_html = f"""
    <div class='cell'>
        <img src='{left_uri}' alt='Left' style='object-position:{LEFT_FOCUS};'/>
        <span class='chip left'>RGB: {fmt_dt_iso(rgb_iso).replace('(UTC)','(Hora Local)')}</span>
    </div>
    """ if left_uri else "<div class='cell' style='color:#9fb0d4'>left.png</div>"

    right_html = f"""
    <div class='cell'>
        <img src='{right_uri}' alt='Right' style='object-position:{RIGHT_FOCUS};'/>
        <span class='chip right'>SWIR: {fmt_dt_iso(swir_iso).replace('(UTC)','(Hora Local)')}</span>
    </div>
    """ if right_uri else "<div class='cell' style='color:#9fb0d4'>right.png</div>"

    combined_block = f"<div class='split-grid'>{left_html}{right_html}</div>"

