# Sin portada: el juego arranca directo en la ciudad. Dentro de los edificios el personaje trota.
import os, re
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def cut(a_mark, b_mark, new=''):
    global s
    a = s.index(a_mark); b = s.index(b_mark, a)
    s = s[:a] + new + s[b:]
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# 1) quitar portada (HTML, CSS, lógica)
cut('<div id="landing"', '<div class="screen" id="start" hidden>')
cut('/* Cartel de cine (landing) */', '/* Atajos */')
rep("  if(!q('landing').hidden){posterShot(dt,t);animate(dt,t);R.render(scene,cam);return}\n", "")
rep("  if(!q('landing').hidden){if(e.key==='Enter'||e.code==='Space'){e.preventDefault();q('playBtn').click()}return}\n", "")
a = s.index("const _pv=new THREE.Vector3(),_pl=new THREE.Vector3();"); b = s.index("/* Bucle */", a)
s = s[:a] + "// arranque directo: el triciclo ya está en el anillo, listo para conducir\nrunning=true;paused=false;snapCam();\n\n" + s[b:]
rep("/* Portada: plano de cine del piloto en su triciclo */", "/* Inicio directo en la ciudad */")
s = s.replace("family=Anton&family=Montserrat:ital,", "family=Montserrat:ital,")

# 2) trote dentro de los edificios (Shift para correr más rápido)
rep("const tv=keys.up?(keys.boost?8.5:4.4):keys.down?-2.6:0;", "const tv=keys.up?(keys.boost?13:8.5):keys.down?-3.5:0;")
rep("S.v+=(tv-S.v)*Math.min(1,dt*(tv===0?7:3.5));", "S.v+=(tv-S.v)*Math.min(1,dt*(tv===0?8:5));")
rep("W.ph+=dt*sp*2.85*(speed<0?-1:1);", "W.ph+=dt*(sp>.05?5+sp*1.6:0)*(speed<0?-1:1);")
rep("const run=Math.max(0,Math.min(1,(sp-5)/3.5)),amp=W.amp", "const run=Math.max(0,Math.min(1,(sp-3)/7)),amp=W.amp")
rep("<span><kbd>W A S D</kbd> caminar y girar</span><span><kbd>Shift</kbd> correr</span>", "<span><kbd>W A S D</kbd> trotar y girar</span><span><kbd>Shift</kbd> correr</span>")
open(p, 'w', encoding='utf-8').write(s)
print('ok', 'landing' in s, 'playBtn' in s, 'posterShot' in s)
