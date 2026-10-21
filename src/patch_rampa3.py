# Rampa sobre el anillo vial (r 56-70), a lo largo del camino circular; el triciclo arranca en el anillo mirando la rampa
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)

rep("// Rampa de salto blanca justo delante de la salida: ocupa celdas de la retícula circular (entre dos radios y dos arcos) y sube hacia afuera",
    "// Rampa de salto blanca sobre el anillo vial: curva como el camino y sube en el sentido de la marcha (hacia ángulos menores)")
rep("const RAMP={r0:27,r1:45,ta:-15*D2R,tb:15*D2R,H:3.6};RAMP.x=0;RAMP.z=36;\nconst rampH=r=>RAMP.H*(r-RAMP.r0)/(RAMP.r1-RAMP.r0);",
    "const RAMP={r0:57,r1:68.5,ta:24*D2R,tb:40*D2R,H:3.6};RAMP.x=Math.sin(32*D2R)*62.5;RAMP.z=Math.cos(32*D2R)*62.5;\nconst rampH=t=>RAMP.H*(RAMP.tb-t)/(RAMP.tb-RAMP.ta);\n// salida: en el anillo, unos metros antes de la rampa, mirando a lo largo del camino\nconst START={t:46*D2R,r:61.5};START.x=Math.sin(START.t)*START.r;START.z=Math.cos(START.t)*START.r;START.h=Math.atan2(-Math.cos(START.t),Math.sin(START.t));")
rep("uv.push([(RAMP.tb-t)/(RAMP.tb-RAMP.ta),(r-RAMP.r0)/(RAMP.r1-RAMP.r0)]);", "uv.push([(RAMP.r1-r)/(RAMP.r1-RAMP.r0),(RAMP.tb-t)/(RAMP.tb-RAMP.ta)]);")
rep("top[i].push(P(r,t,rampH(r)));", "top[i].push(P(r,t,rampH(t)));")
rep("  for(let i=0;i<NR;i++){fSide.push([bot[i][0],bot[i+1][0],top[i+1][0],top[i][0]]);fSide.push([bot[i][NT],top[i][NT],top[i+1][NT],bot[i+1][NT]])}\n  for(let j=0;j<NT;j++)fSide.push([bot[NR][j],top[NR][j],top[NR][j+1],bot[NR][j+1]]);",
    "  for(let j=0;j<NT;j++){fSide.push([bot[0][j],bot[0][j+1],top[0][j+1],top[0][j]]);fSide.push([bot[NR][j],top[NR][j],top[NR][j+1],bot[NR][j+1]])}\n  for(let i=0;i<NR;i++)fSide.push([bot[i][0],top[i][0],top[i+1][0],bot[i+1][0]]);")
rep("{const NR=6,NT=6,", "{const NR=4,NT=8,")
# eslogan en el piso: tres líneas sobre el anillo, después del aterrizaje, alineado con la marcha
rep("""  const fc2=document.createElement('canvas');fc2.width=2048;fc2.height=256;""", """  const fc2=document.createElement('canvas');fc2.width=512;fc2.height=768;""")
rep("""x.clearRect(0,0,2048,256);drawSlogan(x,1024,170,105,'#ffffff',false);""", """x.clearRect(0,0,512,768);drawSlogan(x,256,300,70,'#ffffff',true);""")
rep("""  const fl=new THREE.Mesh(new THREE.PlaneGeometry(34,4.25),""", """  const fl=new THREE.Mesh(new THREE.PlaneGeometry(11,16.5),""")
rep("""  fl.rotation.set(-Math.PI/2,0,Math.PI);fl.position.set(0,.1,49.3);scene.add(fl)}""",
    """  const ft=-4*D2R,fg=new THREE.Group();fl.rotation.x=-Math.PI/2;fg.add(fl);fg.position.set(Math.sin(ft)*62.5,.1,Math.cos(ft)*62.5);fg.rotation.y=Math.atan2(-Math.cos(ft),Math.sin(ft))+Math.PI;scene.add(fg)}""")
rep("function groundH(x,z){const r=Math.hypot(x,z),t=Math.atan2(x,z);if(r>RAMP.r0&&r<RAMP.r1&&t>RAMP.ta&&t<RAMP.tb)return rampH(r);return 0}",
    "function groundH(x,z){const r=Math.hypot(x,z),t=Math.atan2(x,z);if(r>RAMP.r0&&r<RAMP.r1&&t>RAMP.ta&&t<RAMP.tb)return rampH(t);return 0}")
rep("function rampPitch(x,z,h){return Math.atan2(RAMP.H,RAMP.r1-RAMP.r0)*Math.cos(h-Math.atan2(x,z))}",
    "function rampPitch(x,z,h){const t=Math.atan2(x,z),r=Math.hypot(x,z);return Math.atan2(RAMP.H,r*(RAMP.tb-RAMP.ta))*Math.cos(h-Math.atan2(-Math.cos(t),Math.sin(t)))}")
rep("const blocked=(x,z)=>{if(Math.abs(x)<10&&z>4&&z<64)return true;",
    "const blocked=(x,z)=>{const rr=Math.hypot(x,z),tt=Math.atan2(x,z)/D2R;if(rr>50&&rr<75&&tt>-22&&tt<62)return true;")
rep("S.x=0;S.z=24;S.h=S.mh=0;S.y=0;snapCam()", "S.x=START.x;S.z=START.z;S.h=S.mh=START.h;S.y=0;snapCam()")
s = s.replace("La rampa blanca está justo delante de la salida: acelera con <kbd>W</kbd> (y <kbd>Shift</kbd>) para saltar.",
              "Empiezas sobre el anillo vial con la rampa blanca enfrente: acelera con <kbd>W</kbd> (y <kbd>Shift</kbd>), salta y aterriza en el mismo camino circular.")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
