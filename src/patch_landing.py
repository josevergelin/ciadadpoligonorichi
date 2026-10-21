# Landing tipo cartel de cine: el piloto en su triciclo en plano heroico sobre la ciudad, con títulos y créditos
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

rep("family=Montserrat:ital,", "family=Anton&family=Montserrat:ital,")
rep("/* Atajos */", r"""/* Cartel de cine (landing) */
#landing{position:fixed;inset:0;z-index:30;overflow:hidden;color:#fff;cursor:default;background:transparent}
#landing .grade{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 80% at 50% 45%,transparent 35%,rgba(3,6,30,.85) 100%),
  linear-gradient(180deg,rgba(6,12,60,.7) 0%,rgba(6,12,60,0) 22%,rgba(6,12,60,0) 52%,rgba(4,8,40,.92) 78%,#030620 100%),
  linear-gradient(115deg,rgba(0,118,214,.35),rgba(247,201,72,.18) 60%,rgba(120,60,200,.3))}
#landing .grain{position:absolute;inset:-50%;pointer-events:none;opacity:.16;mix-blend-mode:overlay;animation:grain 1s steps(6) infinite;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
@keyframes grain{0%{transform:translate(0,0)}20%{transform:translate(-3%,2%)}40%{transform:translate(2%,-3%)}60%{transform:translate(-2%,-1%)}80%{transform:translate(3%,3%)}100%{transform:translate(0,0)}}
#landing .poster{position:relative;height:100%;max-width:1100px;margin:0 auto;display:grid;grid-template-rows:auto 1fr auto;
  padding:max(22px,env(safe-area-inset-top,0px)) max(18px,env(safe-area-inset-right,0px)) max(18px,env(safe-area-inset-bottom,0px)) max(18px,env(safe-area-inset-left,0px));text-align:center}
#landing .top{display:grid;gap:6px;justify-items:center}
#landing .studio{font:800 .78rem var(--f-display);letter-spacing:.42em;text-transform:uppercase;color:#F7C948}
#landing .quote{font:italic 600 clamp(.95rem,2vw,1.2rem) var(--f-body);color:#dfe6ff;max-width:46ch;text-shadow:0 2px 12px #000}
#landing .bottom{display:grid;gap:12px;justify-items:center}
#landing .names{font:400 clamp(1rem,2.4vw,1.5rem) 'Anton',Impact,sans-serif;letter-spacing:.32em;color:#fff;text-shadow:0 2px 14px #000}
#landing h1.title{margin:0;font:400 clamp(3.4rem,13vw,10rem)/.86 'Anton',Impact,sans-serif;letter-spacing:.02em;text-transform:uppercase;
  background:linear-gradient(180deg,#fff7d6 0%,#F7C948 45%,#c98a00 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 4px 0 #141B45) drop-shadow(0 0 28px rgba(247,201,72,.45));animation:titleIn 1.4s cubic-bezier(.2,.8,.2,1) both}
#landing h1.title small{display:block;font-size:.34em;letter-spacing:.38em;color:transparent;margin-top:.15em}
@keyframes titleIn{from{opacity:0;transform:scale(1.15);letter-spacing:.2em}to{opacity:1;transform:none}}
#landing .tag{font:800 italic clamp(1rem,2.6vw,1.45rem) var(--f-display);color:#fff;letter-spacing:.06em;text-shadow:0 2px 10px #000}
#landing .tag b{color:#56A8FF}
#landing .play{font:400 clamp(1.1rem,2.6vw,1.5rem) 'Anton',Impact,sans-serif;letter-spacing:.22em;border:0;border-radius:4px;padding:14px 34px;background:#F7C948;color:#141B45;cursor:pointer;
  box-shadow:0 0 0 2px #141B45,0 0 0 4px #F7C948,0 12px 40px rgba(247,201,72,.4);animation:pulse 2.2s ease-in-out infinite}
#landing .play:hover{background:#fff}
@keyframes pulse{50%{box-shadow:0 0 0 2px #141B45,0 0 0 4px #F7C948,0 12px 60px rgba(247,201,72,.75)}}
#landing .credits{font:500 clamp(.52rem,1.15vw,.72rem)/1.45 'Anton',Impact,sans-serif;letter-spacing:.14em;color:#b9c3e8;text-transform:uppercase;max-width:80ch;opacity:.9}
#landing .credits b{font-weight:400;color:#fff;font-size:1.25em}
#landing .rel{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:center;font:400 clamp(.8rem,1.8vw,1.05rem) 'Anton',Impact,sans-serif;letter-spacing:.28em;color:#F7C948}
#landing .rating{border:2px solid #fff;color:#fff;padding:3px 8px;font-size:.75em;letter-spacing:.12em}
#landing .logo{font:800 1.1rem var(--f-display);color:#fff;letter-spacing:-.01em}#landing .logo span{color:#56A8FF}
@media (prefers-reduced-motion:reduce){#landing .grain,#landing h1.title,#landing .play{animation:none}}
/* Atajos */""")

rep('<div class="screen" id="start">', r'''<div id="landing" role="dialog" aria-label="Portada">
  <div class="grade"></div><div class="grain"></div>
  <div class="poster">
    <div class="top">
      <div class="studio">UISRAEL presenta</div>
      <div class="quote">«En una ciudad hecha de polígonos, solo un piloto conoce cada vértice, cada arista y cada cara.»</div>
    </div>
    <div></div>
    <div class="bottom">
      <div class="names">MG. SÁNCHEZ</div>
      <h1 class="title">Ciudad Polígono<small>Modelado en Maya 2027</small></h1>
      <div class="tag">Ningún <b>N-gon</b> quedará en pie.</div>
      <button class="play" id="playBtn">Arrancar el triciclo</button>
      <div class="rel"><span>Ahora en tu navegador</span><span class="rating">APTA PARA TODO MODELADOR</span><span class="logo"><span>U</span>ISRAEL</span></div>
      <div class="credits">Una producción <b>UISRAEL</b> · protagonizada por <b>MG. SÁNCHEZ</b> y su triciclo retro-futurista · diseño de producción <b>Modeling Toolkit</b> · efectos visuales <b>Extrude · Bevel · Insert Edge Loop · Bridge · Multi-Cut</b> · música original <b>Web Audio</b> · topología <b>100 % quads</b> · basada en <b>Autodesk Maya 2027</b> · Emprende · trasciende · Innova</div>
    </div>
  </div>
</div>

<div class="screen" id="start" hidden>''')

# en la portada: plano heroico del triciclo, ruedas girando y cámara que se mueve despacio
rep("  if(!paused)update(dt,t);animate(dt,t);if(paused){const a=t*.05;",
    "  if(!q('landing').hidden){posterShot(dt,t);animate(dt,t);R.render(scene,cam);return}\n  if(!paused)update(dt,t);animate(dt,t);if(paused){const a=t*.05;")
rep("/* Bucle */", r"""/* Portada: plano de cine del piloto en su triciclo */
S.x=START.x;S.z=START.z;S.h=S.mh=START.h;trike.position.set(S.x,0,S.z);trike.rotation.set(0,S.h,0);
const _pv=new THREE.Vector3(),_pl=new THREE.Vector3();
function posterShot(dt,t){S.wf+=dt*9;S.wr+=dt*18;fw.userData.w.rotation.z=S.wf;rws.forEach(w=>w.userData.w.rotation.z=S.wr);thr.scale.set(1,1.7+Math.sin(t*30)*.12,1);thr.material.opacity=.8;
  tail2.rotation.y=Math.sin(t*12)*.3;front.rotation.y=Math.sin(t*.6)*.12;
  const sw=Math.sin(t*.25);trike.updateMatrixWorld();_pv.set(2.6+sw*1.2,.55+Math.sin(t*.4)*.15,4.6);trike.localToWorld(_pv);_pl.set(-.2,1.55,.2);trike.localToWorld(_pl);
  cam.position.copy(_pv);cam.fov=42;cam.updateProjectionMatrix();cam.lookAt(_pl);sky.position.copy(cam.position)}
q('playBtn').addEventListener('click',()=>{SFX.init();SFX.win();q('landing').hidden=true;q('start').hidden=false;cam.fov=62;cam.updateProjectionMatrix()});

/* Bucle */""")
# en la portada el teclado solo sirve para arrancar
rep("addEventListener('keydown',e=>{\n  if(!q('interior').hidden)", "addEventListener('keydown',e=>{\n  if(!q('landing').hidden){if(e.key==='Enter'||e.code==='Space'){e.preventDefault();q('playBtn').click()}return}\n  if(!q('interior').hidden)")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
