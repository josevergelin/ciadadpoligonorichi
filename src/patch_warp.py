# Transición holográfica al cambiar de entorno (ciudad <-> salón) + cartel holográfico de bienvenida y nombres
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# --- CSS: velo de teletransporte y texto holográfico ---
rep("#trick{position:fixed;", r"""#warp{position:fixed;inset:0;z-index:4;pointer-events:none;opacity:0;
  background:repeating-linear-gradient(0deg,rgba(140,240,255,.18) 0 2px,transparent 2px 5px),radial-gradient(circle at 50% 55%,rgba(120,235,255,.85),rgba(0,118,214,.55) 45%,rgba(4,10,50,.95) 100%)}
#holoTxt{position:fixed;z-index:7;left:50%;top:30%;transform:translate(-50%,-50%);pointer-events:none;text-align:center;opacity:0;white-space:nowrap;
  font:900 italic clamp(1.6rem,5vw,3.6rem) var(--f-display);letter-spacing:.06em;text-transform:uppercase;color:#bff6ff;
  text-shadow:0 0 6px #56e0ff,0 0 22px #0076d6,0 0 44px rgba(86,224,255,.6)}
#holoTxt small{display:block;font:700 clamp(.7rem,1.6vw,1rem) var(--f-display);letter-spacing:.4em;color:#F7C948;text-shadow:0 0 10px rgba(247,201,72,.8);margin-bottom:.4em}
#holoTxt.show{animation:holoIn 3.2s ease forwards}
#holoTxt.show::after{content:"";position:absolute;inset:-10% -4%;background:repeating-linear-gradient(0deg,rgba(191,246,255,.18) 0 1px,transparent 1px 4px);mix-blend-mode:screen}
@keyframes holoIn{0%{opacity:0;transform:translate(-50%,-50%) scaleY(.05);filter:blur(6px)}8%{opacity:1;transform:translate(-50%,-50%) scaleY(1.15);filter:blur(0)}
  12%{transform:translate(-52%,-50%) skewX(-12deg)}14%{transform:translate(-48%,-50%) skewX(10deg)}16%{transform:translate(-50%,-50%)}70%{opacity:1}
  76%{opacity:.3}78%{opacity:1}100%{opacity:0;transform:translate(-50%,-62%);filter:blur(4px)}}
@media (prefers-reduced-motion:reduce){#holoTxt.show{animation-duration:.01s;opacity:1}}
#trick{position:fixed;""")
rep('<div id="trick" aria-live="polite"></div>', '<div id="warp"></div><div id="holoTxt" aria-live="polite"></div>\n<div id="trick" aria-live="polite"></div>')

# --- sonidos de teletransporte ---
rep("    ai(){if(ok('ai',300)){", "    warp(){if(ok('warp',500)){tone(110,1900,1,'sawtooth',.045);noise(1,300,7000,.08,'bandpass',1.5);for(let i=0;i<5;i++)tone(2400+i*300,1200,.05,'square',.012,.15+i*.14)}},\n    materialize(){if(ok('mat',500)){tone(1800,180,.8,'sine',.06);noise(.7,7000,300,.06,'bandpass',1.5);tone(73.4,70,1,'sine',.08)}},\n    ai(){if(ok('ai',300)){")

# --- voz: sin voz en español no habla en otro idioma; siempre muestra el cartel holográfico ---
rep("  return{say(text){if(!has||!SFX.isOn())return;try{speechSynthesis.cancel();SFX.ai();",
    "  return{say(text,sub){holoBanner(text,sub);if(!has||!SFX.isOn()||!v){SFX.ai();return}try{speechSynthesis.cancel();SFX.ai();")
rep("const VOICE=(()=>{", r"""function holoBanner(text,sub){const el=q('holoTxt');el.innerHTML=(sub?`<small>${sub}</small>`:'')+text;el.classList.remove('show');void el.offsetWidth;el.classList.add('show')}
const VOICE=(()=>{""")
rep("if(dc<26&&!welcomed){welcomed=true;VOICE.say('Bienvenido a Universidad Israel');trick('Bienvenido a Universidad Israel')}else if(dc>44)welcomed=",
    "if(dc<34&&!welcomed){welcomed=true;VOICE.say('Bienvenido a Universidad Israel','Emprende · trasciende · innova')}else if(dc>52)welcomed=")
rep("VOICE.say(b.name.charAt(0)+b.name.slice(1).toLowerCase());", "VOICE.say(b.name.charAt(0)+b.name.slice(1).toLowerCase(),'Ingresando a');")
s = s.replace("trick(`Interior · ${b.name}`);", "")

# --- transición: el vehículo/personaje se vuelve holograma y se desintegra; luego el otro se materializa ---
rep("/* Bucle */", r"""/* ============ Transición holográfica entre entornos ============ */
const HOLO_MAT=new THREE.MeshBasicMaterial({color:0x56e0ff,wireframe:true,transparent:true,opacity:.9,blending:THREE.AdditiveBlending,depthWrite:false});
let trans=null;
function swapHolo(obj,on){obj.traverse(o=>{if(!o.isMesh)return;if(on){if(!o.userData.om){o.userData.om=o.material;o.material=HOLO_MAT}}else if(o.userData.om){o.material=o.userData.om;delete o.userData.om}})}
function samplePts(obj,max){obj.updateMatrixWorld(true);const pts=[];obj.traverse(o=>{if(!o.isMesh||!o.geometry||!o.geometry.attributes.position)return;const a=o.geometry.attributes.position,stp=Math.max(1,Math.floor(a.count/60));
  for(let i=0;i<a.count;i+=stp)pts.push(new THREE.Vector3(a.getX(i),a.getY(i),a.getZ(i)).applyMatrix4(o.matrixWorld))});
  for(let i=pts.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[pts[i],pts[j]]=[pts[j],pts[i]]}return pts.slice(0,max)}
function makeBurst(sc,pts,inward){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(new Float32Array(pts.length*3),3));
  const m=new THREE.PointsMaterial({color:0x9ff4ff,size:4,sizeAttenuation:false,transparent:true,opacity:1,blending:THREE.AdditiveBlending,depthWrite:false});
  const P=new THREE.Points(g,m);P.frustumCulled=false;sc.add(P);let y0=1e9,y1=-1e9;pts.forEach(p=>{y0=Math.min(y0,p.y);y1=Math.max(y1,p.y)});
  return{P,g,m,sc,inward,home:pts,vel:pts.map(()=>new THREE.Vector3((Math.random()-.5)*4,2.5+Math.random()*6,(Math.random()-.5)*4)),
    delay:pts.map(p=>(y1-p.y)/Math.max(.01,y1-y0)*.45)}}
function updBurst(B,k){const a=B.g.attributes.position.array;B.home.forEach((h,i)=>{let u=Math.min(1,Math.max(0,(k-B.delay[i])/(1-B.delay[i]*.9)));if(B.inward)u=1-Math.min(1,Math.max(0,(k*1.25-B.delay[i]*.5)));
    const e=u*u,v=B.vel[i],sw=Math.sin(i+k*9)*.6*e;a[i*3]=h.x+v.x*e+sw;a[i*3+1]=h.y+v.y*e;a[i*3+2]=h.z+v.z*e+Math.cos(i+k*9)*.6*e});B.g.attributes.position.needsUpdate=true;B.m.opacity=B.inward?Math.min(1,k*1.5):1-k*.85}
function killBurst(B){B.sc.remove(B.P);B.g.dispose();B.m.dispose()}
function startWarp(fromObj,fromScene,doSwitch,toObjFn){if(trans)return;for(const k in keys)keys[k]=false;S.v=0;SFX.warp();
  swapHolo(fromObj,true);trans={ph:0,t:0,from:fromObj,burst:makeBurst(fromScene,samplePts(fromObj,800),false),doSwitch,toObjFn}}
function stepWarp(dt){const T=trans;T.t+=dt;const veil=q('warp');
  if(T.ph===0){const k=Math.min(1,T.t/1);HOLO_MAT.opacity=(1-k)*(.55+.45*Math.random());updBurst(T.burst,k);veil.style.opacity=Math.max(0,(k-.55)/.45);
    if(k>=1){swapHolo(T.from,false);killBurst(T.burst);T.doSwitch();const to=T.toObjFn(),sc=mode==='hall'?curHall.sc:scene;T.to=to;T.burst=makeBurst(sc,samplePts(to,800),true);swapHolo(to,true);T.ph=1;T.t=0;SFX.materialize()}}
  else{const k=Math.min(1,T.t/.9);HOLO_MAT.opacity=Math.min(.9,k*1.2)*(.7+.3*Math.random());updBurst(T.burst,k);veil.style.opacity=Math.max(0,1-k*1.6);
    if(k>=1){swapHolo(T.to,false);killBurst(T.burst);veil.style.opacity=0;trans=null}}}
function warpIn(b){startWarp(trike,scene,()=>enterHall(b),()=>walker)}
function warpOut(){if(mode!=='hall')return;startWarp(walker,curHall.sc,()=>exitHall(),()=>trike)}

/* Bucle */""")
rep("  if(mode==='hall'){if(!paused)updateHall(dt,t);animHall(dt,t);R.render(curHall.sc,cam);drawMiniHall();return}",
    "  if(trans){stepWarp(dt);if(mode==='hall'){animHall(dt,t);R.render(curHall.sc,cam);drawMiniHall()}else{animate(dt,t);R.render(scene,cam);drawMini()}return}\n  if(mode==='hall'){if(!paused)updateHall(dt,t);animHall(dt,t);R.render(curHall.sc,cam);drawMiniHall();return}")
rep("if(nb&&q('interior').hidden){enterHall(nb);return}", "if(nb&&q('interior').hidden){warpIn(nb);return}")
rep("if(nt==='exit'){exitHall();return}", "if(nt==='exit'){warpOut();return}")
rep("else if(e.code==='Escape')exitHall();return}", "else if(e.code==='Escape')warpOut();return}")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
