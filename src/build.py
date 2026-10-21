# Arma ciudad-poligono.html a partir de shell.html + los módulos de la versión 1 (respaldo-v1)
import os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
s = open(os.path.join(here, 'shell.html'), encoding='utf-8').read()

# Bloque de ciudad (se inserta una sola vez en shell.html)
A, Bm = '// Cielo degradado + estrellas + planeta', '/* ============ Triciclo + piloto ============ */'
if A in s:
    block = open(os.path.join(here, 'city_block.js'), encoding='utf-8').read()
    s = s[:s.index(A)] + block + s[s.index(Bm):]
    s = s.replace("B.forEach(b=>{const s=label(b.name,b.sub,hex(b.color));s.position.set(0,b.id==='academia'?30:46,6);b.group.add(s)});",
                  "B.forEach(b=>{const s=groundSign(b.name,b.sub,b.ui);s.position.set(0,.16,30);b.group.add(s)});")
    s = s.replace("x.fillStyle='#56A8FF';x.fillText('U',st,190);x.fillStyle='#ffffff';x.fillText('ISRAEL',st+w1,190);",
                  "x.fillStyle='#0076D6';x.fillText('U',st,190);x.fillStyle='#3F4B6E';x.fillText('ISRAEL',st+w1,190);")
    s = s.replace("x.font='700 44px Montserrat, Arial';x.fillStyle='#F7C948';", "x.font='700 44px Montserrat, Arial';x.fillStyle='#3F4B6E';")
    s = s.replace("P.style.setProperty('--c',hex(nb.color))", "P.style.setProperty('--c',nb.ui)")
    s = s.replace("I.style.setProperty('--c',hex(b.color))", "I.style.setProperty('--c',b.ui)")
    open(os.path.join(here, 'shell.html'), 'w', encoding='utf-8').write(s)

v1 = open(os.path.join(root, 'respaldo-v1', 'modelado-poligonal-maya.html'), encoding='utf-8').read()
css = v1[v1.index('<style>'):v1.index('</style>') + 8]
main = v1[v1.index('<main>') + 6:v1.index('</main>')]
js = v1[v1.rindex('<script>'):v1.rindex('</script>') + 9]
js = js[:js.index('/* ================= Fondo del héroe')] + '</script>'
js = js.replace("const r=$('vpPlay').getBoundingClientRect();", "if(!$('vpPlay').offsetParent)return;const r=$('vpPlay').getBoundingClientRect();")
js = js.replace('Pruébalo en el Taller (Módulo 2)', 'Pruébalo en el Taller de este edificio').replace('Repasa el Módulo 4 y vuelve', 'Visita el edificio Topología y vuelve')
for a, b in [('Módulo 1 · Anatomía de una malla', 'Edificio Componentes · Anatomía de una malla'), ('Módulo 2 · Taller práctico', 'Edificio Herramientas · Taller práctico'),
             ('Módulo 3 · Modeling Toolkit', 'Edificio Herramientas · Modeling Toolkit'), ('Módulo 4 · Topología', 'Edificio Topología'), ('Módulo 5 · Autoevaluación', 'Edificio Academia · Autoevaluación')]:
    main = main.replace(a, b)
out = s.replace('<!--V1CSS-->', css).replace('<!--V1SECTIONS-->', main).replace('<!--V1JS-->', js)
import base64
img = os.path.join(here, 'assets', 'portada.jpg')
if os.path.exists(img):
    out = out.replace('{{PORTADA}}', 'data:image/jpeg;base64,' + base64.b64encode(open(img, 'rb').read()).decode())
open(os.path.join(root, 'ciudad-poligono.html'), 'w', encoding='utf-8').write(out)
print('ok', len(out), 'glass(' in out, 'withEdges(' in out, 'label(' in out)
