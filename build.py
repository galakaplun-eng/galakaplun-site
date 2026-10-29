#!/usr/bin/env python3
"""Gala Kaplun portfolio — static site generator.
Run:  python3 build.py   then   cd docs && python3 -m http.server 8000
All content lives in this file; the output goes to docs/ (served by GitHub Pages).
"""
import os, html, urllib.parse, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
YEAR = datetime.date.today().year

PNG = {"33bf54696eea493faf3eb01dd00472f7", "bbafdad86a84426fab20e8d1ac8968c9", "46c5d22be2b64cd3ba4ae2abedeeae7d"}

def img(id_):  # original Wix media ids kept as filenames
    return f"assets/img/9efe7c_{id_}~mv2." + ("png" if id_ in PNG else "jpg")

def exists(rel):
    return os.path.exists(os.path.join(OUT, rel))

# ---- home gallery: (image id, slug, w, h) in the original order / justified layout
HOME_ROWS = [
    [("7e7250bf05674e218b12279cf88d9004", "showreel", 935, 525), ("5b4d0c61dd7b42e2bc5806e1692a9bc2", "lancome", 295, 525)],
    [("8b4cfe52d00c4bb6aba78394e593b972", "bezalel", 499, 561), ("bc12b93fccc44943988b19b494b41945", "taboola", 316, 561), ("18c8e276c76b4648a1ad418038550766", "dear-mom", 405, 561)],
    [("f0583d6adfe54f32a8a722ffe1d87c56", "tokyo", 514, 385), ("7b38afe6e9d645edbe503327128a6629", "hahokrim", 716, 385)],
    [("828419cd11e544eb8113f13e27f882ac", "bein-hakolot", 613, 344), ("6b0d146fcea64b868bd29cb938eb5ce8", "sap-labs", 617, 344)],
    [("523b63cbe2a94eb4baa7e784576d20f7", "solaredge", 878, 493), ("b99d4dca063d4eaaa5fdde991b4d1363", "lelo-tnai", 352, 493)],
    [("a4cef72328ad4a348a6df069546f81ed", "noa-rosin", 807, 520), ("12f848094fef421f9ac2cf626455f1bb", "one-zero", 423, 520)],
    [("0567f46e12c64b83b47f49ce0cb0e254", "kan", 935, 525), ("3bd570676c274aaeb7c7a9a2c7cbefd5", "israel-hofshit", 295, 525)],
]
THUMB = {slug: id_ for row in HOME_ROWS for id_, slug, _, _ in row}
HOME_ORDER = [slug for row in HOME_ROWS for _, slug, _, _ in row]

ABOUT_PHOTO = "eefd9c8965874512809235c79ecbb71c"
EMAIL = "gala.kaplun@gmail.com"

# ---- project pages
# player: ("youtube", id) | ("vimeo", id) | ("facebook", url) | ("file", local mp4 id)
PROJECTS = [
    dict(slug="showreel", title="Showreel", type="Showreel", production=None, director=None, player=("vimeo", "857472011"),
         rows=[[("4b99eb66cbc74d3595bc696509dfd95a", 449, 252), ("f86463913891404eb6588ea78e64d29a", 450, 252)], [("4dca04b30aaa49a4815632ff9a8a1f7f", 914, 503)]]),
    dict(slug="lancome", title="Lancôme", type="Commercial", production="ORRO", director=None,
         player=("facebook", "https://www.facebook.com/647276161/videos/273409427654162/"),
         rows=[[("a60181b895774c2cbaf2627f38d4a081", 293, 522), ("95f6e5067c28481d93b5bcc0a7a950de", 293, 522), ("6cf8ab1e4e494910b35aed2842ff2658", 293, 522)]]),
    dict(slug="bezalel", title="What Bezalel Would Do?", type="Game show", production="Lava", director=None,
         extra_link=("Watch the full show", "https://www.instagram.com/what_theydo.il/"),
         player=("file", "9efe7c_da8d97ec2769431baa5bbd75a9a9e11c"),
         rows=[[("1419712ee1854fb19801e513d843a6fe", 300, 424), ("86e8925a656c45c1a3f038aab00e3997", 599, 424)], [("6add8583072a4ce5b2de925de10cd86f", 599, 424), ("2eef88960f1749878e783d78a3f1a6cf", 300, 424)]]),
    dict(slug="taboola", title="Taboola", type="Commercial", production="Karmi ve Cohen", director=None, player=("file", "9efe7c_4a47774921c44de3ba260be3074f4e61"),
         rows=[[("d532822397a545f3b8499e87006cbdd0", 293, 522), ("63da4a39dd844359a432ef6a3f72af65", 293, 522), ("bc12b93fccc44943988b19b494b41945", 293, 522)]]),
    dict(slug="dear-mom", title="Dear Mom,", type="Short documentary", production="Self production", director="Gala Kaplun, Danna Levy, Maor Alters",
         player=("youtube", "x_nBWRxkS0E"),
         rows=[[("853a30437a8e42dfad79198bf90378f5", 450, 253), ("499af4e97c394ccb8caa602fa4ce7638", 449, 253)], [("dddc0d09d5b84292a83e50b94af80b07", 914, 514)]]),
    dict(slug="tokyo", title="Road to Tokyo", type="Documentary web series", production="KAN", director=None, player=("youtube", "BjTEG6dHcpA"),
         rows=[[("3f547217417f4e889ea4b84c787c25b6", 450, 337), ("622c215623914648835d744eeb36c9de", 449, 337)], [("f0583d6adfe54f32a8a722ffe1d87c56", 450, 337), ("c01bb5ad768d404a83f3f2feb850745b", 449, 337)]]),
    dict(slug="hahokrim", title="The Researchers", type="Web series", production="Studio Pixel", director=None, player=("youtube", "n1If_Okk35U"),
         rows=[[("33bf54696eea493faf3eb01dd00472f7", 450, 337), ("8bee372a46d640a394b816e5de723258", 449, 337)], [("bbafdad86a84426fab20e8d1ac8968c9", 450, 337), ("46c5d22be2b64cd3ba4ae2abedeeae7d", 449, 337)]]),
    dict(slug="bein-hakolot", title="Bein Hakolot", type="Promotional video", production="Bein Hakolot", director=None, player=("youtube", "EU5GUXUDlkU"),
         rows=[[("1c671718d07b4291abe0120391454136", 450, 337), ("64ea10f917de4348a902b41bce152e7a", 449, 337)], [("b72f891244814bc59ec1aa611daaf0d7", 450, 337), ("b883bf7b0be642d9b1c135588059d4d2", 449, 337)]]),
    dict(slug="sap-labs", title="SAP Labs", type="Corporate video", production="SAP Labs", director=None,
         player=("facebook", "https://www.facebook.com/SAPLabsIsrael/videos/7460149127379761"),
         rows=[[("20a05cd959af4f219d7e8d7e6993496e", 449, 253), ("6b0d146fcea64b868bd29cb938eb5ce8", 450, 253)], [("6c16edf692a74dd5ba283953fb64e629", 914, 515)]]),
    dict(slug="solaredge", title="SolarEdge", type="Promotional video", production="Filma", director=None, player=("file", "9efe7c_2c796579e7584ef69420bc914129d7d1"),
         rows=[[("43e1e4022ab245f18e7112d8841ca0f2", 449, 253), ("be050369f533449d98555809581ba2b5", 450, 253)], [("76d4d838e480465ca54582fb1ac2ddd2", 914, 514)]]),
    dict(slug="lelo-tnai", title="On Parole", type="Documentary", production=None, director="Neta Pat Ben-Itzhak", player=("file", "9efe7c_0607e74b8928473d8ab59ba3aa9e9559"),
         rows=[[("67352563b1b34df195e469bbd3269db5", 450, 253), ("cdf7e31c15d646809b322e73e1a34b04", 449, 253)], [("366044758c1f4825b6942b14a2f324c0", 450, 253), ("65867c6ebe064320935df6ceb987cfa2", 449, 253)], [("1bba20d2e2444c1eb351fae232231c65", 450, 253), ("7d5778c413714e31a98d9fec7f60c3e3", 449, 253)]]),
    dict(slug="noa-rosin", title="Noa Rosin", type="Food vlog", production="YAP", director=None, player=("youtube", "qu03wYHzBWs"),
         rows=[[("1df9b24172524879b0b061e77bf1944d", 450, 252), ("7066c624a3384095a69678a741deada7", 449, 252)], [("eff19aa4b0a345008dfc06a9a93b5e76", 914, 513)]]),
    dict(slug="one-zero", title="One Zero Bank", type="Commercial", production="Karmi ve Cohen", director=None,
         player=("facebook", "https://www.facebook.com/ONEZEROBANK/videos/656924923155098/"),
         rows=[[("12f848094fef421f9ac2cf626455f1bb", 450, 553), ("f1695594a95446d7b7ad856adb44ba4f", 451, 553)]]),
    dict(slug="kan", title="KAN", type="Web series", production="KAN", director=None, player=("youtube", "3VB0qQOYjQY"),
         rows=[[("93c9c16196cc4440a74f9b569b9d0eac", 450, 252), ("b631d5a13c6c4970aa55d8d4e1a87119", 449, 252)], [("0567f46e12c64b83b47f49ce0cb0e254", 914, 513)]]),
    dict(slug="israel-hofshit", title="Israel Hofshit", type="Commercial", production="Lava", director=None, player=("youtube", "PVePaV0JME8"),
         rows=[[("044856253e6e4251af906b5e4b2654bd", 300, 424), ("84a3c661acba4e16b0650d036458739f", 599, 424)], [("9d943807a5fa48eea7ac84dfe791b2d2", 599, 424), ("c3212bc8c99e4e1f81be925e953601fc", 300, 424)]]),
    dict(slug="tahrir", title="Tahrir Hotel", type="Short film", production="Tale Runners", director="Yossi Medved", player=("youtube", "BjTEG6dHcpA"),
         rows=[[("e104a6400e794778ba78e6da36aad8e0", 450, 236), ("854ccacb5ec449db9d38a38b20561497", 449, 236)], [("1b481c83554f4d3aa58a7fd2681b250b", 914, 481)]]),
]
BY_SLUG = {p["slug"]: p for p in PROJECTS}
# navigation order = order on the home page, then the two pages not shown there
NAV_ORDER = HOME_ORDER + [p["slug"] for p in PROJECTS if p["slug"] not in HOME_ORDER]

# ------------------------------------------------------------------ CSS
CSS = r"""
:root{--bg:#fff;--ink:#111;--muted:#6f6f6f;--line:#e8e8e8;--accent:#993717;--gap:10px;--radius:10px;--head:72px;
 --font:'Jost','Futura','Helvetica Neue',sans-serif;--ease:cubic-bezier(.2,.7,.2,1)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--font);font-weight:300;-webkit-font-smoothing:antialiased;line-height:1.5}
a{color:inherit;text-decoration:none}img,video{display:block;max-width:100%}
button{font:inherit}
.wrap{width:min(1240px,calc(100% - 48px));margin:0 auto}
.narrow{width:min(960px,calc(100% - 48px));margin:0 auto}
.eyebrow{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:400}
h1,h2,h3{font-weight:300;margin:0;letter-spacing:-.01em}
/* ---------- header */
header.top{position:fixed;top:0;left:0;right:0;height:var(--head);z-index:50;display:flex;align-items:center;transition:background .35s var(--ease),color .35s var(--ease),box-shadow .35s var(--ease);color:#fff}
header.top .wrap{display:flex;align-items:center;justify-content:space-between}
header.top .brand{font-size:22px;font-weight:400;letter-spacing:.02em}
header.top nav{display:flex;gap:34px}
header.top nav a{font-size:15px;letter-spacing:.06em;position:relative;padding:4px 0}
header.top nav a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform .3s var(--ease)}
header.top nav a:hover::after{transform:scaleX(1)}
header.top.solid,body.inner header.top{background:rgba(255,255,255,.86);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);color:var(--ink);box-shadow:0 1px 0 var(--line)}
/* ---------- hero */
.hero{position:relative;height:70vh;min-height:480px;overflow:hidden;background:#111;color:#fff}
.hero video,.hero img.poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero .shade{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.72) 0%,rgba(0,0,0,.25) 45%,rgba(0,0,0,.15) 100%)}
.hero .content{position:absolute;left:0;right:0;bottom:0;padding-bottom:56px}
.hero .content .wrap{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.hero h1{font-size:clamp(52px,8.5vw,118px);line-height:.95;font-weight:300;letter-spacing:-.025em}
.hero .eyebrow{color:rgba(255,255,255,.75);margin-bottom:18px}
.hero .cta{display:inline-flex;align-items:center;gap:10px;font-size:15px;letter-spacing:.06em;border:1px solid rgba(255,255,255,.55);padding:12px 20px;border-radius:999px;transition:background .3s,color .3s}
.hero .cta:hover{background:#fff;color:#111}
.hero .cta svg{width:14px;height:14px}
.hero .scroll{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);width:1px;height:28px;background:rgba(255,255,255,.6);animation:drop 1.8s var(--ease) infinite}
@keyframes drop{0%{transform:translateX(-50%) scaleY(0);transform-origin:top}50%{transform:translateX(-50%) scaleY(1);transform-origin:top}51%{transform-origin:bottom}100%{transform:translateX(-50%) scaleY(0);transform-origin:bottom}}
/* ---------- sections */
section.block{padding:96px 0 0}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:28px;gap:16px}
.sec-head h2{font-size:clamp(30px,3.6vw,44px)}
.sec-head .count{font-size:13px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase}
/* ---------- work grid */
.rows{display:flex;flex-direction:column;gap:var(--gap)}
.row{display:flex;gap:var(--gap)}
.tile{display:block;min-width:0;position:relative;overflow:hidden;border-radius:var(--radius);background:#eee;isolation:isolate}
.tile img,.tile video{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.tile img{transition:transform 1.2s var(--ease),opacity .5s}
.tile video{opacity:0;transition:opacity .5s}
.tile:hover img{transform:scale(1.035)}
.tile.playing video{opacity:1}
.tile .cap{position:absolute;left:0;right:0;bottom:0;padding:22px 22px 18px;color:#fff;background:linear-gradient(to top,rgba(0,0,0,.7),rgba(0,0,0,0));opacity:0;transform:translateY(8px);transition:opacity .4s var(--ease),transform .5s var(--ease)}
.tile:hover .cap,.tile:focus-visible .cap{opacity:1;transform:none}
.tile .cap .t{font-size:20px;font-weight:400;letter-spacing:.01em}
.tile .cap .m{font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.8;margin-top:2px}
@media (hover:none){.tile .cap{opacity:1;transform:none}}
/* ---------- about */
.about{display:grid;grid-template-columns:5fr 7fr;gap:64px;align-items:start}
.about .photo{aspect-ratio:4/5;border-radius:var(--radius);overflow:hidden;background:#eee}
.about .photo img{width:100%;height:100%;object-fit:cover}
.about .quote{font-size:clamp(24px,2.6vw,32px);line-height:1.3;margin:0 0 28px;letter-spacing:-.01em}
.about p{font-size:17px;line-height:1.65;margin:0 0 1.2em;color:#333}
/* ---------- contact */
.contact{text-align:center;padding-bottom:40px}
.contact h2{font-size:clamp(32px,4.4vw,56px);margin-bottom:16px}
.contact .big{display:inline-block;font-size:clamp(20px,2.4vw,28px);border-bottom:1px solid var(--ink);padding-bottom:2px;margin-bottom:48px;transition:color .3s,border-color .3s}
.contact .big:hover{color:var(--accent);border-color:var(--accent)}
form.contact-form{width:min(640px,100%);margin:0 auto;text-align:left}
form.contact-form .grid{display:grid;grid-template-columns:1fr 1fr;gap:26px 32px}
form.contact-form .full{grid-column:1/-1}
form.contact-form label{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;font-weight:400}
form.contact-form input,form.contact-form textarea{width:100%;border:0;border-bottom:1px solid #cfcfcf;padding:8px 0;font:inherit;font-size:17px;background:transparent;outline:none;transition:border-color .3s;border-radius:0}
form.contact-form input:focus,form.contact-form textarea:focus{border-color:var(--ink)}
form.contact-form textarea{min-height:90px;resize:vertical}
form.contact-form .actions{grid-column:1/-1;display:flex;justify-content:flex-end;margin-top:8px}
form.contact-form button{background:var(--ink);color:#fff;border:0;padding:12px 34px;border-radius:999px;font-size:15px;letter-spacing:.06em;cursor:pointer;transition:background .3s}
form.contact-form button:hover{background:var(--accent)}
/* ---------- footer */
footer.site{margin-top:96px;border-top:1px solid var(--line);padding:28px 0 36px;font-size:13px;color:var(--muted);letter-spacing:.04em}
footer.site .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer.site a:hover{color:var(--ink)}
/* ---------- project page */
body.inner main{padding-top:calc(var(--head) + 56px)}
.phead{display:grid;grid-template-columns:7fr 5fr;gap:40px;align-items:end;margin-bottom:36px}
.phead h1{font-size:clamp(40px,6vw,76px);line-height:1;letter-spacing:-.02em;margin-top:14px}
.phead h1 a{border-bottom:1px solid currentColor}
.meta{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;font-size:15px;align-content:end}
.meta dt{color:var(--muted);font-size:12px;letter-spacing:.14em;text-transform:uppercase;padding-top:3px;font-weight:400}
.meta dd{margin:0}
.meta a{border-bottom:1px solid #bbb;transition:border-color .3s}.meta a:hover{border-color:var(--ink)}
.player{width:100%;aspect-ratio:16/9;background:#000;position:relative;border-radius:var(--radius);overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.35)}
.player iframe,.player video{position:absolute;inset:0;width:100%;height:100%;border:0}
.gallery{margin-top:var(--gap)}
.gallery .cell{display:block;min-width:0;position:relative;overflow:hidden;border-radius:var(--radius);cursor:zoom-in;background:#eee;border:0;padding:0}
.gallery .cell img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.gallery .cell:hover img{transform:scale(1.03)}
.pnav{margin-top:96px;border-top:1px solid var(--line);padding-top:40px;display:grid;grid-template-columns:1fr 1fr;gap:24px}
.pnav a{display:flex;gap:18px;align-items:center;padding:12px;border-radius:var(--radius);transition:background .3s}
.pnav a:hover{background:#f5f5f5}
.pnav a.next{flex-direction:row-reverse;text-align:right}
.pnav .th{width:120px;aspect-ratio:3/2;border-radius:6px;overflow:hidden;flex:none;background:#eee}
.pnav .th img{width:100%;height:100%;object-fit:cover}
.pnav .lbl{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.pnav .nm{font-size:20px;font-weight:400}
.all{display:block;text-align:center;margin-top:36px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.all:hover{color:var(--ink)}
/* ---------- lightbox */
.lb{position:fixed;inset:0;background:rgba(10,10,10,.94);display:none;align-items:center;justify-content:center;z-index:100;padding:48px}
.lb.open{display:flex}
.lb img{max-width:100%;max-height:100%;object-fit:contain;border-radius:4px;box-shadow:0 40px 80px rgba(0,0,0,.6)}
.lb button{position:absolute;background:none;border:0;color:#fff;cursor:pointer;opacity:.75;transition:opacity .2s;padding:14px}
.lb button:hover{opacity:1}
.lb .x{top:14px;right:14px;font-size:30px;line-height:1}
.lb .prev,.lb .next{top:50%;transform:translateY(-50%);font-size:36px}
.lb .prev{left:10px}.lb .next{right:10px}
/* ---------- reveal on scroll */
.reveal{opacity:0;transform:translateY(18px);transition:opacity .8s var(--ease),transform .9s var(--ease)}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}.hero .scroll{animation:none}}
/* ---------- responsive */
@media (max-width:860px){
 .about{grid-template-columns:1fr;gap:32px}.about .photo{max-width:420px}
 .phead{grid-template-columns:1fr;gap:20px}
 .pnav{grid-template-columns:1fr}.pnav a.next{flex-direction:row;text-align:left}
}
@media (max-width:700px){
 :root{--head:60px}
 .wrap,.narrow{width:calc(100% - 32px)}
 header.top nav{gap:20px}header.top nav a{font-size:13px}header.top .brand{font-size:18px}
 .hero{height:78vh}.hero .content{padding-bottom:44px}
 .row{flex-direction:column}.row .tile,.row .cell{aspect-ratio:auto!important;flex:none!important}
 .row .tile img,.row .tile video,.gallery .cell img{position:static;height:auto}
 .tile .cap{padding:16px}
 section.block{padding-top:64px}
 form.contact-form .grid{grid-template-columns:1fr}
 .lb{padding:16px}.lb .prev,.lb .next{display:none}
}
"""

# ------------------------------------------------------------------ JS
JS = r"""
(function(){
  // header: transparent over the hero, solid after
  var hd=document.querySelector('header.top'), hero=document.querySelector('.hero');
  function onScroll(){ if(!hero){return;} hd.classList.toggle('solid', window.scrollY > hero.offsetHeight - hd.offsetHeight); }
  onScroll(); addEventListener('scroll', onScroll, {passive:true});

  // hover previews
  var canHover = matchMedia('(hover:hover)').matches;
  document.querySelectorAll('.tile').forEach(function(t){
    var v=t.querySelector('video'); if(!v||!canHover) return;
    t.addEventListener('mouseenter', function(){
      if(!v.getAttribute('src')){ v.setAttribute('src', v.dataset.src); v.load(); }
      var p=v.play(); if(p&&p.then){ p.then(function(){ t.classList.add('playing'); }).catch(function(){}); } else { t.classList.add('playing'); }
    });
    t.addEventListener('mouseleave', function(){ t.classList.remove('playing'); v.pause(); try{ v.currentTime=0; }catch(e){} });
  });

  // reveal on scroll
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }); },{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });
  } else { document.querySelectorAll('.reveal').forEach(function(el){ el.classList.add('in'); }); }

  // lightbox
  var cells=[].slice.call(document.querySelectorAll('.gallery .cell'));
  if(cells.length){
    var lb=document.createElement('div'); lb.className='lb';
    lb.innerHTML='<button class="x" aria-label="Close">×</button><button class="prev" aria-label="Previous">‹</button><img alt=""><button class="next" aria-label="Next">›</button>';
    document.body.appendChild(lb);
    var im=lb.querySelector('img'), i=0;
    function show(n){ i=(n+cells.length)%cells.length; im.src=cells[i].dataset.full; lb.classList.add('open'); document.body.style.overflow='hidden'; }
    function hide(){ lb.classList.remove('open'); document.body.style.overflow=''; }
    cells.forEach(function(c,n){ c.addEventListener('click', function(){ show(n); }); });
    lb.querySelector('.x').onclick=hide; lb.querySelector('.prev').onclick=function(e){e.stopPropagation();show(i-1);} ; lb.querySelector('.next').onclick=function(e){e.stopPropagation();show(i+1);};
    lb.addEventListener('click', function(e){ if(e.target===lb||e.target===im) hide(); });
    addEventListener('keydown', function(e){ if(!lb.classList.contains('open')) return; if(e.key==='Escape') hide(); if(e.key==='ArrowRight') show(i+1); if(e.key==='ArrowLeft') show(i-1); });
  }

  // contact form -> mail client
  var f=document.querySelector('form.contact-form');
  if(f){ f.addEventListener('submit', function(e){
    e.preventDefault();
    var b='Name: '+f.first.value+' '+f.last.value+'\nEmail: '+f.email.value+'\nPhone: '+f.phone.value+'\n\n'+f.message.value;
    location.href='mailto:%EMAIL%?subject='+encodeURIComponent('Website contact from '+f.first.value)+'&body='+encodeURIComponent(b);
  }); }
})();
""".replace("%EMAIL%", EMAIL)

# ------------------------------------------------------------------ templates
def head(title, base, inner):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Gala Kaplun</title>
<meta name="description" content="Gala Kaplun — content creator, video editor and storyteller.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
</head><body class="{'inner' if inner else 'home'}">
<header class="top"><div class="wrap">
  <a class="brand" href="{base}index.html">Gala Kaplun</a>
  <nav><a href="{base}index.html#work">Work</a><a href="{base}index.html#about">About</a><a href="{base}index.html#contact">Contact</a></nav>
</div></header>
"""

def foot(base):
    return f"""<footer class="site"><div class="wrap">
  <span>© {YEAR} Gala Kaplun</span>
  <a href="mailto:{EMAIL}">{EMAIL}</a>
  <a href="#top">Back to top ↑</a>
</div></footer>
<script src="{base}site.js"></script>
</body></html>
"""

def tile(id_, slug, w, h, base):
    p = BY_SLUG[slug]
    meta = p["type"] + (f" · {p['production']}" if p.get("production") else "")
    prev = f"assets/preview/{slug}.mp4"
    video = f'<video muted loop playsinline preload="none" data-src="{base}{prev}" poster="{base}assets/preview/{slug}.jpg"></video>' if exists(prev) else ""
    return (f'<a class="tile reveal" href="{base}{slug}/index.html" style="flex:{w} 1 0;aspect-ratio:{w}/{h}">'
            f'<img src="{base}{img(id_)}" alt="{html.escape(p["title"])}" loading="lazy">{video}'
            f'<div class="cap"><div class="t">{html.escape(p["title"])}</div><div class="m">{html.escape(meta)}</div></div></a>')

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
    hero_video = "assets/video/showreel.mp4"
    poster = "assets/img/showreel-poster.jpg" if exists("assets/img/showreel-poster.jpg") else img("4b99eb66cbc74d3595bc696509dfd95a")
    media = (f'<video autoplay muted loop playsinline poster="{poster}" src="{hero_video}"></video>' if exists(hero_video)
             else f'<img class="poster" src="{poster}" alt="">')
    rows = "".join('<div class="row">' + "".join(tile(*it, base) for it in row) + '</div>' for row in HOME_ROWS)
    count = sum(len(r) for r in HOME_ROWS)
    body = f"""<a id="top"></a>
<section class="hero">
  {media}<div class="shade"></div>
  <div class="content"><div class="wrap">
    <div><div class="eyebrow">Content creator · Video editor · Storyteller</div><h1>Gala Kaplun</h1></div>
    <a class="cta" href="showreel/index.html">Watch the showreel <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
  </div></div>
  <div class="scroll" aria-hidden="true"></div>
</section>

<section class="block" id="work"><div class="wrap">
  <div class="sec-head reveal"><h2>Selected work</h2><span class="count">{count} projects</span></div>
  <div class="rows">{rows}</div>
</div></section>

<section class="block" id="about"><div class="wrap about">
  <div class="photo reveal"><img src="{img(ABOUT_PHOTO)}" alt="Gala Kaplun"></div>
  <div class="reveal">
    <div class="eyebrow" style="margin-bottom:18px">About</div>
    <p class="quote">I believe the most personal stories are also the most universal.</p>
    <p>Hi! I'm Gala, a video editor and storyteller, and a proud graduate of Sapir College's Audio &amp; Visual Arts program with a degree in film studies.</p>
    <p>I’m passionate about storytelling. Every project feels like stepping into a new world, and I thrive on uncovering and shaping visual stories that resonate.</p>
    <p>Staying ahead in a fast-evolving industry, I embrace the latest trends and technologies to create fresh, impactful content. Whether it's crafting an emotional narrative or delivering high-energy visuals, I aim to bring your ideas to life in unforgettable ways.</p>
    <p>Always seeking new challenges and diverse projects, I’d love to connect and create something extraordinary together.</p>
  </div>
</div></section>

<section class="block contact" id="contact"><div class="narrow">
  <div class="eyebrow reveal" style="margin-bottom:14px">Contact</div>
  <h2 class="reveal">Let’s make something together.</h2>
  <a class="big reveal" href="mailto:{EMAIL}">{EMAIL}</a>
  <form class="contact-form reveal">
    <div class="grid">
      <div><label>First name *</label><input name="first" required></div>
      <div><label>Last name</label><input name="last"></div>
      <div class="full"><label>Email *</label><input name="email" type="email" required></div>
      <div class="full"><label>Phone</label><input name="phone" type="tel"></div>
      <div class="full"><label>Message *</label><textarea name="message" required></textarea></div>
      <div class="actions"><button type="submit">Send message</button></div>
    </div>
  </form>
</div></section>
"""
    write("index.html", head("Home", base, False) + body + foot(base))

def build_project(p):
    base = "../"
    slug = p["slug"]
    title = html.escape(p["title"])
    if p.get("title_link"):
        title = f'<a href="{p["title_link"]}" target="_blank" rel="noreferrer noopener">{title}</a>'
    meta = []
    if p.get("production"): meta.append(("Production", html.escape(p["production"])))
    if p.get("director"): meta.append(("Director", html.escape(p["director"])))
    if p.get("extra_link"):
        t, u = p["extra_link"]
        meta.append(("Link", f'<a href="{u}" target="_blank" rel="noreferrer noopener">{html.escape(t)} ↗</a>'))
    meta_html = ('<dl class="meta">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in meta) + "</dl>") if meta else ""
    gallery = "".join('<div class="row">' + "".join(
        f'<button class="cell" type="button" style="flex:{w} 1 0;aspect-ratio:{w}/{h}" data-full="{base}{img(i)}" aria-label="Enlarge image"><img src="{base}{img(i)}" alt="" loading="lazy"></button>'
        for i, w, h in row) + '</div>' for row in p["rows"])
    n = NAV_ORDER.index(slug)
    prv, nxt = BY_SLUG[NAV_ORDER[n - 1]], BY_SLUG[NAV_ORDER[(n + 1) % len(NAV_ORDER)]]
    def card(q, cls, lbl):
        th = THUMB.get(q["slug"]) or q["rows"][0][0][0]
        return (f'<a class="{cls}" href="{base}{q["slug"]}/index.html"><div class="th"><img src="{base}{img(th)}" alt=""></div>'
                f'<div><div class="lbl">{lbl}</div><div class="nm">{html.escape(q["title"])}</div></div></a>')
    body = f"""<a id="top"></a>
<main class="wrap">
  <div class="phead">
    <div><div class="eyebrow">{html.escape(p["type"])}</div><h1>{title}</h1></div>
    {meta_html}
  </div>
  {player_html(*p["player"], base)}
  <div class="rows gallery">{gallery}</div>
  <nav class="pnav">{card(prv, "prev", "Previous")}{card(nxt, "next", "Next")}</nav>
  <a class="all" href="{base}index.html#work">All projects</a>
</main>
"""
    write(f"{slug}/index.html", head(p["title"], base, True) + body + foot(base))

def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write("style.css", CSS)
    write("site.js", JS)
    build_home()
    for p in PROJECTS:
        build_project(p)
    previews = sum(exists(f"assets/preview/{p['slug']}.mp4") for p in PROJECTS)
    print(f"built {1 + len(PROJECTS)} pages into {OUT}; hero video: {exists('assets/video/showreel.mp4')}; previews: {previews}/{len(PROJECTS)}")
