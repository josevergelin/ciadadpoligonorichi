# Integra las salas interiores 3D (hall_block.js) y la infografía del teclado en el juego
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new, cnt=1):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, cnt)

# 1) separar la parte visual del triciclo (ruedas, piernas, propulsor) para reutilizarla dentro de los salones
a = s.index("  front.rotation.y=S.steer*.45;")
b = s.index("  // la pierna sigue el giro del manubrio")
vis = s[a:b]
s = s[:a] + "  trikeVisual(dt,t);\n" + s[b:]
rep("let boostWas=false;\nfunction update(dt,t){", "let boostWas=false;\nfunction trikeVisual(dt,t){\n" + vis + "}\nfunction update(dt,t){")

# 2) bloque de salones antes del bucle
block = open(os.path.join(here, 'hall_block.js'), encoding='utf-8').read()
rep("/* Bucle */", block + "\n/* Bucle */")

# 3) bucle: ciudad o salón
rep("  if(!paused)update(dt,t);animate(dt,t);if(paused){const a=t*.05;cam.position.set(Math.sin(a)*150,70,Math.cos(a)*150);cam.lookAt(0,15,0);sky.position.copy(cam.position)}\n  R.render(scene,cam);drawMini()}",
    "  if(mode==='hall'){if(!paused)updateHall(dt,t);animHall(dt,t);R.render(curHall.sc,cam);drawMiniHall();return}\n  if(!paused)update(dt,t);animate(dt,t);if(paused){const a=t*.05;cam.position.set(Math.sin(a)*150,70,Math.cos(a)*150);cam.lookAt(0,15,0);sky.position.copy(cam.position)}\n  R.render(scene,cam);drawMini()}")

# 4) teclas: E y Esc dentro del salón; E en la puerta entra al salón 3D
rep("  if((e.code==='KeyE'||e.code==='Enter')&&near)openInterior(near)});",
    "  if(mode==='hall'){if(e.code==='KeyE'||e.code==='Enter')hallAction();else if(e.code==='Escape')exitHall();return}\n  if((e.code==='KeyE'||e.code==='Enter')&&near)enterHall(near)});")
rep("q('enterBtn').addEventListener('click',()=>near&&openInterior(near));", "q('enterBtn').addEventListener('click',()=>{if(mode==='hall')hallAction();else if(near)enterHall(near)});")
# viaje rápido: entra directo al salón; los chips del HUD te dejan en la puerta
rep("const b=B.find(x=>x.id===bt.dataset.b);placeAt(b);q('start').hidden=true;paused=false;openInterior(b)});",
    "const b=B.find(x=>x.id===bt.dataset.b);if(mode==='hall')exitHall();placeAt(b);q('start').hidden=true;paused=false;running=true;enterHall(b)});")
rep("const b=B.find(x=>x.id===bt.dataset.b);placeAt(b);q('start').hidden=true;paused=false;canvas.focus()});",
    "const b=B.find(x=>x.id===bt.dataset.b);if(mode==='hall')exitHall();placeAt(b);q('start').hidden=true;paused=false;canvas.focus()});")
# en la ciudad, el botón vuelve a decir Entrar
rep("if(nb){SFX.chime();P.style.setProperty('--c',nb.ui);", "if(nb){SFX.chime();q('enterBtn').innerHTML='Entrar <kbd>E</kbd>';P.style.setProperty('--c',nb.ui);")
# atajos: el reto usa la lista ampliada
i0 = s.index("const HK=[")
i1 = s.index("];", i0) + 2
s = s[:i0] + "const HK=SHORT.map(x=>[x[3],x[2]]);" + s[i1:]
# textos de ayuda
rep("<div><b>ENTRAR</b>Detente sobre el anillo de luz de la puerta y pulsa <kbd>E</kbd>.</div>",
    "<div><b>ENTRAR</b>Detente sobre el anillo de luz de la puerta y pulsa <kbd>E</kbd>: entras a un salón 3D con estaciones animadas. Sobre cada anillo, <kbd>E</kbd> abre la lección; <kbd>Esc</kbd> vuelve a la ciudad.</div>")
rep("<p>En Maya los atajos ahorran horas. Responde 10 rondas: elige el atajo correcto para cada acción. Las rachas suman puntos extra.</p>",
    "<p>En Maya los atajos ahorran horas. Explora la infografía del teclado y luego responde 10 rondas eligiendo el atajo correcto. Las rachas suman puntos extra.</p>")
# infografía en la lección de Atajos
rep('      <div class="hk">',
    '''      <div class="kbinfo" id="kbInfo">
        <div class="kbtabs" id="kbTabs"></div>
        <div class="kbwrap"><canvas id="kbCanvas" width="1400" height="520" aria-label="Teclado con los atajos de Maya resaltados"></canvas></div>
        <div class="helpline" id="kbNow">Elige un atajo de la lista para verlo en el teclado.</div>
        <div class="kblist" id="kbList"></div>
      </div>
      <div class="hk">''')
rep("/* Flujo */", """/* Infografía del teclado */
.kbinfo{display:grid;gap:14px;margin-bottom:28px}
.kbtabs{display:flex;flex-wrap:wrap;gap:6px}
.kbtabs button{font:700 .78rem var(--f-display);border-radius:999px;padding:6px 12px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
.kbtabs button[aria-pressed="true"]{background:var(--c,var(--brand));border-color:var(--c,var(--brand));color:#0b1240}
.kbwrap{overflow-x:auto;border-radius:14px;border:1px solid var(--line);background:#0a1240}
.kbwrap canvas{display:block;width:100%;min-width:640px;height:auto}
.kbinfo #kbNow span{color:var(--muted);font-weight:500}
.kblist{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.kbcat h5{margin:0 0 6px;font:800 .72rem var(--f-display);letter-spacing:.14em;text-transform:uppercase}
.kbcat button{display:flex;gap:10px;align-items:center;width:100%;text-align:left;font:600 .88rem var(--f-body);color:var(--ink);background:transparent;border:1px solid transparent;border-radius:8px;padding:5px 8px;cursor:pointer}
.kbcat button:hover,.kbcat button.on{background:var(--surface-2);border-color:var(--line)}
.kbcat kbd{min-width:7.5em;text-align:center}
/* Flujo */""")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
