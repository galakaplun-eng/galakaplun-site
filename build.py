#!/usr/bin/env python3
"""Static rebuild of galakaplun.com (Wix) as plain HTML/CSS.
Run:  python3 build.py   then   cd docs && python3 -m http.server 8000
"""
import os, html, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")

def img(id_):  # original Wix media ids kept as filenames
    return f"assets/img/9efe7c_{id_}~mv2." + ("png" if id_ in PNG else "jpg")

PNG = {"33bf54696eea493faf3eb01dd00472f7", "bbafdad86a84426fab20e8d1ac8968c9", "46c5d22be2b64cd3ba4ae2abedeeae7d"}

# ---- home gallery: (image id, slug) in the original order; rows are the original justified layout
HOME_ROWS = [
    [("7e7250bf05674e218b12279cf88d9004", "showreel", 935, 525), ("5b4d0c61dd7b42e2bc5806e1692a9bc2", "lancome", 295, 525)],
    [("8b4cfe52d00c4bb6aba78394e593b972", "bezalel", 499, 561), ("bc12b93fccc44943988b19b494b41945", "taboola", 316, 561), ("18c8e276c76b4648a1ad418038550766", "dear-mom", 405, 561)],
    [("f0583d6adfe54f32a8a722ffe1d87c56", "tokyo", 514, 385), ("7b38afe6e9d645edbe503327128a6629", "hahokrim", 716, 385)],
    [("828419cd11e544eb8113f13e27f882ac", "bein-hakolot", 613, 344), ("6b0d146fcea64b868bd29cb938eb5ce8", "sap-labs", 617, 344)],
    [("523b63cbe2a94eb4baa7e784576d20f7", "solaredge", 878, 493), ("b99d4dca063d4eaaa5fdde991b4d1363", "lelo-tnai", 352, 493)],
    [("a4cef72328ad4a348a6df069546f81ed", "noa-rosin", 807, 520), ("12f848094fef421f9ac2cf626455f1bb", "one-zero", 423, 520)],
    [("0567f46e12c64b83b47f49ce0cb0e254", "kan", 935, 525), ("3bd570676c274aaeb7c7a9a2c7cbefd5", "israel-hofshit", 295, 525)],
]

ABOUT_PHOTO = "eefd9c8965874512809235c79ecbb71c"

# ---- project pages
# player: ("youtube", id) | ("vimeo", id) | ("facebook", url) | ("file", local mp4 id)
PROJECTS = [
    dict(slug="showreel", title="My Showreel", meta=[], player=("vimeo", "857472011"),
         rows=[[("4b99eb66cbc74d3595bc696509dfd95a", 449, 252), ("f86463913891404eb6588ea78e64d29a", 450, 252)], [("4dca04b30aaa49a4815632ff9a8a1f7f", 914, 503)]]),
    dict(slug="lancome", title="Lancôme", title_link="https://www.caretobeauty.com/il/lancome/", meta=["Commercial", "Production: ORRO"],
         player=("facebook", "https://www.facebook.com/647276161/videos/273409427654162/"),
         rows=[[("a60181b895774c2cbaf2627f38d4a081", 293, 522), ("95f6e5067c28481d93b5bcc0a7a950de", 293, 522), ("6cf8ab1e4e494910b35aed2842ff2658", 293, 522)]]),
    dict(slug="bezalel", title="What Bezalel Would do?", meta=["Game Show", "Production: Lava"], extra_link=("Watch full show >>", "https://www.instagram.com/what_theydo.il/"),
         player=("file", "9efe7c_da8d97ec2769431baa5bbd75a9a9e11c"),
         rows=[[("1419712ee1854fb19801e513d843a6fe", 300, 424), ("86e8925a656c45c1a3f038aab00e3997", 599, 424)], [("6add8583072a4ce5b2de925de10cd86f", 599, 424), ("2eef88960f1749878e783d78a3f1a6cf", 300, 424)]]),
    dict(slug="taboola", title="Taboola", meta=["Commercial", "Production: Karmi ve Cohen"], player=("file", "9efe7c_4a47774921c44de3ba260be3074f4e61"),
         rows=[[("d532822397a545f3b8499e87006cbdd0", 293, 522), ("63da4a39dd844359a432ef6a3f72af65", 293, 522), ("bc12b93fccc44943988b19b494b41945", 293, 522)]]),
    dict(slug="dear-mom", title="Dear mom,", meta=["Short Documentary", "Production: self production", "Director: Gala Kaplun, Danna Levy, Maor Alters"],
         player=("youtube", "x_nBWRxkS0E"),
         rows=[[("853a30437a8e42dfad79198bf90378f5", 450, 253), ("499af4e97c394ccb8caa602fa4ce7638", 449, 253)], [("dddc0d09d5b84292a83e50b94af80b07", 914, 514)]]),
    dict(slug="tokyo", title="Road To Tokyo", meta=["Documentary", "Web Series", "Production: KAN"], player=("youtube", "BjTEG6dHcpA"),
         rows=[[("3f547217417f4e889ea4b84c787c25b6", 450, 337), ("622c215623914648835d744eeb36c9de", 449, 337)], [("f0583d6adfe54f32a8a722ffe1d87c56", 450, 337), ("c01bb5ad768d404a83f3f2feb850745b", 449, 337)]]),
    dict(slug="hahokrim", title="The Researchers", meta=["Web Series", "Production: Studio Pixel"], player=("youtube", "n1If_Okk35U"),
         rows=[[("33bf54696eea493faf3eb01dd00472f7", 450, 337), ("8bee372a46d640a394b816e5de723258", 449, 337)], [("bbafdad86a84426fab20e8d1ac8968c9", 450, 337), ("46c5d22be2b64cd3ba4ae2abedeeae7d", 449, 337)]]),
    dict(slug="bein-hakolot", title="Bein Hakolot", meta=["Promotional video", "Production: Bein Hakolot"], player=("youtube", "EU5GUXUDlkU"),
         rows=[[("1c671718d07b4291abe0120391454136", 450, 337), ("64ea10f917de4348a902b41bce152e7a", 449, 337)], [("b72f891244814bc59ec1aa611daaf0d7", 450, 337), ("b883bf7b0be642d9b1c135588059d4d2", 449, 337)]]),
    dict(slug="sap-labs", title="SAP Labs", meta=["Production: SAP Labs"], player=("facebook", "https://www.facebook.com/SAPLabsIsrael/videos/7460149127379761"),
         rows=[[("20a05cd959af4f219d7e8d7e6993496e", 449, 253), ("6b0d146fcea64b868bd29cb938eb5ce8", 450, 253)], [("6c16edf692a74dd5ba283953fb64e629", 914, 515)]]),
    dict(slug="solaredge", title="Solaredge", meta=["Promotional video", "Production: Filma"], player=("file", "9efe7c_2c796579e7584ef69420bc914129d7d1"),
         rows=[[("43e1e4022ab245f18e7112d8841ca0f2", 449, 253), ("be050369f533449d98555809581ba2b5", 450, 253)], [("76d4d838e480465ca54582fb1ac2ddd2", 914, 514)]]),
    dict(slug="lelo-tnai", title="On Parole", meta=["Documentary", "Director: Neta Pat Ben - Itzhak"], player=("file", "9efe7c_0607e74b8928473d8ab59ba3aa9e9559"),
         rows=[[("67352563b1b34df195e469bbd3269db5", 450, 253), ("cdf7e31c15d646809b322e73e1a34b04", 449, 253)], [("366044758c1f4825b6942b14a2f324c0", 450, 253), ("65867c6ebe064320935df6ceb987cfa2", 449, 253)], [("1bba20d2e2444c1eb351fae232231c65", 450, 253), ("7d5778c413714e31a98d9fec7f60c3e3", 449, 253)]]),
    dict(slug="noa-rosin", title="Noa Rosin", meta=["Food Vlog", "Production: YAP"], player=("youtube", "qu03wYHzBWs"),
         rows=[[("1df9b24172524879b0b061e77bf1944d", 450, 252), ("7066c624a3384095a69678a741deada7", 449, 252)], [("eff19aa4b0a345008dfc06a9a93b5e76", 914, 513)]]),
    dict(slug="one-zero", title="One-Zero Bank", meta=["Commercial", "Production: Karmi ve Cohen"], player=("facebook", "https://www.facebook.com/ONEZEROBANK/videos/656924923155098/"),
         rows=[[("12f848094fef421f9ac2cf626455f1bb", 450, 553), ("f1695594a95446d7b7ad856adb44ba4f", 451, 553)]]),
    dict(slug="kan", title="KAN", meta=["Web series", "Production: KAN"], player=("youtube", "3VB0qQOYjQY"),
         rows=[[("93c9c16196cc4440a74f9b569b9d0eac", 450, 252), ("b631d5a13c6c4970aa55d8d4e1a87119", 449, 252)], [("0567f46e12c64b83b47f49ce0cb0e254", 914, 513)]]),
    dict(slug="israel-hofshit", title="Israel Hofshit", meta=["Commercial", "Production: Lava"], player=("youtube", "PVePaV0JME8"),
         rows=[[("044856253e6e4251af906b5e4b2654bd", 300, 424), ("84a3c661acba4e16b0650d036458739f", 599, 424)], [("9d943807a5fa48eea7ac84dfe791b2d2", 599, 424), ("c3212bc8c99e4e1f81be925e953601fc", 300, 424)]]),
    dict(slug="tahrir", title="Tahrir Hotel", meta=["Short Film", "Production: Tale Runners", "Director: Yossi Medved"], player=("youtube", "BjTEG6dHcpA"),
         rows=[[("e104a6400e794778ba78e6da36aad8e0", 450, 236), ("854ccacb5ec449db9d38a38b20561497", 449, 236)], [("1b481c83554f4d3aa58a7fd2681b250b", 914, 481)]]),
]

CSS = r"""
:root{--bg:#fff;--ink:#000;--muted:#404040;--brick:#993717;--gap:10px;--font-futura:'Jost','Futura',sans-serif;--font-din:'Barlow Condensed','DIN Condensed',sans-serif}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--font-futura);font-weight:300;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%}
.wrap{width:min(980px,calc(100% - 32px));margin:0 auto}
.gallery-wrap{width:min(1240px,calc(100% - 32px));margin:0 auto}
header.site{padding:34px 16px 0;text-align:center}
header.site .name{font-size:50px;line-height:1.1;font-weight:300;margin:0}
header.site .tag{font-size:20px;margin:6px 0 0;font-weight:300}
nav.main{display:flex;justify-content:center;margin-top:22px}
nav.main a{width:327px;height:55px;line-height:55px;font-size:22px;text-align:center;color:#212121;border-left:1px solid #000}
nav.main a:first-child{border-left:0}nav.main a:hover{color:#777}
h2.section{font-size:40px;font-weight:300;text-align:center;margin:30px 0 24px}
.rows{display:flex;flex-direction:column;gap:var(--gap)}
.row{display:flex;gap:var(--gap)}
.row a,.row .cell{display:block;min-width:0;position:relative;overflow:hidden}
.row img{width:100%;height:100%;object-fit:cover}
.row a:hover img{opacity:.92}
/* about */
#about{padding:70px 0 20px}
.about{display:grid;grid-template-columns:327px 1fr;gap:66px;align-items:center;width:min(980px,calc(100% - 32px));margin:0 auto}
.about .photo{width:327px;height:327px;border-radius:50%;object-fit:cover}
.about p{font-size:20px;line-height:1.4;margin:0 0 1.4em;font-weight:300}
/* contact */
#contact{padding:70px 0 80px;text-align:center}
form.contact{width:min(660px,calc(100% - 32px));margin:0 auto;text-align:left;font-family:var(--font-futura)}
form.contact .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px 24px}
form.contact .full{grid-column:1/-1}
form.contact label{display:block;font-size:14px;margin-bottom:6px;font-weight:400}
form.contact input,form.contact textarea{width:100%;border:1px solid #000;border-radius:0;padding:8px 10px;font:inherit;font-size:15px;background:#fff}
form.contact textarea{min-height:84px;resize:vertical}
form.contact .actions{grid-column:1/-1;display:flex;justify-content:flex-end;margin-top:12px}
form.contact button{background:#000;color:#fff;border:0;padding:8px 48px;font:inherit;font-size:15px;cursor:pointer}
form.contact button:hover{background:#333}
.email{font-size:16px;margin-top:38px}
footer.site{background:var(--brick);color:#fff;text-align:center;font-size:14px;padding:16px 0;margin-top:60px}
/* project page */
.project{padding-top:30px}
.project h1{font-family:var(--font-din);font-weight:600;font-size:50px;line-height:1.1;margin:0 0 20px;letter-spacing:.01em}
.project h1 a{text-decoration:underline}
.project .meta{font-size:16px;line-height:1.7;font-weight:400;margin:0}
.project .meta a{color:#555}
.player{width:100%;aspect-ratio:16/9;background:#000;margin:40px 0 40px;position:relative}
.player iframe,.player video{position:absolute;inset:0;width:100%;height:100%;border:0}
.back{display:flex;justify-content:center;margin:60px 0 0}
.back a{font-size:14px;font-weight:400;padding:6px 14px}
.back a:hover{text-decoration:underline}
@media (max-width:760px){
 header.site .name{font-size:38px}nav.main a{width:33%;font-size:18px}
 .row{flex-direction:column}.row a,.row .cell{aspect-ratio:auto!important;flex:none!important}.row img{height:auto}
 .about{grid-template-columns:1fr;gap:30px;justify-items:center;text-align:left}
 form.contact .grid{grid-template-columns:1fr}
 .project h1{font-size:38px}
}
"""

HEAD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Gala Kaplun</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400&family=Barlow+Condensed:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
</head><body>
<header class="site">
  <p class="name"><a href="{base}index.html">Gala Kaplun</a></p>
  <p class="tag"><a href="{base}index.html">Content creator, Video editor &amp; Storyteller</a></p>
  <nav class="main"><a href="{base}index.html#projects">projects.</a><a href="{base}index.html#about">about.</a><a href="{base}index.html#contact">contact.</a></nav>
</header>
"""
FOOT = """<footer class="site">© Gala Kaplun</footer>
</body></html>
"""

def rows_html(rows, base, link=True):
    out = ['<div class="rows">']
    for row in rows:
        out.append('<div class="row">')
        for item in row:
            if link:
                id_, slug, w, h = item
                out.append(f'<a href="{base}{slug}/index.html" style="flex:{w} 1 0;aspect-ratio:{w}/{h}"><img src="{base}{img(id_)}" alt="{html.escape(slug)}" loading="lazy"></a>')
            else:
                id_, w, h = item
                out.append(f'<div class="cell" style="flex:{w} 1 0;aspect-ratio:{w}/{h}"><img src="{base}{img(id_)}" alt="" loading="lazy"></div>')
        out.append('</div>')
    out.append('</div>')
    return "\n".join(out)

def player_html(kind, val, base):
    if kind == "youtube":
        return f'<div class="player"><iframe src="https://www.youtube.com/embed/{val}?rel=0" title="video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>'
    if kind == "vimeo":
        return f'<div class="player"><iframe src="https://player.vimeo.com/video/{val}?title=0&byline=0&portrait=0" title="video" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
    if kind == "facebook":
        q = urllib.parse.quote(val, safe="")
        return f'<div class="player"><iframe src="https://www.facebook.com/plugins/video.php?href={q}&show_text=false&width=914" title="video" scrolling="no" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share; fullscreen" allowfullscreen></iframe></div>'
    if kind == "file":
        return f'<div class="player"><video controls playsinline preload="metadata" src="{base}assets/video/{val}.mp4"></video></div>'
    raise ValueError(kind)

def build_home():
    base = ""
    about = """<p>Hi! I'm Gala<br>A video editor and storyteller, proud graduate of Sapir College's Audio &amp; Visual Arts program with a degree in film studies.</p>
<p>I’m passionate about storytelling. Every project feels like stepping into a new world, and I thrive on uncovering and shaping visual stories that resonate. I believe the most personal stories are also the most universal, and this philosophy inspires my work.</p>
<p>Staying ahead in a fast-evolving industry, I embrace the latest trends and technologies to create fresh, impactful content. Whether it's crafting an emotional narrative or delivering high-energy visuals, I aim to bring your ideas to life in unforgettable ways.</p>
<p>Always seeking new challenges and diverse projects, I’d love to connect and create something extraordinary together!</p>"""
    body = f"""
<section id="projects">
  <h2 class="section">projects.</h2>
  <div class="gallery-wrap">{rows_html(HOME_ROWS, base)}</div>
</section>
<section id="about">
  <h2 class="section">about.</h2>
  <div class="about">
    <img class="photo" src="{img(ABOUT_PHOTO)}" alt="Gala Kaplun">
    <div>{about}</div>
  </div>
</section>
<section id="contact">
  <h2 class="section">contact.</h2>
  <form class="contact" onsubmit="return sendMail(this)">
    <div class="grid">
      <div><label>First Name *</label><input name="first" required></div>
      <div><label>Last Name</label><input name="last"></div>
      <div class="full"><label>Email *</label><input name="email" type="email" required></div>
      <div class="full"><label>Phone</label><input name="phone" type="tel"></div>
      <div class="full"><label>Message *</label><textarea name="message" required></textarea></div>
      <div class="actions"><button type="submit">Send</button></div>
    </div>
  </form>
  <p class="email"><a href="mailto:gala.kaplun@gmail.com">gala.kaplun@gmail.com</a></p>
</section>
<script>
function sendMail(f){{
  var b='Name: '+f.first.value+' '+f.last.value+'\\nEmail: '+f.email.value+'\\nPhone: '+f.phone.value+'\\n\\n'+f.message.value;
  location.href='mailto:gala.kaplun@gmail.com?subject='+encodeURIComponent('Website contact from '+f.first.value)+'&body='+encodeURIComponent(b);
  return false;
}}
</script>
"""
    write("index.html", HEAD.format(title="HOME", base=base) + body + FOOT)

def build_project(p):
    base = "../"
    title = html.escape(p["title"])
    if p.get("title_link"):
        title = f'<a href="{p["title_link"]}" target="_blank" rel="noreferrer noopener">{title}</a>'
    meta = "<br>".join(html.escape(m) for m in p["meta"])
    if p.get("extra_link"):
        t, u = p["extra_link"]
        meta += ("<br>" if meta else "") + f'<a href="{u}" target="_blank" rel="noreferrer noopener">{html.escape(t)}</a>'
    body = f"""
<main class="wrap project">
  <h1>{title}</h1>
  <p class="meta">{meta}</p>
  {player_html(*p["player"], base)}
  {rows_html(p["rows"], base, link=False)}
  <div class="back"><a href="{base}index.html#projects">&lt; Back to Projects</a></div>
</main>
"""
    write(f'{p["slug"]}/index.html', HEAD.format(title=p["title"].upper(), base=base) + body + FOOT)

def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write("style.css", CSS)
    build_home()
    for p in PROJECTS:
        build_project(p)
    print(f"built {1 + len(PROJECTS)} pages into {OUT}")
