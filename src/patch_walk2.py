# Interiores: sonidos futuristas, caminata fluida y orientación con el mouse (la ciudad no se toca)
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)
def span(a_mark, b_mark, new, include_b=False):
    global s
    a = s.index(a_mark); b = s.index(b_mark, a)
    if include_b: b += len(b_mark)
    s = s[:a] + new + s[b:]

# ---------- 1) sonidos futuristas de los interiores ----------
span("  const pick=a=>a[Math.floor(Math.random()*a.length)];", "  function stopAmb(){", r"""  const pick=a=>a[Math.floor(Math.random()*a.length)];
  // síntesis FM para campanas metálicas y cristalinas
  function fm(f,ratio,idx,dur,vol,delay=0){if(!ab)return;const t=T()+delay,c=ctx.createOscillator(),m=ctx.createOscillator(),mg=ctx.createGain(),g=ctx.createGain();c.frequency.value=f;m.frequency.value=f*ratio;
    mg.gain.setValueAtTime(f*idx,t);mg.gain.exponentialRampToValueAtTime(Math.max(1,f*idx*.04),t+dur);m.connect(mg);mg.connect(c.frequency);
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+dur);c.connect(g);g.connect(ab);c.start(t);m.start(t);c.stop(t+dur+.05);m.stop(t+dur+.05)}
  // colchón con filtro resonante que se abre y cierra (barrido de sintetizador)
  function padR(fs,type,vol,cut,Q,lfoHz,depth){const fl=ctx.createBiquadFilter();fl.type='lowpass';fl.frequency.value=cut;fl.Q.value=Q;const g=ctx.createGain();g.gain.value=vol;fl.connect(g);g.connect(ab);ambNodes.push(fl,g);
    fs.forEach((f,i)=>{[-8,8].forEach(dt=>{const o=ctx.createOscillator();o.type=type;o.frequency.value=f;o.detune.value=dt+i*2;o.connect(fl);o.start();ambNodes.push(o)})});
    const l=ctx.createOscillator(),lg=ctx.createGain();l.frequency.value=lfoHz;lg.gain.value=depth;l.connect(lg);lg.connect(fl.frequency);l.start();ambNodes.push(l,lg)}
  function wind(f,vol,lfo){const src=ctx.createBufferSource();src.buffer=noiseBuf;src.loop=true;const fl=ctx.createBiquadFilter();fl.type='bandpass';fl.frequency.value=f;fl.Q.value=1.2;const g=ctx.createGain();g.gain.value=vol;
    const l=ctx.createOscillator(),lg=ctx.createGain();l.frequency.value=lfo;lg.gain.value=f*.5;l.connect(lg);lg.connect(fl.frequency);l.start();src.connect(fl);fl.connect(g);g.connect(ab);src.start();ambNodes.push(src,fl,g,l,lg)}
  const PAT={
    // cristal digital: campanas FM en arpegio y barridos ascendentes
    componentes(){if(stp%2===0)fm(pick([523.3,659.3,784,987.8,1174.7,1318.5]),3.5,2,1.6,.035);if(stp%24===0)pl(180,1400,1.4,'sawtooth',.008)},
    // fábrica robótica: pulso sub, disparos láser, servos y válvulas hidráulicas
    herramientas(){const b=stp%8;if(b===0||b===4)pl(72,34,.32,'sine',.17);if(b===2||b===6)pl(2600,260,.12,'square',.02);
      if(stp%16===11)pl(320,980,.5,'sawtooth',.016);if(stp%16===14)nzA(.3,6500,.03,'highpass',.5);if(stp%32===20)fm(880,1.41,5,.9,.03)},
    // espacio profundo: sonar y latido lejano
    topologia(){if(stp%20===0)fm(660,2,1.2,3,.045);if(stp%10===5)pl(98,92,1.6,'sine',.06);if(stp%40===30)pl(1600,400,2,'triangle',.01)},
    // ciber-datos: arpegio de sierra, bips de datos y bajo
    atajos(){const arp=[220,330,440,660,440,330,494,740];pl(arp[stp%8],arp[stp%8]*1.002,.14,'sawtooth',.012);if(Math.random()<.35)pl(...(f=>[f,f])(1500+Math.random()*2200),.04,'square',.016);if(stp%8===0)pl(55,52,.4,'sine',.1)},
    // corriente de datos: notas de vidrio y barrido lento
    flujo(){if(stp%3===0)fm(pick([880,1046.5,1318.5,1568]),5,1.2,1.3,.028);if(stp%40===0)pl(150,620,4,'triangle',.014)},
    // templo sci-fi: campanas FM graves y destellos agudos
    academia(){if(stp%16===0){fm(1046.5,3.01,3,3,.04);fm(523.3,2,1.5,3,.028)}if(stp%8===4)pl(2093,2093,.6,'sine',.01)}};
  const PADS={componentes:()=>padR([130.8,196,261.6],'sawtooth',.014,600,6,.08,500),
    herramientas:()=>{padR([55,82.4],'sawtooth',.028,240,8,.12,160);wind(5000,.006,.1)},
    topologia:()=>padR([110,164.8,220,277.2],'triangle',.026,500,9,.04,400),
    atajos:()=>padR([110,165],'square',.008,400,10,.25,300),
    flujo:()=>{padR([146.8,220,293.7,370],'sine',.02,1500,1,.03,500);wind(900,.02,.05)},
    academia:()=>padR([261.6,329.6,392,493.9,587.3],'sawtooth',.009,1000,2,.05,600)};
""")
# eco espacial (delay con realimentación) en el bus del salón
rep("ambId=id;ab=ctx.createGain();ab.gain.value=0;ab.connect(master);ab.gain.setTargetAtTime(1,T(),.8);",
    "ambId=id;ab=ctx.createGain();ab.gain.value=0;ab.connect(master);ab.gain.setTargetAtTime(1,T(),.8);\n      {const dl=ctx.createDelay(1.5),fb=ctx.createGain(),wet=ctx.createGain(),lp=ctx.createBiquadFilter();dl.delayTime.value=.375;fb.gain.value=.4;wet.gain.value=.4;lp.type='lowpass';lp.frequency.value=3200;ab.connect(dl);dl.connect(lp);lp.connect(fb);fb.connect(dl);lp.connect(wet);wet.connect(master);ambNodes.push(dl,fb,wet,lp)}")
# pasos con botas futuristas
rep("    step(){if(ok('step',140)){noise(.07,800,280,.07,'lowpass',.7);tone(130,70,.07,'sine',.05)}},",
    "    step(){if(ok('step',140)){tone(64,40,.09,'sine',.07);tone(190,95,.05,'square',.02);noise(.05,3200,1600,.035,'bandpass',3)}},")

# ---------- 2) caminata fluida ----------
span("// ciclo de caminata:", "walkPose(0,0);", r"""// ciclo de caminata: la zancada avanza según la distancia recorrida (sin patinar), con transición suave entre quieto, caminar y correr
walker.rotation.order='YXZ';Object.assign(walker.userData,{lean:0,sway:0,yaw:0});
function walkPose(dt,speed){const W=walker.userData,sp=Math.abs(speed);W.amp+=(Math.min(1,sp/3.2)-W.amp)*Math.min(1,dt*6);
  const prev=Math.sin(W.ph);W.ph+=dt*sp*2.85*(speed<0?-1:1);if(Math.sign(Math.sin(W.ph))!==Math.sign(prev)&&sp>.6)SFX.step();
  const run=Math.max(0,Math.min(1,(sp-5)/3.5)),amp=W.amp,dir=a=>[0,-Math.cos(a),Math.sin(a)];
  W.L.forEach((l,i)=>{const sd=i?-1:1,ph=W.ph+(i?Math.PI:0),a=Math.sin(ph)*(.48+.2*run)*amp,bend=(Math.max(0,Math.sin(ph+1.3))*(.75+.7*run)+.06)*amp;
    const hip=[sd*.13,1.0,0],knee=add(hip,scl(dir(a),.48)),ank=add(knee,scl(dir(a-bend),.46));setSeg(l.th,hip,knee);setSeg(l.sh,knee,ank);l.ft.position.set(ank[0],Math.max(.05,ank[1]-.02),ank[2]+.08);l.ft.rotation.x=-(a-bend)*.4;
    const aa=-Math.sin(ph)*(.42+.35*run)*amp,sh=[sd*.37,1.85,0],el=add(sh,scl(dir(aa),.36)),hn=add(el,scl(dir(aa+.2+(.3+.6*run)*amp),.33));setSeg(l.ua,sh,el);setSeg(l.la,el,hn);l.hn.position.set(...hn)});
  W.lean+=(((.05+.17*run)*Math.min(1,sp/3))-W.lean)*Math.min(1,dt*5);W.sway+=((Math.sin(W.ph)*.035*amp-S.steer*.06*Math.min(1,sp/3))-W.sway)*Math.min(1,dt*8);
  walker.position.y=Math.abs(Math.cos(W.ph))*(.05+.04*run)*amp;W.st.rotation.y=Math.sin(W.ph*2)*.25*amp+Math.sin(performance.now()/700)*.08}
walkPose(0,0);""", include_b=True)

span("function updateHall(dt,t){const H=curHall;", "let hallFrame=0;", "")  # se reescribe abajo
# ---------- 3) mouse: clic para capturar (o arrastrar) y girar; vertical para mirar arriba/abajo ----------
rep("let hallFrame=0;", r"""const MOUSE={dx:0,dy:0,pitch:0,drag:false,lx:null,ly:null};
canvas.addEventListener('click',()=>{if(mode!=='hall'||document.pointerLockElement===canvas)return;try{const r=canvas.requestPointerLock&&canvas.requestPointerLock();if(r&&r.catch)r.catch(()=>{})}catch(e){}});
canvas.addEventListener('pointerdown',e=>{if(mode!=='hall')return;MOUSE.drag=true;MOUSE.lx=e.clientX;MOUSE.ly=e.clientY});
addEventListener('pointermove',e=>{if(mode!=='hall')return;if(document.pointerLockElement===canvas){MOUSE.dx+=e.movementX||0;MOUSE.dy+=e.movementY||0}
  else if(MOUSE.drag&&MOUSE.lx!==null){MOUSE.dx+=e.clientX-MOUSE.lx;MOUSE.dy+=e.clientY-MOUSE.ly;MOUSE.lx=e.clientX;MOUSE.ly=e.clientY}});
addEventListener('pointerup',()=>{MOUSE.drag=false;MOUSE.lx=null});
let hallFrame=0;""")
rep("const MOUSE={dx:0,dy:0,pitch:0,drag:false,lx:null,ly:null};", r"""const MOUSE={dx:0,dy:0,pitch:0,drag:false,lx:null,ly:null};
const camLook=new THREE.Vector3();let camYaw=0;
function updateHall(dt,t){const H=curHall,W=walker.userData;
  // orientación: teclas A/D y mouse (horizontal gira, vertical mira arriba o abajo)
  const st=(keys.left?1:0)-(keys.right?1:0);S.steer+=(st-S.steer)*Math.min(1,dt*8);
  S.h+=S.steer*dt*2.3-MOUSE.dx*.0026;MOUSE.pitch=Math.max(-.35,Math.min(.75,MOUSE.pitch-MOUSE.dy*.0022));MOUSE.dx=0;MOUSE.dy=0;S.mh=S.h;S.drift=false;
  // velocidad con aceleración suave: caminar con W, correr con Shift
  const tv=keys.up?(keys.boost?8.5:4.4):keys.down?-2.6:0;S.v+=(tv-S.v)*Math.min(1,dt*(tv===0?7:3.5));
  S.x+=Math.sin(S.h)*S.v*dt;S.z+=Math.cos(S.h)*S.v*dt;
  for(const c of H.cols){const dx=S.x-c.x,dz=S.z-c.z,d=Math.hypot(dx,dz),m=c.r+.8;if(d<m&&d>0){S.x=c.x+dx/d*m;S.z=c.z+dz/d*m}}
  const r=Math.hypot(S.x,S.z),lim=H.RH-1.5;if(r>lim){S.x*=lim/r;S.z*=lim/r}
  // el cuerpo sigue la orientación con suavidad
  let dy=S.h-W.yaw;dy=Math.atan2(Math.sin(dy),Math.cos(dy));W.yaw+=dy*Math.min(1,dt*12);
  walkPose(dt,S.v);walker.position.x=S.x;walker.position.z=S.z;walker.rotation.set(W.lean,W.yaw,W.sway);
  // cámara en tercera persona con seguimiento suave
  let dc=S.h-camYaw;dc=Math.atan2(Math.sin(dc),Math.cos(dc));camYaw+=dc*Math.min(1,dt*6);
  const fx=Math.sin(camYaw),fz=Math.cos(camYaw),back=6.2-MOUSE.pitch*1.2;const want=new THREE.Vector3(S.x-fx*back,3.2-MOUSE.pitch*1.4,S.z-fz*back);
  const wr=Math.hypot(want.x,want.z);if(wr>H.RH-1.2){want.x*=(H.RH-1.2)/wr;want.z*=(H.RH-1.2)/wr}cam.position.lerp(want,1-Math.exp(-dt*7));
  camLook.lerp(new THREE.Vector3(S.x+fx*3,2.2+MOUSE.pitch*6,S.z+fz*3),1-Math.exp(-dt*9));cam.lookAt(camLook);
  cam.fov+=(60-cam.fov)*Math.min(1,dt*3);cam.updateProjectionMatrix();
  let nt=null;for(const o of H.st)if(Math.hypot(S.x-o.px,S.z-o.pz)<4.2)nt=o;if(!nt&&Math.hypot(S.x-H.ex.x,S.z-H.ex.z)<4.2)nt='exit';if(nt!==hallNear){hallNear=nt;showHallPrompt()}
  q('spd').parentElement.style.borderColor='';q('spd').textContent=Math.round(Math.abs(S.v)*3.6)}""")
# al entrar: orientar cámara y cuerpo, y mostrar los controles a pie
rep("curHall.sc.add(walker);walker.userData.amp=0;", "curHall.sc.add(walker);Object.assign(walker.userData,{amp:0,yaw:Math.PI,lean:0,sway:0});camYaw=Math.PI;MOUSE.pitch=0;MOUSE.dx=MOUSE.dy=0;")
rep("trick(`Interior · ${b.name}`)}", "camLook.set(S.x,2.2,S.z-3);trick(`Interior · ${b.name}`);KEYS_CITY=KEYS_CITY||q('keys').innerHTML;q('keys').innerHTML='<span><kbd>W A S D</kbd> caminar y girar</span><span><kbd>Shift</kbd> correr</span><span><kbd>Mouse</kbd> clic o arrastra para mirar</span><span><kbd>E</kbd> lección</span><span><kbd>Esc</kbd> salir</span>'}\nlet KEYS_CITY=null;")
rep("function exitHall(){if(mode!=='hall')return;mode='city';", "function exitHall(){if(mode!=='hall')return;mode='city';try{if(document.pointerLockElement)document.exitPointerLock()}catch(e){}if(KEYS_CITY)q('keys').innerHTML=KEYS_CITY;")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
