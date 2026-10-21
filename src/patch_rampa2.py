# Rampa blanca frente a la salida (sube hacia afuera, entre dos radios de la retícula) + eslogan en la rampa y el piso
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html')
s = open(p, encoding='utf-8').read()
a = s.index('// Rampa de salto curva')
b = s.index('\n', s.index('function rampPitch('))
new = r"""// Rampa de salto blanca justo delante de la salida: ocupa celdas de la retícula circular (entre dos radios y dos arcos) y sube hacia afuera
const D2R=Math.PI/180;
const RAMP={r0:27,r1:45,ta:-15*D2R,tb:15*D2R,H:3.6};RAMP.x=0;RAMP.z=36;
const rampH=r=>RAMP.H*(r-RAMP.r0)/(RAMP.r1-RAMP.r0);
// Eslogan con las letras invertidas del logo (P y D en EMPRENDE, N en INNOVA)
function drawSlogan(x,cx,y,size,color,lines){x.fillStyle=color;x.textBaseline='alphabetic';
  const word=(w,wt,mir)=>{x.font=`${wt} ${size}px Montserrat, Arial, sans-serif`;return{w,wt,mir,width:[...w].reduce((s,ch)=>s+x.measureText(ch).width,0)}};
  const draw=(seg,px,py)=>{x.font=`${seg.wt} ${size}px Montserrat, Arial, sans-serif`;[...seg.w].forEach((ch,i)=>{const cw=x.measureText(ch).width;
      if(seg.mir.includes(i)){x.save();x.translate(px+cw,py);x.scale(-1,1);x.fillText(ch,0,0);x.restore()}else x.fillText(ch,px,py);px+=cw});return px};
  const W=[word('EMPRENDE','800',[2,6]),word('trasciende','400',[]),word('INNOVA','800',[1,2])];
  if(lines){W.forEach((w,i)=>draw(w,cx-w.width/2,y+i*size*1.25))}
  else{const gap=size*.35,tot=W.reduce((s,w)=>s+w.width,0)+gap*2;let px=cx-tot/2;W.forEach(w=>{px=draw(w,px,y)+gap})}}
{const NR=6,NT=6,v=[],uv=[],top=[],bot=[];const P=(r,t,y)=>{v.push([r*Math.sin(t),y,r*Math.cos(t)]);uv.push([(RAMP.tb-t)/(RAMP.tb-RAMP.ta),(r-RAMP.r0)/(RAMP.r1-RAMP.r0)]);return v.length-1};
  for(let i=0;i<=NR;i++){top.push([]);bot.push([]);for(let j=0;j<=NT;j++){const r=RAMP.r0+(RAMP.r1-RAMP.r0)*i/NR,t=RAMP.ta+(RAMP.tb-RAMP.ta)*j/NT;top[i].push(P(r,t,rampH(r)));bot[i].push(P(r,t,0))}}
  const fTop=[],fSide=[];
  for(let i=0;i<NR;i++)for(let j=0;j<NT;j++)fTop.push([top[i][j],top[i+1][j],top[i+1][j+1],top[i][j+1]]);
  for(let i=0;i<NR;i++){fSide.push([bot[i][0],bot[i+1][0],top[i+1][0],top[i][0]]);fSide.push([bot[i][NT],top[i][NT],top[i+1][NT],bot[i+1][NT]])}
  for(let j=0;j<NT;j++)fSide.push([bot[NR][j],top[NR][j],top[NR][j+1],bot[NR][j+1]]);
  const geoOf=(fs,withUV)=>{const pos=[],uvs=[];fs.forEach(fc=>[[0,1,2],[0,2,3]].forEach(t=>t.forEach(k=>{pos.push(...v[fc[k]]);uvs.push(...uv[fc[k]])})));
    const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));if(withUV)g.setAttribute('uv',new THREE.Float32BufferAttribute(uvs,2));g.computeVertexNormals();return g};
  const c=document.createElement('canvas');c.width=1024;c.height=1024;const rampTex=new THREE.CanvasTexture(c);if(R)rampTex.anisotropy=R.capabilities.getMaxAnisotropy();
  const paint=()=>{const x=c.getContext('2d');x.fillStyle='#f4f5f7';x.fillRect(0,0,1024,1024);x.fillStyle='#0076D6';x.fillRect(0,0,1024,26);x.fillStyle='#F7C948';x.fillRect(0,26,1024,10);
    drawSlogan(x,512,380,140,'#3F4B6E',true);rampTex.needsUpdate=true};paint();rampPaint.push(paint);
  const mTop=new THREE.Mesh(geoOf(fTop,true),new THREE.MeshStandardMaterial({map:rampTex,roughness:.75,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:1}));
  const mSide=new THREE.Mesh(geoOf(fSide,false),new THREE.MeshStandardMaterial({color:0xeef0f3,roughness:.85,flatShading:true,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:1}));
  const ln=[];[...fTop,...fSide].forEach(fc=>{for(let k=0;k<4;k++)ln.push(...v[fc[k]],...v[fc[(k+1)%4]])});
  const rm=new THREE.Group();rm.add(mTop,mSide,wireLines(ln,new THREE.LineBasicMaterial({color:0x8b8f96})));rm.position.y=.02;scene.add(rm);
  // eslogan pintado en el piso, en la zona de aterrizaje
  const fc2=document.createElement('canvas');fc2.width=2048;fc2.height=256;const floorTex=new THREE.CanvasTexture(fc2);if(R)floorTex.anisotropy=R.capabilities.getMaxAnisotropy();
  const paintF=()=>{const x=fc2.getContext('2d');x.clearRect(0,0,2048,256);drawSlogan(x,1024,170,105,'#ffffff',false);floorTex.needsUpdate=true};paintF();rampPaint.push(paintF);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(34,4.25),new THREE.MeshBasicMaterial({map:floorTex,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2}));
  fl.rotation.set(-Math.PI/2,0,Math.PI);fl.position.set(0,.1,49.3);scene.add(fl)}
function groundH(x,z){const r=Math.hypot(x,z),t=Math.atan2(x,z);if(r>RAMP.r0&&r<RAMP.r1&&t>RAMP.ta&&t<RAMP.tb)return rampH(r);return 0}
// inclinación de la rampa en la dirección en que avanza el triciclo (sube hacia afuera)
function rampPitch(x,z,h){return Math.atan2(RAMP.H,RAMP.r1-RAMP.r0)*Math.cos(h-Math.atan2(x,z))}"""
s = s[:a] + "const rampPaint=[];\n" + new + s[b:]
# despegue más potente
old = "S.vy=Math.max(0,S.lastVy)*1.15+2"
assert old in s; s = s.replace(old, "S.vy=Math.max(0,S.lastVy)*1.3+3")
# repintar con la fuente cargada
old = "]).then(()=>{drawLogo();"
assert old in s; s = s.replace(old, "]).then(()=>{drawLogo();rampPaint.forEach(f=>f());")
s = s.replace("<div><b>RAMPA</b>En la plaza hay una rampa amarilla curva que sigue el círculo del piso: recórrela a toda velocidad para saltar.</div>",
              "<div><b>RAMPA</b>La rampa blanca está justo delante de la salida: acelera con <kbd>W</kbd> (y <kbd>Shift</kbd>) para saltar.</div>")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
