# Añade: esfera central con logo, esferas pequeñas con física y humo del triciclo
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html')
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, 1)

rep("""const holo=new THREE.Group();holo.position.y=26;const hc=PRESETS.cube3();holo.add(meshLines(hc,7,0xf7c948),meshPoints(hc,7,0x0076d6,8),solid(hc,7,0xffffff,.25));scene.add(holo);
scene.add(clayW(new THREE.CylinderGeometry(2,3,14,6,4),[0,7,0]));colliders.push({type:'circle',x:0,z:0,r:3.5});""",
r"""// Logo UISRAEL dibujado en un canvas (proyección equirectangular: aparece dos veces alrededor de la esfera)
const logoC=document.createElement('canvas');logoC.width=2048;logoC.height=1024;
function drawLogo(){const x=logoC.getContext('2d');x.fillStyle='#ffffff';x.fillRect(0,0,2048,1024);
  x.strokeStyle='rgba(63,75,110,.16)';x.lineWidth=3;for(let i=0;i<=32;i++){x.beginPath();x.moveTo(i*64,0);x.lineTo(i*64,1024);x.stroke()}for(let j=0;j<=16;j++){x.beginPath();x.moveTo(0,j*64);x.lineTo(2048,j*64);x.stroke()}
  [512,1536].forEach(cx=>{x.textBaseline='alphabetic';x.font='800 200px Montserrat, Arial, sans-serif';const wU=x.measureText('U').width,wI=x.measureText('ISRAEL').width,st=cx-(wU+wI)/2;
    x.fillStyle='#0076D6';x.fillText('U',st,560);x.fillStyle='#3F4B6E';x.fillText('ISRAEL',st+wU,560);
    const parts=[['EMPRENDE ','800'],['trasciende ','400'],['INNOVA','800']];let tw=0;parts.forEach(([t,w])=>{x.font=`${w} 54px Montserrat, Arial, sans-serif`;tw+=x.measureText(t).width});
    let px=cx-tw/2;parts.forEach(([t,w])=>{x.font=`${w} 54px Montserrat, Arial, sans-serif`;x.fillText(t,px,640);px+=x.measureText(t).width})});
  logoTex.needsUpdate=true}
const logoTex=new THREE.CanvasTexture(logoC);if(R)logoTex.anisotropy=R.capabilities.getMaxAnisotropy();drawLogo();
// Esfera grande en el centro de la plaza
const holo=new THREE.Group();holo.position.y=11;
const bigBall=new THREE.Mesh(new THREE.SphereGeometry(11,64,32),new THREE.MeshStandardMaterial({map:logoTex,roughness:.35,metalness:.05}));holo.add(bigBall);
const orbit=new THREE.Group();const orbRing=new THREE.Mesh(new THREE.TorusGeometry(15,.28,8,96),new THREE.MeshBasicMaterial({color:0xf7c948}));orbit.add(orbRing);
const sat=new THREE.Mesh(new THREE.SphereGeometry(.9,16,12),new THREE.MeshBasicMaterial({color:0x0076d6}));sat.position.x=15;orbit.add(sat);orbit.rotation.x=1.2;holo.add(orbit);scene.add(holo);
{const sh=new THREE.Mesh(new THREE.CircleGeometry(12,48),new THREE.MeshBasicMaterial({color:0x2e3034,transparent:true,opacity:.35,depthWrite:false}));sh.rotation.x=-Math.PI/2;sh.position.y=.1;scene.add(sh)}
colliders.push({type:'circle',x:0,z:0,r:11.3});

// Esferas pequeñas con el logo: ruedan y saltan al chocar con el triciclo
const balls=[];{const bg=new THREE.SphereGeometry(1.3,28,18),bm=new THREE.MeshStandardMaterial({map:logoTex,roughness:.35});
  for(let i=0;i<40;i++){const ring=i<26,a=Math.random()*Math.PI*2,r=ring?16+Math.random()*36:72+Math.random()*70;const m=new THREE.Mesh(bg,bm);
    const b={m,p:new THREE.Vector3(Math.sin(a)*r,1.3,Math.cos(a)*r),v:new THREE.Vector3(),r:1.3};m.position.copy(b.p);m.rotation.y=Math.random()*6.3;scene.add(m);balls.push(b)}}
const _ax=new THREE.Vector3(),_q=new THREE.Quaternion();
function pushOut(b){for(const c of colliders){if(c.type==='circle'){const dx=b.p.x-c.x,dz=b.p.z-c.z,d=Math.hypot(dx,dz),m=c.r+b.r;
      if(d<m&&d>0){const nx=dx/d,nz=dz/d;b.p.x=c.x+nx*m;b.p.z=c.z+nz*m;const vn=b.v.x*nx+b.v.z*nz;if(vn<0){b.v.x-=1.6*vn*nx;b.v.z-=1.6*vn*nz}}}
    else{const cx=Math.max(c.minx,Math.min(b.p.x,c.maxx)),cz=Math.max(c.minz,Math.min(b.p.z,c.maxz)),dx=b.p.x-cx,dz=b.p.z-cz,d=Math.hypot(dx,dz);
      if(d<b.r&&d>0){const nx=dx/d,nz=dz/d;b.p.x=cx+nx*b.r;b.p.z=cz+nz*b.r;const vn=b.v.x*nx+b.v.z*nz;if(vn<0){b.v.x-=1.6*vn*nx;b.v.z-=1.6*vn*nz}}}}}
function updateBalls(dt){const tvx=Math.sin(S.h)*S.v,tvz=Math.cos(S.h)*S.v;
  for(const b of balls){b.v.y-=32*dt;b.p.addScaledVector(b.v,dt);
    if(b.p.y<b.r){b.p.y=b.r;if(b.v.y<-3)b.v.y*=-.55;else b.v.y=0;const f=Math.pow(.45,dt);b.v.x*=f;b.v.z*=f}
    // choque con el triciclo
    const dx=b.p.x-S.x,dz=b.p.z-S.z,d=Math.hypot(dx,dz),min=b.r+1.6;
    if(d<min&&b.p.y<3.5&&d>0){const nx=dx/d,nz=dz/d;b.p.x=S.x+nx*min;b.p.z=S.z+nz*min;const rel=(tvx-b.v.x)*nx+(tvz-b.v.z)*nz;
      if(rel>0){const sp=Math.abs(S.v);b.v.x+=nx*rel*1.5+tvx*.35;b.v.z+=nz*rel*1.5+tvz*.35;b.v.y=Math.max(b.v.y,5+sp*.5);S.v*=.9}}
    pushOut(b);const rr=Math.hypot(b.p.x,b.p.z);if(rr>330){b.p.x*=330/rr;b.p.z*=330/rr;b.v.x*=-.5;b.v.z*=-.5}}
  for(let i=0;i<balls.length;i++)for(let j=i+1;j<balls.length;j++){const A=balls[i],Bb=balls[j],dx=Bb.p.x-A.p.x,dy=Bb.p.y-A.p.y,dz=Bb.p.z-A.p.z,d=Math.hypot(dx,dy,dz),m=A.r+Bb.r;
    if(d<m&&d>0){const nx=dx/d,ny=dy/d,nz=dz/d,o=(m-d)/2;A.p.x-=nx*o;A.p.y-=ny*o;A.p.z-=nz*o;Bb.p.x+=nx*o;Bb.p.y+=ny*o;Bb.p.z+=nz*o;
      const rv=(Bb.v.x-A.v.x)*nx+(Bb.v.y-A.v.y)*ny+(Bb.v.z-A.v.z)*nz;if(rv<0){const k=-.9*rv;A.v.x-=nx*k;A.v.y-=ny*k;A.v.z-=nz*k;Bb.v.x+=nx*k;Bb.v.y+=ny*k;Bb.v.z+=nz*k}}}
  for(const b of balls){b.p.y=Math.max(b.p.y,b.r);const hs=Math.hypot(b.v.x,b.v.z);
    if(hs>.02){_ax.set(b.v.z/hs,0,-b.v.x/hs);_q.setFromAxisAngle(_ax,hs*dt/b.r);b.m.quaternion.premultiply(_q)}b.m.position.copy(b.p)}}

// Humo del triciclo: partículas que salen del escape, suben, crecen y se desvanecen
const smokeTex=(()=>{const c=document.createElement('canvas');c.width=c.height=64;const x=c.getContext('2d');const g=x.createRadialGradient(32,32,2,32,32,31);
  g.addColorStop(0,'rgba(255,255,255,1)');g.addColorStop(.5,'rgba(255,255,255,.55)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,64,64);return new THREE.CanvasTexture(c)})();
const puffs=[];for(let i=0;i<110;i++){const s=new THREE.Sprite(new THREE.SpriteMaterial({map:smokeTex,color:0xd9dbdf,transparent:true,opacity:0,depthWrite:false}));s.visible=false;scene.add(s);puffs.push({s,life:0,max:1,v:new THREE.Vector3()})}
let smokeAcc=0,puffI=0;const _ex=new THREE.Vector3();
function updateSmoke(dt){const sp=Math.abs(S.v);if(sp>.4){smokeAcc+=dt*(5+sp*1.3)*(keys.boost?1.8:1);trike.updateMatrixWorld();
    while(smokeAcc>1){smokeAcc--;const p=puffs[puffI=(puffI+1)%puffs.length];_ex.set((Math.random()-.5)*.3,.9,-1.95);trike.localToWorld(_ex);p.s.position.copy(_ex);
      p.v.set(-Math.sin(S.h)*sp*.12+(Math.random()-.5)*1.2,1+Math.random()*1.2,-Math.cos(S.h)*sp*.12+(Math.random()-.5)*1.2);p.max=p.life=1.1+Math.random()*.9;p.s.visible=true;p.s.scale.setScalar(.5)}}
  for(const p of puffs){if(p.life<=0)continue;p.life-=dt;if(p.life<=0){p.s.visible=false;continue}const k=1-p.life/p.max;
    p.s.position.addScaledVector(p.v,dt);p.v.multiplyScalar(1-dt*1.6);p.v.y+=.5*dt;p.s.scale.setScalar(.5+k*3.4);p.s.material.opacity=.55*(1-k)*Math.min(1,k*8)}}""")

rep("  S.x+=Math.sin(S.h)*S.v*dt;S.z+=Math.cos(S.h)*S.v*dt;collide();",
    "  S.x+=Math.sin(S.h)*S.v*dt;S.z+=Math.cos(S.h)*S.v*dt;collide();updateBalls(dt);")
rep("  q('spd').textContent=Math.round(Math.abs(S.v)*3.6)}", "  updateSmoke(dt);q('spd').textContent=Math.round(Math.abs(S.v)*3.6)}")
rep("holo.rotation.y+=.2*dt;holo.rotation.x=Math.sin(t*.3)*.25;", "bigBall.rotation.y+=.12*dt;orbit.rotation.z+=.35*dt;")
rep("S.x=0;S.z=14;S.h=0;snapCam()", "S.x=0;S.z=24;S.h=0;snapCam()")
# minimapa: esferas como puntos blancos
rep("  mx.fillStyle='#F7C948';mx.beginPath();mx.moveTo(0,-16)",
    "  mx.fillStyle='#ffffff';balls.forEach(b=>{const p=P(b.p.x,b.p.z);mx.fillRect(p[0]-2.5,p[1]-2.5,5,5)});\n  mx.fillStyle='#F7C948';mx.beginPath();mx.moveTo(0,-16)")
# redibujar el logo cuando cargue la fuente
rep("Promise.race([document.fonts?document.fonts.load('900 italic 100px Montserrat'):Promise.resolve(),new Promise(r=>setTimeout(r,2500))]).then(()=>{",
    "Promise.race([document.fonts?Promise.all([document.fonts.load('900 italic 100px Montserrat'),document.fonts.load('800 100px Montserrat'),document.fonts.load('400 50px Montserrat')]):Promise.resolve(),new Promise(r=>setTimeout(r,2500))]).then(()=>{drawLogo();")
open(p, 'w', encoding='utf-8').write(s)
print('patched')
