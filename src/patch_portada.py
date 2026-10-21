# Portada con la imagen de Ciudad Polígono y un botón EMPEZAR que lleva directo a la ciudad
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

rep("/* Atajos */", r"""/* Portada */
#portada{position:fixed;inset:0;z-index:40;background:#0b1a4a url("{{PORTADA}}") center/cover no-repeat;overflow:hidden}
#portada::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 55%,rgba(4,10,40,.55) 100%),repeating-linear-gradient(100deg,transparent 0 46px,rgba(140,220,255,.06) 46px 48px);
  background-size:auto,300% 100%;animation:streak 2.4s linear infinite}
@keyframes streak{to{background-position:0 0,-300px 0}}
#portada .cta{position:absolute;left:50%;top:47%;transform:translate(-50%,-50%);display:grid;gap:12px;justify-items:center}
#startBtn{position:relative;font:900 italic clamp(1.5rem,4.2vw,2.6rem) var(--f-display);letter-spacing:.14em;color:#fff;cursor:pointer;
  padding:.45em 1.6em .5em;border-radius:999px;border:3px solid #cfe6ff;
  background:linear-gradient(180deg,#5fb2ff 0%,#0076D6 55%,#0a3f9e 100%);
  text-shadow:0 2px 0 #062a6b,0 0 18px rgba(255,255,255,.45);
  box-shadow:0 0 0 4px #0a3f9e,0 0 26px 6px rgba(70,170,255,.8),inset 0 2px 0 rgba(255,255,255,.7),inset 0 -6px 12px rgba(0,30,90,.6);
  animation:ctaPulse 2s ease-in-out infinite}
#startBtn::after{content:"";position:absolute;inset:3px 12% auto;height:40%;border-radius:999px;background:linear-gradient(180deg,rgba(255,255,255,.55),rgba(255,255,255,0));pointer-events:none}
#startBtn:hover{filter:brightness(1.12);transform:scale(1.04)}
#startBtn:focus-visible{outline:4px solid #F7C948;outline-offset:6px}
@keyframes ctaPulse{50%{box-shadow:0 0 0 4px #0a3f9e,0 0 46px 14px rgba(70,170,255,.95),inset 0 2px 0 rgba(255,255,255,.7),inset 0 -6px 12px rgba(0,30,90,.6)}}
#portada .hint{font:700 .82rem var(--f-display);letter-spacing:.12em;color:#fff;text-shadow:0 2px 8px #000;background:rgba(6,16,60,.55);padding:6px 14px;border-radius:999px}
body:has(#portada:not([hidden])) .hudbox,body:has(#portada:not([hidden])) #touch{display:none!important}
@media (prefers-reduced-motion:reduce){#portada::before,#startBtn{animation:none}}
/* Atajos */""")
rep('<div id="warp"></div>', '<div id="portada" role="dialog" aria-label="Ciudad Polígono"><div class="cta"><button id="startBtn">EMPEZAR</button><div class="hint">Conduce con W A S D · Shift turbo · Espacio drift</div></div></div>\n<div id="warp"></div>')
# el juego espera en pausa hasta pulsar EMPEZAR
rep("running=true;paused=false;snapCam();", r"""running=true;paused=true;snapCam();
q('startBtn').addEventListener('click',()=>{SFX.init();SFX.materialize();q('portada').hidden=true;paused=false;last=performance.now();canvas.focus()});
q('startBtn').focus({preventScroll:true});""")
rep("addEventListener('keydown',e=>{", "addEventListener('keydown',e=>{\n  if(!q('portada').hidden){if(e.key==='Enter'||e.code==='Space'){e.preventDefault();q('startBtn').click()}return}")
rep("  if(trans){stepWarp(dt);", "  if(!q('portada').hidden)return;\n  if(trans){stepWarp(dt);")
open(p, 'w', encoding='utf-8').write(s)

# el build incrusta la imagen como data URI
b = os.path.join(here, 'build.py')
bs = open(b, encoding='utf-8').read()
if '{{PORTADA}}' not in bs:
    bs = bs.replace("open(os.path.join(root, 'ciudad-poligono.html'), 'w', encoding='utf-8').write(out)",
        "import base64\nimg = os.path.join(here, 'assets', 'portada.jpg')\nif os.path.exists(img):\n    out = out.replace('{{PORTADA}}', 'data:image/jpeg;base64,' + base64.b64encode(open(img, 'rb').read()).decode())\nopen(os.path.join(root, 'ciudad-poligono.html'), 'w', encoding='utf-8').write(out)")
    open(b, 'w', encoding='utf-8').write(bs)
print('ok')
