# Entradas automáticas: al pisar el anillo de una puerta se entra; dentro, al pisar una estación se abre su lección y al pisar SALIDA se vuelve a la ciudad
import os, re
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# ciudad: tocar el anillo de la puerta = entrar
i = s.index("  if(nb!==near){near=nb;const P=q('prompt');"); j = s.index("\n", i)
s = s[:i] + "  // basta con tocar el anillo de la puerta para entrar (se rearma al salir del anillo)\n  if(nb!==near){near=nb;q('prompt').hidden=true;if(nb&&q('interior').hidden){enterHall(nb);return}}" + s[j:]
# al salir de un salón el triciclo queda sobre el anillo: no debe volver a entrar hasta alejarse
rep("placeAt(curB);S.h=S.mh=curB.angle+Math.PI;snapCam();SFX.exit()}", "placeAt(curB);near=curB;S.h=S.mh=curB.angle+Math.PI;snapCam();SFX.exit()}")
# dentro: se entra parado junto a la salida, así que esta no se activa hasta alejarse
rep("mode='hall';near=null;hallNear=null;q('prompt').hidden=true;", "mode='hall';near=null;hallNear='exit';q('prompt').hidden=true;")
# dentro: tocar una estación abre su lección; tocar SALIDA vuelve a la ciudad; el teclado holográfico avanza
rep("if(nt!==hallNear){hallNear=nt;showHallPrompt()}",
    "if(nt!==hallNear){hallNear=nt;q('prompt').hidden=true;if(nt==='exit'){exitHall();return}if(nt){if(nt.s.holo){showHallPrompt();hallAction()}else{SFX.chime();openLesson(curB,nt.s)}}}")
# textos de ayuda
rep("<span><kbd>E</kbd> entrar</span>", "")
s = s.replace("<span><kbd>E</kbd> lección</span>", "")
s = re.sub(r"<div><b>ENTRAR</b>.*?</div>", "<div><b>ENTRAR</b>Pasa sobre el anillo de luz de una puerta y entras al instante: bajas del triciclo y recorres a pie un salón 3D con estaciones animadas. Pisa el anillo de una estación para abrir su lección y el anillo blanco de SALIDA para volver.</div>", s, count=1, flags=re.S)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
