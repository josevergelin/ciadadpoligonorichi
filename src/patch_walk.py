# Dentro de los edificios el personaje camina (sin triciclo) y cada salón tiene su propio ambiente sonoro
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# 1) personaje a pie
rep("/* ============ Estado del juego ============ */", r"""/* ============ Personaje a pie (dentro de los edificios) ============ */
const walker=new THREE.Group();
{const put=(m,x,y,z)=>{m.position.set(x,y,z);walker.add(m);return m};
  put(new THREE.Mesh(new THREE.CylinderGeometry(.27,.25,.3,12),pants),0,1.02,0);
  put(new THREE.Mesh(new THREE.CylinderGeometry(.31,.27,.78,14),jacket),0,1.55,0);
  put(new THREE.Mesh(new THREE.BoxGeometry(.04,.6,.02),scarf.material),0,1.55,.29);
  put(new THREE.Mesh(new THREE.SphereGeometry(.21,16,12),skin),0,2.17,0);
  put(new THREE.Mesh(new THREE.SphereGeometry(.25,16,10,0,Math.PI*2,0,Math.PI*.55),helm.material),0,2.21,0);
  put(new THREE.Mesh(new THREE.BoxGeometry(.38,.09,.07),visor.material),0,2.24,.2);
  const sf=put(new THREE.Mesh(new THREE.TorusGeometry(.21,.07,6,16),scarf.material),0,1.95,0);sf.rotation.x=Math.PI/2;
  const st=put(new THREE.Mesh(new THREE.BoxGeometry(.14,.04,.55),scarf.material),.12,1.92,-.38);
  put(new THREE.Mesh(new THREE.BoxGeometry(.5,.55,.25),new THREE.MeshStandardMaterial({color:0x0076d6,roughness:.5})),0,1.6,-.36);
  put(new THREE.Mesh(new THREE.BoxGeometry(.52,.07,.27),scarf.material),0,1.72,-.36);
  const shoe=new THREE.MeshStandardMaterial({color:0x1b2350,roughness:.6});
  const limb=(r,mat)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,1,8),mat);walker.add(m);return m};
  const L=[0,1].map(()=>({th:limb(.1,pants),sh:limb(.085,pants),ft:put(new THREE.Mesh(new THREE.BoxGeometry(.16,.1,.32),shoe),0,0,0),
    ua:limb(.075,jacket),la:limb(.065,jacket),hn:put(new THREE.Mesh(new THREE.SphereGeometry(.075,8,6),skin),0,0,0)}));
  walker.userData={L,st,ph:0,amp:0}}
// ciclo de caminata: piernas y brazos opuestos, rebote del cuerpo y un paso sonoro en cada apoyo
function walkPose(dt,speed){const W=walker.userData,target=Math.min(1,Math.abs(speed)/5);W.amp+=(target-W.amp)*Math.min(1,dt*8);
  const prev=Math.sin(W.ph);if(W.amp>.03)W.ph+=dt*(3.2+Math.abs(speed)*.85)*(speed<0?-1:1);
  if(Math.sign(Math.sin(W.ph))!==Math.sign(prev)&&W.amp>.3)SFX.step();
  const dir=a=>[0,-Math.cos(a),Math.sin(a)];
  W.L.forEach((l,i)=>{const sd=i?-1:1,ph=W.ph+(i?Math.PI:0),a=Math.sin(ph)*.55*W.amp,bend=Math.max(0,Math.sin(ph+1.4))*.9*W.amp;
    const hip=[sd*.13,1.0,0],knee=add(hip,scl(dir(a),.48)),ank=add(knee,scl(dir(a-bend),.46));setSeg(l.th,hip,knee);setSeg(l.sh,knee,ank);l.ft.position.set(ank[0],Math.max(.05,ank[1]-.02),ank[2]+.08);
    const aa=-Math.sin(ph)*.5*W.amp,sh=[sd*.37,1.85,0],el=add(sh,scl(dir(aa),.36)),hn=add(el,scl(dir(aa+.25+.3*W.amp),.33));setSeg(l.ua,sh,el);setSeg(l.la,el,hn);l.hn.position.set(...hn)});
  walker.position.y=Math.abs(Math.sin(W.ph))*.07*W.amp;W.st.rotation.y=Math.sin(W.ph*2)*.25*W.amp}
walkPose(0,0);

/* ============ Estado del juego ============ */""")

# 2) sonido: ambientes por salón y pasos
rep("  const notes=(fs,step,type,vol)=>", r"""  // ambientes de cada salón: un colchón sostenido + un patrón rítmico propio, en su propio bus
  let ab=null,ambT=null,ambNodes=[],ambId=null,stp=0;
  function pl(f0,f1,dur,type,vol,delay=0){if(!ab)return;const t=T()+delay,o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(Math.max(20,f1),t+dur);
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.015);g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(g);g.connect(ab);o.start(t);o.stop(t+dur+.05)}
  function nzA(dur,f,vol,type='bandpass',q=1){if(!ab)return;const t=T(),src=ctx.createBufferSource(),fl=ctx.createBiquadFilter(),g=ctx.createGain();src.buffer=noiseBuf;fl.type=type;fl.frequency.value=f;fl.Q.value=q;
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+dur);src.connect(fl);fl.connect(g);g.connect(ab);src.start(t,Math.random());src.stop(t+dur+.05)}
  function pad(fs,type,vol,cut,lfoHz=0){const fl=ctx.createBiquadFilter();fl.type='lowpass';fl.frequency.value=cut;const g=ctx.createGain();g.gain.value=vol;fl.connect(g);g.connect(ab);ambNodes.push(fl,g);
    fs.forEach((f,i)=>{const o=ctx.createOscillator();o.type=type;o.frequency.value=f;o.detune.value=(i%2?6:-6);o.connect(fl);o.start();ambNodes.push(o)});
    if(lfoHz){const l=ctx.createOscillator(),lg=ctx.createGain();l.frequency.value=lfoHz;lg.gain.value=cut*.6;l.connect(lg);lg.connect(fl.frequency);l.start();ambNodes.push(l,lg)}}
  const pick=a=>a[Math.floor(Math.random()*a.length)];
  const PAT={
    componentes(){if(stp%3===0)pl(...(f=>[f,f*.995])(pick([523.3,587.3,659.3,784,880,1046.5])),1.4,'sine',.05)},
    herramientas(){const b=stp%8;if(b===0||b===4)pl(95,42,.22,'sine',.16);if(b===2||b===6)nzA(.06,5200,.05,'highpass',.7);if(stp%32===12){pl(1480,1470,.6,'triangle',.035);pl(2220,2200,.4,'sine',.015)}if(b===7)nzA(.04,2600,.03,'bandpass',5)},
    topologia(){if(stp%16===0)pl(440,438,2.8,'sine',.035);if(stp%16===8)pl(329.6,328,2.8,'sine',.03)},
    atajos(){const arp=[440,554.4,659.3,880,659.3,554.4,493.9,659.3];pl(arp[stp%8],arp[stp%8],.12,'square',.018);if(stp%2===0)nzA(.025,3400,.045,'bandpass',4);if(stp%8===0)pl(110,108,.3,'triangle',.07)},
    flujo(){if(stp%3===0)pl(...(f=>[f,f*.6])(1100+Math.random()*900),.18,'sine',.03);if(stp%24===0)pl(196,196,3.5,'sine',.03)},
    academia(){if(stp%16===0){pl(1046.5,1044,2.4,'sine',.045);pl(2093,2088,1.6,'sine',.015)}if(stp%16===10)pl(784,782,2,'sine',.03)}};
  const PADS={componentes:()=>pad([261.6,392,523.3],'sine',.018,1200),herramientas:()=>pad([65.4,98,130.8],'sawtooth',.03,320),topologia:()=>pad([220,261.6,329.6],'triangle',.03,700,.05),
    atajos:()=>pad([110,164.8],'sawtooth',.012,500),flujo:()=>{pad([196,293.7,392],'sine',.022,900);const src=ctx.createBufferSource();src.buffer=noiseBuf;src.loop=true;const fl=ctx.createBiquadFilter();fl.type='bandpass';fl.frequency.value=700;fl.Q.value=.6;const g=ctx.createGain();g.gain.value=.025;src.connect(fl);fl.connect(g);g.connect(ab);src.start();ambNodes.push(src,fl,g)},
    academia:()=>pad([261.6,329.6,392,493.9],'sawtooth',.012,900,.04)};
  function stopAmb(){if(ambT){clearInterval(ambT);ambT=null}if(ab){const old=ab,nodes=ambNodes;old.gain.setTargetAtTime(0,T(),.3);setTimeout(()=>{nodes.forEach(n=>{try{n.stop&&n.stop()}catch(e){}try{n.disconnect()}catch(e){}});old.disconnect()},1500)}ab=null;ambNodes=[];ambId=null}
  const notes=(fs,step,type,vol)=>""")
rep("    quiet(){if(!ctx)return;const now=T();eng.g.gain.setTargetAtTime(0,now,.08);scr.g.gain.setTargetAtTime(0,now,.05);amb.gain.setTargetAtTime(.012,now,.5)},",
    """    quiet(){if(!ctx)return;const now=T();eng.g.gain.setTargetAtTime(0,now,.08);scr.g.gain.setTargetAtTime(0,now,.05);amb.gain.setTargetAtTime(ambId?.002:.012,now,.5)},
    hallAmb(id){if(!ctx)return;stopAmb();if(!id||!PAT[id]){amb.gain.setTargetAtTime(.022,T(),.6);return}ambId=id;ab=ctx.createGain();ab.gain.value=0;ab.connect(master);ab.gain.setTargetAtTime(1,T(),.8);
      amb.gain.setTargetAtTime(.002,T(),.4);PADS[id]();stp=0;ambT=setInterval(()=>{if(ctx.state==='running'){PAT[id]();stp++}},150)},
    step(){if(ok('step',140)){noise(.07,800,280,.07,'lowpass',.7);tone(130,70,.07,'sine',.05)}},""")
rep("document.addEventListener('visibilitychange',()=>{if(document.hidden)SFX.quiet()});",
    "document.addEventListener('visibilitychange',()=>{if(document.hidden)SFX.quiet();SFX.pause(document.hidden)});")
rep("    toggle(){on=!on;", "    pause(h){if(ctx){h?ctx.suspend():ctx.resume()}},\n    toggle(){on=!on;")

# 3) salón: el personaje camina
rep("curHall.sc.add(trike);S.x=curHall.ex.x;", "curHall.sc.add(walker);walker.userData.amp=0;S.x=curHall.ex.x;")
rep("const fx=Math.sin(S.h),fz=Math.cos(S.h);cam.position.set(S.x-fx*9,4.4,S.z-fz*9);cam.lookAt(S.x+fx*5,1.9,S.z+fz*5);",
    "const fx=Math.sin(S.h),fz=Math.cos(S.h);cam.position.set(S.x-fx*6.5,3.4,S.z-fz*6.5);cam.lookAt(S.x+fx*3,2.4,S.z+fz*3);q('speed').querySelector('small').textContent='KM/H · A PIE';")
rep("SFX.init();SFX.enter();if(firstAll)setTimeout(()=>SFX.win(),450);\n  const h=curHall.st.find(o=>o.holo);",
    "SFX.init();SFX.enter();SFX.hallAmb(b.id);if(firstAll)setTimeout(()=>SFX.win(),450);\n  const h=curHall.st.find(o=>o.holo);")
rep("function exitHall(){if(mode!=='hall')return;mode='city';scene.add(trike);",
    "function exitHall(){if(mode!=='hall')return;mode='city';if(walker.parent)walker.parent.remove(walker);SFX.hallAmb(null);q('speed').querySelector('small').textContent='KM/H · TRICICLO';")
a = s.index("function updateHall(dt,t){")
b = s.index("let hallFrame=0;")
s = s[:a] + r"""function updateHall(dt,t){const H=curHall;
  // caminar: W/S avanzan y retroceden, A/D giran; Shift para correr
  const max=keys.boost?12:7;if(keys.up)S.v+=24*dt;else if(keys.down)S.v-=24*dt;else S.v-=Math.sign(S.v)*Math.min(Math.abs(S.v),30*dt);
  S.v=Math.max(-4,Math.min(max,S.v));const st=(keys.left?1:0)-(keys.right?1:0);S.steer+=(st-S.steer)*Math.min(1,dt*10);
  S.h+=S.steer*dt*2.6;S.mh=S.h;S.drift=false;S.x+=Math.sin(S.h)*S.v*dt;S.z+=Math.cos(S.h)*S.v*dt;
  for(const c of H.cols){const dx=S.x-c.x,dz=S.z-c.z,d=Math.hypot(dx,dz),m=c.r+.8;if(d<m&&d>0){S.x=c.x+dx/d*m;S.z=c.z+dz/d*m;S.v*=.6}}
  const r=Math.hypot(S.x,S.z),lim=H.RH-1.5;if(r>lim){S.x*=lim/r;S.z*=lim/r;S.v*=.6}
  walker.position.x=S.x;walker.position.z=S.z;walker.rotation.y=S.h;walkPose(dt,S.v);
  const fx=Math.sin(S.h),fz=Math.cos(S.h),back=6.5;const want=new THREE.Vector3(S.x-fx*back,3.4,S.z-fz*back);
  const wr=Math.hypot(want.x,want.z);if(wr>H.RH-1.2){want.x*=(H.RH-1.2)/wr;want.z*=(H.RH-1.2)/wr}cam.position.lerp(want,1-Math.exp(-dt*5));cam.lookAt(S.x+fx*3,2.4,S.z+fz*3);
  cam.fov+=(60-cam.fov)*Math.min(1,dt*3);cam.updateProjectionMatrix();
  let nt=null;for(const o of H.st)if(Math.hypot(S.x-o.px,S.z-o.pz)<4.2)nt=o;if(!nt&&Math.hypot(S.x-H.ex.x,S.z-H.ex.z)<4.2)nt='exit';if(nt!==hallNear){hallNear=nt;showHallPrompt()}
  q('spd').parentElement.style.borderColor='';q('spd').textContent=Math.round(Math.abs(S.v)*3.6)}
""" + s[b:]
rep("pl.position.set(0,s.panel?16:12.5,0)", "pl.position.set(0,s.panel?15.5:11.5,0)")
# el motor del triciclo no suena dentro de los edificios
rep("if(paused||!q('start').hidden)SFX.quiet();else SFX.drive(", "if(paused||!q('start').hidden||mode==='hall')SFX.quiet();else SFX.drive(")
rep("entras a un salón 3D con estaciones animadas.", "bajas del triciclo y recorres a pie un salón 3D con estaciones animadas y su propia música de fondo (<kbd>W</kbd> caminar, <kbd>Shift</kbd> correr).")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
