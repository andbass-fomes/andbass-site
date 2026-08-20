# -*- coding: utf-8 -*-
"""Generatore statico andbass.com — rigenera tutte le pagine HTML.
Uso: python3 _build.py (dalla cartella SITO/)
Struttura: Images (Visualization /render + AI Explorations) · Craft · 3D · About"""
import os, json, pathlib

ROOT = pathlib.Path(__file__).parent
WIRE = json.load(open(ROOT / "_models_wire.json"))  # modello -> indice immagine wireframe
EMAIL = "andreabassetti@live.com"
SKY = "https://3dsky.org/users/andreabassetti"

# ---------------- DATI ----------------
# (slug, folder, titolo, anno, blurb)
AI_ARCH = [
    ("futuristic-interiors", "Futuristic-Interiors", "Futuristic Interiors", 2023,
     "Neon-lit caves and light-drawn thresholds — interiors from a soft sci-fi."),
    ("wabi-sabi-interiors", "Wabi-Sabi-Interiors", "Wabi-Sabi Interiors", 2023,
     "Raw plaster, stone and timber — quiet rooms that age with grace."),
    ("modern-interiors", "Modern-Interiors", "Modern Interiors", 2023,
     "Grand arches, terrazzo and stone — an Italian palazzo language, revisited."),
    ("cave-architectures", "Cave-Architectures", "Cave Architectures", 2023,
     "Carved voids, oculi and still water — architecture as excavation."),
    ("classic-yacht-living", "Classic-Yacht-Living", "Classic Yacht — Living", 2023,
     "Dark timber salons and open-sea lounges aboard a classic motoryacht."),
    ("classic-yacht-bedroom", "Classic-Yacht-Bedroom", "Classic Yacht — Bedroom", 2023,
     "Cabins in red lacquer and white linen, portholes on a moving horizon."),
    ("worm-apartment", "Worm-Apartment", "Worm Apartment", 2023,
     "Boucle, brass and warm light in a soft Parisian apartment."),
    ("vintage-spaceship", "Vintage-Spaceship", "Vintage Spaceship", 2023,
     "Chrome domes and red leather — a retro-futurist cruiser above the clouds."),
    ("after-yovanovitch", "After-Yovanovitch", "After Yovanovitch", 2023,
     "An interior study after Pierre Yovanovitch's Parisian language."),
    ("tropical-villa", "Tropical-Villa", "Tropical Villa", 2023,
     "Pink towers and arches over turquoise coves."),
    ("overgrown-architectures", "Overgrown-Architectures", "Overgrown Architectures", 2023,
     "Buildings losing gracefully to vegetation and weather."),
    ("parasite-architecture", "Parasite-Architecture", "Parasite Architecture", 2024,
     "Biomorphic shells latching onto landscapes and streets."),
    ("biomorphic-house", "Biomorphic-House", "Biomorphic House", 2024,
     "Voronoi skins and translucent volumes — houses grown, not built."),
    ("parametric-pods", "Parametric-Pods", "Parametric Pods", 2024,
     "Cinematic pods and pavilions in empty landscapes."),
]
AI_PHOTO = [
    ("beast-bw", "Beast-BW", "Beast (B/W)", 2023,
     "Monochrome busts of imagined creatures — sculpture studies in light."),
    ("underwater", "Underwater", "Underwater", 2023,
     "Fish, flowers and falling light — still lifes below the surface."),
    ("dump-rituals", "Dump-Rituals", "Dump Rituals", 2024,
     "Night ceremonies at the edge of the landfill."),
    ("toiletpaper-reinvented", "Toiletpaper-Reinvented", "Toiletpaper, Reinvented", 2023,
     "Pop-surreal tableaux after the magazine's deadpan grammar."),
    ("liminal-spaces", "Liminal-Spaces", "Liminal Spaces", 2023,
     "Rooms that shouldn't exist, lit like memories."),
    ("after-hido-houses", "After-Hido-Houses", "After Hido — Houses", 2023,
     "Nocturnal houses in fog — a study after Todd Hido."),
    ("after-hido-interiors", "After-Hido-Interiors", "After Hido — Interiors", 2023,
     "Sunstruck empty rooms — a study after Todd Hido."),
    ("oh-my-cloud", "Oh-My-Cloud", "Oh, My Cloud", 2023,
     "A single cumulus, impossibly low over modernist suburbia at dusk."),
    ("oh-my-bomb", "Oh-My-Bomb", "Oh, My Bomb", 2023,
     "Detonations blooming over quiet architecture — beauty and dread in one frame."),
    ("on-my-way", "On-My-Way", "On My Way", 2023,
     "Wet, empty streets after dark. American loneliness, made cinematic."),
    ("crash-test", "Crash-Test", "Crash Test", 2024,
     "Wrecks, fire and faceless dummies — staged tableaux of the aftermath."),
    ("the-mask", "The-Mask", "The Mask", 2024,
     "Portrait busts behind sculptural masks: shell, bone, glass and chrome."),
]
AI_ALL = AI_ARCH + AI_PHOTO

# (cartella assets/render, slug, titolo)
R_META = "Modeled, lit and rendered in 3ds Max with Corona / V-Ray — finished in Photoshop."
RENDER = (
    [(f"ID_{i:02d}", f"id-{i:02d}", f"Interior {i:02d}") for i in range(1, 12)]
    + [("YD_01", "yd-01", "Yacht 01"), ("YD_02", "yd-02", "Yacht 02")]
)

def count(sub, folder):
    d = ROOT / "assets" / sub / folder
    return len([f for f in os.listdir(d) if f.endswith(".webp") and not f.endswith("_th.webp")])

def model_title(folder):
    parts = folder.split("_")
    return " · ".join(p.replace("-", " ") for p in parts)

MODELS = sorted(d for d in os.listdir(ROOT / "assets" / "models")
                if (ROOT / "assets" / "models" / d).is_dir())

# ---------------- TEMPLATE ----------------
def page(rel, title, desc, body, active=""):
    nav_items = [("Craft", "craft/"), ("3D", "3d/"), ("Images", "images/"), ("About", "about/")]
    links = "\n".join(
        f'      <a href="{rel}{href}" class="{"active" if active == label else ""}">\\{label}</a>'
        for label, href in nav_items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://andbass.com/assets/img/cover_og.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="{rel}assets/img/favicon.svg">
<link rel="stylesheet" href="{rel}assets/css/style.css">
</head>
<body>
<header class="nav">
  <a class="wordmark" href="{rel}index.html">A<span class="wm-slash">//</span>B</a>
  <nav class="nav-links">
      <span class="nav-plus">+</span>
{links}
  </nav>
  <div class="nav-side">ANDREA BASSETTI — ANDBASS</div>
</header>
<main>
{body}
</main>
<footer class="footer">
  <div>© 2026 Andrea Bassetti — AndBass</div>
  <div class="muted">AI-assisted series are labeled as such.</div>
  <a href="mailto:{EMAIL}">{EMAIL}</a>
</footer>
<div class="cursor" id="cursor" aria-hidden="true"></div>
<div class="lightbox" id="lightbox" aria-hidden="true">
  <button class="lb-close" aria-label="Close">×</button>
  <button class="lb-prev" aria-label="Previous">←</button>
  <img alt="">
  <button class="lb-next" aria-label="Next">→</button>
  <div class="lb-count"></div>
</div>
<script src="{rel}assets/js/main.js"></script>
</body>
</html>"""

# ---------------- HOME ----------------
# Carosello: una card per ogni progetto di Images (render + AI)
DECK_ITEMS = (
    [(f"render/{slug}/", f"assets/render/{folder}/{folder}_01_th.webp", title)
     for folder, slug, title in RENDER]
    + [(f"images/{slug}/", f"assets/gallery/{folder}/{folder}_01_th.webp", title)
       for slug, folder, title, year, blurb in AI_ALL]
)

def _strip_item(item):
    href, src, title = item
    return (f'      <a class="strip-item" href="{href}" aria-label="{title}" tabindex="-1">'
            f'<img src="{src}" alt="{title} — preview" loading="lazy"></a>')

_half = (len(DECK_ITEMS) + 1) // 2
strip_left = "\n".join(_strip_item(it) for it in DECK_ITEMS[:_half])
strip_right = "\n".join(_strip_item(it) for it in DECK_ITEMS[_half:])

home_body = f"""
<section class="hero">
  <div class="hero-meta">
    <span>ANDREA BASSETTI</span>
    <span>(AND//BASS® — 26)</span>
    <span>DESIGNER</span>
  </div>
  <div class="hero-deck reveal" id="deck">
    <div class="strip" id="strip">
{strip_left}
      <a class="deck-card" href="about/" id="deckMain" aria-label="About Andrea Bassetti">
        <img class="deck-img deck-main" src="assets/img/cover.webp" alt="AndBass — dithered cover artwork">
        <span class="deck-hint muted">About ↗</span>
      </a>
{strip_right}
    </div>
  </div>
  <h1 class="giant" aria-label="Andrea Bassetti">Andrea&nbsp;Bassetti</h1>
</section>

<section class="intro">
  <p class="positioning reveal">A practice between visualization, image and the made&nbsp;object.</p>
</section>

<section class="entries">
  <a class="entry reveal" href="craft/">
    <span class="entry-label muted">TUBOH — in preparation</span>
    <span class="entry-title">Craft</span>
    <span class="entry-arrow">↗</span>
  </a>
  <a class="entry reveal" href="3d/">
    <span class="entry-label muted">{len(MODELS)} product models</span>
    <span class="entry-title">3D</span>
    <span class="entry-arrow">↗</span>
  </a>
  <a class="entry reveal" href="images/">
    <span class="entry-label muted">{len(RENDER)} projects · {len(AI_ALL)} AI series</span>
    <span class="entry-title">Images</span>
    <span class="entry-arrow">↗</span>
  </a>
</section>
"""

# ---------------- IMAGES INDEX ----------------
def ai_tile(s):
    slug, folder, title, year, _ = s
    return f"""  <a class="tile reveal" href="{slug}/">
    <div class="tile-img"><img src="../assets/gallery/{folder}/{folder}_01_th.webp" alt="{title} — cover image" loading="lazy"></div>
    <div class="tile-row"><span class="tile-title">{title}</span><span class="muted">{year}</span></div>
  </a>"""

def render_tile(r, rel="../"):
    folder, slug, title = r
    return f"""  <a class="tile reveal" href="{rel}render/{slug}/">
    <div class="tile-img"><img src="{rel}assets/render/{folder}/{folder}_01_th.webp" alt="{title} — cover image" loading="lazy"></div>
    <div class="tile-row"><span class="tile-title">{title}</span><span class="muted">Render</span></div>
  </a>"""

images_body = f"""
<section class="page-head">
  <h1 class="display">Images</h1>
  <p class="lede muted">Two bodies of work, kept deliberately separate: professional 3D visualization,
  and AI-assisted image series.</p>
</section>
<section class="block-head">
  <h2 class="subhead"><a href="../render/">Visualization ↗</a></h2>
  <p class="muted block-note">{R_META}</p>
</section>
<section class="tiles">
{chr(10).join(render_tile(r) for r in RENDER)}
</section>
<section class="block-head">
  <h2 class="subhead">AI Explorations</h2>
  <p class="muted block-note">Personal research: cinematic digital images made with AI-assisted tools
  and a photographer's eye. Clearly labeled — none of this is client work or rendering.</p>
</section>
<section class="block-head"><h3 class="subhead-sm muted">Architecture &amp; interiors</h3></section>
<section class="tiles">
{chr(10).join(ai_tile(s) for s in AI_ARCH)}
</section>
<section class="block-head"><h3 class="subhead-sm muted">Photographic series</h3></section>
<section class="tiles">
{chr(10).join(ai_tile(s) for s in AI_PHOTO)}
</section>
"""

# ---------------- RENDER (/render: indice a tile + una pagina per progetto) ----------------
render_body = f"""
<section class="page-head">
  <p class="crumb muted"><a href="../images/">Images</a> / Visualization</p>
  <h1 class="display">Visualization</h1>
  <p class="lede muted">Interior and yacht visualization. {R_META}</p>
</section>
<section class="tiles">
{chr(10).join(render_tile(r, rel="../") for r in RENDER)}
</section>
"""

def render_project_body(i):
    folder, slug, title = RENDER[i]
    prev_r = RENDER[(i - 1) % len(RENDER)]
    next_r = RENDER[(i + 1) % len(RENDER)]
    n = count("render", folder)
    figs = "\n".join(
        f"""    <figure class="g-item reveal"><img src="../../assets/render/{folder}/{folder}_{k:02d}_th.webp"
      data-full="../../assets/render/{folder}/{folder}_{k:02d}.webp"
      alt="{title} — view {k:02d} of {n}" loading="lazy"></figure>"""
        for k in range(1, n + 1))
    return f"""
<section class="page-head">
  <p class="crumb muted"><a href="../">Visualization</a></p>
  <h1 class="display">{title}</h1>
  <p class="lede muted"><em>{R_META}</em></p>
</section>
<section class="gallery" id="gallery">
{figs}
</section>
<nav class="series-nav">
  <a href="../{prev_r[1]}/"><span class="muted">← Prev</span><br>{prev_r[2]}</a>
  <a class="right" href="../{next_r[1]}/"><span class="muted">Next →</span><br>{next_r[2]}</a>
</nav>
"""

# ---------------- AI SERIES PAGES ----------------
def series_body(i):
    slug, folder, title, year, blurb = AI_ALL[i]
    prev_s = AI_ALL[(i - 1) % len(AI_ALL)]
    next_s = AI_ALL[(i + 1) % len(AI_ALL)]
    n = count("gallery", folder)
    figs = "\n".join(
        f"""    <figure class="g-item reveal"><img src="../../assets/gallery/{folder}/{folder}_{k:02d}_th.webp"
      data-full="../../assets/gallery/{folder}/{folder}_{k:02d}.webp"
      alt="{title} — image {k:02d} of {n}" loading="lazy"></figure>"""
        for k in range(1, n + 1))
    return f"""
<section class="page-head">
  <p class="crumb muted"><a href="../">Images</a> / AI Explorations / {year}</p>
  <h1 class="display">{title}</h1>
  <p class="lede muted"><em>{blurb}</em></p>
  <p class="muted block-note">AI-assisted image series — personal research, not rendering work.</p>
</section>
<section class="gallery" id="gallery">
{figs}
</section>
<nav class="series-nav">
  <a href="../{prev_s[0]}/"><span class="muted">← Prev</span><br>{prev_s[2]}</a>
  <a class="right" href="../{next_s[0]}/"><span class="muted">Next →</span><br>{next_s[2]}</a>
</nav>
"""

# ---------------- 3D PAGE ----------------
def model_figs(m):
    n = count("models", m)
    title = model_title(m)
    w = WIRE.get(m)
    out = [f"""    <figure class="g-item reveal" data-group="{m}"><img src="../assets/models/{m}/{m}_01_th.webp"
      data-full="../assets/models/{m}/{m}_01.webp" alt="{title}" loading="lazy">
      <figcaption class="cap muted">{title}</figcaption></figure>"""]
    for k in range(2, n + 1):
        lab = " — wireframe" if k == w else f" — view {k}"
        out.append(f"""    <figure class="g-item g-hide" data-group="{m}"><img data-full="../assets/models/{m}/{m}_{k:02d}.webp"
      src="../assets/models/{m}/{m}_{k:02d}_th.webp" alt="{title}{lab}" loading="lazy"></figure>""")
    return "\n".join(out)

three_d_body = f"""
<section class="page-head">
  <h1 class="display">3D Models</h1>
  <p class="lede muted">Furniture and product modeling: {len(MODELS)} models built for visualization work —
  clean topology, real proportions, render-ready shaders. Beauty shot and wireframe for each;
  click through for all views.</p>
  <p class="cta"><a href="{SKY}" target="_blank" rel="noopener">Profile on 3dsky ↗</a></p>
</section>
<section class="gallery models" id="gallery">
{chr(10).join(model_figs(m) for m in MODELS)}
</section>
"""

# ---------------- CRAFT ----------------
craft_body = """
<section class="page-head">
  <h1 class="display">Craft</h1>
  <p class="lede">The core of this practice is physical: product, material research, the move from drawing to produced object.</p>
  <p class="muted">TUBOH and selected physical work — told through process: sketches, Rhino models, materials
  (MJF PA12, glass, O-rings), prototypes and packaging — will live here.
  Art objects, case studies and prototypes will join as the work is produced.</p>
  <p class="cta"><a href="../3d/">Meanwhile, see the 3D models ↗</a></p>
</section>
"""

# ---------------- ABOUT ----------------
about_body = f"""
<section class="page-head">
  <h1 class="display">Andrea Bassetti</h1>
  <p class="lede muted"><em>Architecture-trained designer with a background in 3D visualization,
  moving toward material-driven object design — from concept to produced object.</em></p>
</section>
<section class="about">
  <div class="bio">
    <p>I'm a designer trained in architecture, with a working background in high-end 3D visualization,
    photography and image-making. Over the years that eye for light, material and composition has pulled
    me toward the object itself.</p>
    <p>I co-founded FOMES, where I took a product — TUBOH — from concept to a produced object.
    That's the direction I'm building toward: material-driven, craft-minded product design, with different
    digital media as the method rather than the identity.</p>
    <p>Based in Italy. Working internationally.</p>
    <p class="cta"><a href="../assets/CV_Andrea-Bassetti.pdf" download>Download CV (PDF) ↓</a></p>
  </div>
  <aside class="contact">
    <dl>
      <dt class="muted">Mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt class="muted">Phone</dt><dd><a href="tel:+393298832274">+39 329 8832274</a></dd>
      <dt class="muted">Web</dt><dd>andbass.com</dd>
      <dt class="muted">3dsky</dt><dd><a href="{SKY}" target="_blank" rel="noopener">3dsky.org/users/andreabassetti</a></dd>
      <dt class="muted">Handle</dt><dd>@andbass</dd>
    </dl>
    <figure class="qr"><img src="../assets/img/qr.svg" alt="QR code — andbass.com"><figcaption class="muted">Scan for andbass.com</figcaption></figure>
  </aside>
</section>
"""

# work/ → redirect a craft/ (link vecchi)
redirect_work = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=../craft/">
<link rel="canonical" href="../craft/"><title>Craft — Andrea Bassetti</title></head>
<body><p><a href="../craft/">Moved to /craft</a></p></body></html>"""

pages = [
    ("index.html", "", "Andrea Bassetti — AndBass",
     "Architecture-trained designer moving toward material-driven object design — from concept to produced object.",
     home_body, ""),
    ("images/index.html", "../", "Images — Andrea Bassetti",
     "Professional 3D visualization and AI-assisted image series, kept deliberately separate.",
     images_body, "Images"),
    ("render/index.html", "../", "Visualization — Andrea Bassetti",
     "Interior and yacht visualization — 3ds Max, Corona / V-Ray. Actual renders, no generative AI.",
     render_body, "Images"),
    ("3d/index.html", "../", "3D Models — Andrea Bassetti",
     "Furniture and product modeling for visualization: clean topology, real proportions, render-ready shaders.",
     three_d_body, "3D"),
    ("craft/index.html", "../", "Craft — Andrea Bassetti",
     "Product, material research, the move from drawing to produced object. TUBOH in preparation.",
     craft_body, "Craft"),
    ("about/index.html", "../", "About — Andrea Bassetti",
     "Designer trained in architecture, moving toward material-driven, craft-minded product design.",
     about_body, "About"),
]
for i, s in enumerate(AI_ALL):
    pages.append((f"images/{s[0]}/index.html", "../../",
                  f"{s[2]} ({s[3]}) — Andrea Bassetti", s[4], series_body(i), "Images"))
for i, r in enumerate(RENDER):
    pages.append((f"render/{r[1]}/index.html", "../../",
                  f"{r[2]} — Visualization — Andrea Bassetti", R_META,
                  render_project_body(i), "Images"))

for path, rel, title, desc, body, active in pages:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(page(rel, title, desc, body, active), encoding="utf-8")
    print("wrote", path)

(ROOT / "work").mkdir(exist_ok=True)
(ROOT / "work" / "index.html").write_text(redirect_work, encoding="utf-8")
print("wrote work/index.html (redirect)")
