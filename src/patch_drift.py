# Añade: drift con barra espaciadora y rampa de salto
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html')
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, 1)

# --- CSS y HUD ---
rep("#prompt{left:50%;", "#trick{position:fixed;z-index:6;left:50%;top:22%;transform:translateX(-50%);font:900 italic clamp(1.6rem,4vw,2.6rem) var(--f-display);color:#F7C948;text-shadow:0 3px 0 #141B45,0 0 24px rgba(247,201,72,.6);pointer-events:none;opacity:0;transition:opacity .25s;white-space:nowrap}\n#trick.on{opacity:1}\n#prompt{left:50%;")
rep('<div id="touch" aria-hidden="true"><div><button data-k="left">◀</button><button data-k="right">▶</button></div><div><button data-k="down">▼</button><button data-k="up">▲</button></div></div>',
    '<div id="trick" aria-live="polite"></div>\n<div id="touch" aria-hidden="true"><div><button data-k="left">◀</button><button data-k="right">▶</button></div><div><button data-k="drift" style="font-size:.8rem">DRIFT</button><button data-k="down">▼</button><button data-k="up">▲</button></div></div>')
rep('<span><kbd>Shift</kbd> turbo</span>', '<span><kbd>Shift</kbd> turbo</span><span><kbd>Espacio</kbd> drift</span>')
rep("<div><b>TURBO</b>Mantén <kbd>Shift</kbd> para acelerar por las avenidas.</div>",
    "<div><b>TURBO Y DRIFT</b>Mantén <kbd>Shift</kbd> para acelerar y <kbd>Espacio</kbd> al girar para derrapar. Suelta tras un drift largo para un mini turbo.</div>\n      <div><b>RAMPA</b>En la plaza hay una rampa amarilla: tómala a toda velocidad para saltar.</div>")

# --- Rampa (antes de las esferas, que también la usan como suelo) ---
rep("// Esferas pequeñas con el logo: ruedan y saltan al chocar con el triciclo",
r"""// Rampa de salto en la plaza, apuntando hacia una avenida (sube a lo largo de su +z local)
const RAMP={a:30*Math.PI/180,r:34,L:11,W:7,H:2.6};RAMP.x=Math.sin(RAMP.a)*RAMP.r;RAMP.z=Math.cos(RAMP.a)*RAMP.r;
{const g=new THREE.BoxGeometry(RAMP.W,1,RAMP.L,4,1,6),pa=g.attributes.position;
  for(let i=0;i<pa.count;i++){const z=pa.getZ(i),y=pa.getY(i)+.5;pa.setY(i,y*RAMP.H*(z+RAMP.L/2)/RAMP.L)}g.computeVertexNormals();
  const rm=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xf7c948,roughness:.7,polygonOffset:true,polygonOffsetFactor:1}));rm.add(wireLines(quadEdges(g)));
  // franjas de advertencia en la cara inclinada
  const c=document.createElement('canvas');c.width=256;c.height=64;const x=c.getContext('2d');x.fillStyle='#141628';x.fillRect(0,0,256,64);x.fillStyle='#F7C948';for(let i=-2;i<12;i++){x.beginPath();x.moveTo(i*32,64);x.lineTo(i*32+16,64);x.lineTo(i*32+48,0);x.lineTo(i*32+32,0);x.fill()}
  const strip=new THREE.Mesh(new THREE.PlaneGeometry(RAMP.W,1.2),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c)}));const ang=Math.atan2(RAMP.H,RAMP.L);
  strip.rotation.x=-Math.PI/2-ang;strip.position.set(0,RAMP.H*(RAMP.L-.7)/RAMP.L+.03,RAMP.L/2-.7);rm.add(strip);
  rm.position.set(RAMP.x,0,RAMP.z);rm.rotation.y=RAMP.a;scene.add(rm)}
function groundH(x,z){const dx=x-RAMP.x,dz=z-RAMP.z,sa=Math.sin(RAMP.a),ca=Math.cos(RAMP.a),lz=dx*sa+dz*ca,lx=dx*ca-dz*sa;
  if(Math.abs(lx)<RAMP.W/2&&lz>-RAMP.L/2&&lz<RAMP.L/2)return RAMP.H*(lz+RAMP.L/2)/RAMP.L;return 0}

// Marcas de llanta del drift
const skidMat=new THREE.MeshBasicMaterial({color:0x1d1e21,transparent:true,opacity:.45,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-1});
const skids=[];{const sg=new THREE.PlaneGeometry(.28,.7);sg.rotateX(-Math.PI/2);for(let i=0;i<260;i++){const m=new THREE.Mesh(sg,skidMat);m.visible=false;scene.add(m);skids.push(m)}}
let skidI=0,skidAcc=0;

// Esferas pequeñas con el logo: ruedan y saltan al chocar con el triciclo""")

# esferas: suelo con rampa y choque según altura del triciclo
rep("function updateBalls(dt){const tvx=Math.sin(S.h)*S.v,tvz=Math.cos(S.h)*S.v;",
    "function updateBalls(dt){const tvx=Math.sin(S.mh)*S.v,tvz=Math.cos(S.mh)*S.v;")
rep("    if(b.p.y<b.r){b.p.y=b.r;if(b.v.y<-3)b.v.y*=-.55;else b.v.y=0;const f=Math.pow(.45,dt);b.v.x*=f;b.v.z*=f}",
    "    const gb=groundH(b.p.x,b.p.z)+b.r;if(b.p.y<gb){b.p.y=gb;if(b.v.y<-3)b.v.y*=-.55;else b.v.y=0;const f=Math.pow(.45,dt);b.v.x*=f;b.v.z*=f}")
rep("if(d<min&&b.p.y<3.5&&d>0)", "if(d<min&&Math.abs(b.p.y-S.y-1)<2.6&&d>0)")
rep("for(const b of balls){b.p.y=Math.max(b.p.y,b.r);", "for(const b of balls){b.p.y=Math.max(b.p.y,groundH(b.p.x,b.p.z)+b.r);")

# humo extra en las ruedas traseras durante el drift
rep("  for(const p of puffs){if(p.life<=0)continue;p.life-=dt;",
r"""  if(S.drift&&!S.air){skidAcc+=dt*(18+sp);trike.updateMatrixWorld();while(skidAcc>1){skidAcc--;for(const wx of[-.8,.8]){
      const p=puffs[puffI=(puffI+1)%puffs.length];_ex.set(wx,.3,-1.05);trike.localToWorld(_ex);p.s.position.copy(_ex);p.v.set((Math.random()-.5)*2,.8+Math.random(),(Math.random()-.5)*2);p.max=p.life=.8+Math.random()*.6;p.s.visible=true;p.s.scale.setScalar(.7);
      const k=skids[skidI=(skidI+1)%skids.length];k.position.set(_ex.x,.075,_ex.z);k.rotation.y=S.mh;k.visible=true}}}
  for(const p of puffs){if(p.life<=0)continue;p.life-=dt;""")

# estado
rep("const S={x:0,z:-30,h:0,v:0,steer:0,wf:0,wr:0,crank:0};", "const S={x:0,z:-30,h:0,mh:0,y:0,vy:0,air:false,lastVy:0,drift:false,dt0:0,airT:0,v:0,steer:0,wf:0,wr:0,crank:0};")
rep("S.h=b.angle;S.v=0;snapCam()}", "S.h=S.mh=b.angle;S.v=0;S.y=0;S.air=false;snapCam()}")
rep("S.x=0;S.z=24;S.h=0;snapCam()", "S.x=0;S.z=24;S.h=S.mh=0;S.y=0;snapCam()")
rep("ShiftLeft:'boost',ShiftRight:'boost'};", "ShiftLeft:'boost',ShiftRight:'boost',Space:'drift'};")

# física de manejo
rep("""  S.h+=S.steer*dt*1.9*Math.tanh(S.v/6);
  S.x+=Math.sin(S.h)*S.v*dt;S.z+=Math.cos(S.h)*S.v*dt;collide();updateBalls(dt);
  trike.position.set(S.x,0,S.z);trike.rotation.set(0,S.h,0);trike.rotateZ(-S.steer*Math.min(1,Math.abs(S.v)/25)*.18);""",
r"""  // drift: la dirección de avance (mh) sigue a la orientación (h) con poco agarre
  const wasDrift=S.drift;S.drift=!!keys.drift&&S.v>7&&!S.air;
  if(S.drift){S.dt0+=dt;S.v-=3*dt}
  else if(wasDrift){if(S.dt0>.8){S.v=Math.min(S.v+6+Math.min(6,S.dt0*3),max+10);trick(`¡Mini turbo! Drift ${S.dt0.toFixed(1)} s`)}S.dt0=0}
  S.h+=S.steer*dt*1.9*(S.drift?1.75:1)*(S.air?.35:1)*Math.tanh(S.v/6);
  let dh=S.h-S.mh;dh=Math.atan2(Math.sin(dh),Math.cos(dh));S.mh+=dh*Math.min(1,dt*(S.drift?1.4:S.air?.5:10));
  const px=S.x,pz=S.z;S.x+=Math.sin(S.mh)*S.v*dt;S.z+=Math.cos(S.mh)*S.v*dt;collide();
  // altura: rampa, despegue y aterrizaje
  const gh=groundH(S.x,S.z);
  if(S.air){S.vy-=30*dt;S.y+=S.vy*dt;S.airT+=dt;if(S.y<=gh){S.y=gh;S.air=false;if(S.airT>.35){trick(`¡Salto! ${S.airT.toFixed(2)} s en el aire`);landPuff()}S.vy=0}}
  else if(gh-S.y>.6){S.x=px;S.z=pz;S.v*=-.3}
  else if(gh<S.y-.25){S.air=true;S.airT=0;S.vy=Math.max(0,S.lastVy)*1.15+2}
  else{S.lastVy=(gh-S.y)/Math.max(dt,1e-3);S.y=gh}
  updateBalls(dt);
  const slope=gh>0&&!S.air?Math.atan2(RAMP.H,RAMP.L)*Math.cos(S.mh-RAMP.a):0;const pitch=S.air?Math.atan2(S.vy,Math.max(4,Math.abs(S.v)))*.7:slope;
  trike.position.set(S.x,S.y,S.z);trike.rotation.set(0,S.h,0);trike.rotateX(-pitch);trike.rotateZ(-S.steer*Math.min(1,Math.abs(S.v)/25)*(S.drift?.3:.18));""")
rep("const want=new THREE.Vector3(S.x-fx*back,4.6+Math.abs(S.v)*.03,S.z-fzv*back);", "const want=new THREE.Vector3(S.x-Math.sin(S.mh)*back,4.6+S.y*.85+Math.abs(S.v)*.03,S.z-Math.cos(S.mh)*back);")
rep("cam.lookAt(S.x+fx*5,1.9,S.z+fzv*5);", "cam.lookAt(S.x+fx*5,1.9+S.y*.8,S.z+fzv*5);")
rep("  updateSmoke(dt);q('spd').textContent=", "  updateSmoke(dt);q('spd').parentElement.style.borderColor=S.drift?'#F7C948':'';q('spd').textContent=")

# utilidades: mensaje de truco y polvo de aterrizaje
rep("function collide(){",
r"""let trickT=0;function trick(t){const el=q('trick');el.textContent=t;el.classList.add('on');clearTimeout(trickT);trickT=setTimeout(()=>el.classList.remove('on'),1600)}
function landPuff(){for(let i=0;i<14;i++){const p=puffs[puffI=(puffI+1)%puffs.length];const a=i/14*Math.PI*2;p.s.position.set(S.x+Math.cos(a)*1.2,S.y+.3,S.z+Math.sin(a)*1.2);
  p.v.set(Math.cos(a)*4,.6+Math.random(),Math.sin(a)*4);p.max=p.life=.9+Math.random()*.5;p.s.visible=true;p.s.scale.setScalar(.8)}}
function collide(){""")

# minimapa: rampa
rep("  mx.fillStyle='#ffffff';balls.forEach(", "  {const p=P(RAMP.x,RAMP.z);mx.fillStyle='#F7C948';mx.fillRect(p[0]-5,p[1]-5,10,10)}\n  mx.fillStyle='#ffffff';balls.forEach(")
open(p, 'w', encoding='utf-8').write(s)
print('patched')
