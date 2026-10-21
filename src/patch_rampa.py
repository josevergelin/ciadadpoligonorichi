# Rampa curva: ocupa celdas de la retícula polar del plaza (bordes en radios y arcos) y sube a lo largo del círculo
import os, re
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html')
s = open(p, encoding='utf-8').read()
a = s.index('// Rampa de salto en la plaza')
b = s.index('return 0}', s.index('function groundH(')) + len('return 0}')
new = r"""// Rampa de salto curva: sigue la retícula circular del plaza (radios y arcos) y sube en el sentido del círculo
const D2R=Math.PI/180;
const RAMP={r0:27,r1:45,ta:15*D2R,tb:45*D2R,H:2.6};RAMP.x=Math.sin(30*D2R)*36;RAMP.z=Math.cos(30*D2R)*36;
const rampH=t=>RAMP.H*(RAMP.tb-t)/(RAMP.tb-RAMP.ta);
{const NR=4,NT=8,v=[],f=[],col=[];const P=(r,t,y)=>{v.push([r*Math.sin(t),y,r*Math.cos(t)]);return v.length-1};
  const top=[],bot=[];for(let i=0;i<=NR;i++){top.push([]);bot.push([]);for(let j=0;j<=NT;j++){const r=RAMP.r0+(RAMP.r1-RAMP.r0)*i/NR,t=RAMP.tb+(RAMP.ta-RAMP.tb)*j/NT;top[i].push(P(r,t,rampH(t)));bot[i].push(P(r,t,0))}}
  const Y=[.97,.75,.13],K=[.08,.09,.16];
  for(let i=0;i<NR;i++)for(let j=0;j<NT;j++){f.push([top[i][j],top[i][j+1],top[i+1][j+1],top[i+1][j]]);col.push(j===NT-1&&i%2===0?K:Y)}
  for(let j=0;j<NT;j++){f.push([bot[0][j],bot[0][j+1],top[0][j+1],top[0][j]]);col.push(Y);f.push([bot[NR][j],top[NR][j],top[NR][j+1],bot[NR][j+1]]);col.push(Y)}
  for(let i=0;i<NR;i++){f.push([bot[i][NT],bot[i+1][NT],top[i+1][NT],top[i][NT]]);col.push(i%2?Y:K)}
  const pos=[],cc=[];f.forEach((fc,k)=>{const Pp=fc.map(i=>v[i]);const tr=Pp.length===4?[[0,1,2],[0,2,3]]:[[0,1,2]];tr.forEach(t=>t.forEach(j=>{pos.push(...Pp[j]);cc.push(...col[k])}))});
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.setAttribute('color',new THREE.Float32BufferAttribute(cc,3));g.computeVertexNormals();
  const rm=new THREE.Mesh(g,new THREE.MeshStandardMaterial({vertexColors:true,roughness:.7,side:THREE.DoubleSide,flatShading:true,polygonOffset:true,polygonOffsetFactor:1}));
  // aristas: bordes de los quads, curvos como la retícula del suelo
  const ln=[];f.forEach(fc=>{for(let k=0;k<fc.length;k++){const A=v[fc[k]],B2=v[fc[(k+1)%fc.length]];ln.push(...A,...B2)}});rm.add(wireLines(ln));
  rm.position.y=.02;scene.add(rm)}
function groundH(x,z){const r=Math.hypot(x,z),t=Math.atan2(x,z);if(r>RAMP.r0&&r<RAMP.r1&&t>RAMP.ta&&t<RAMP.tb)return rampH(t);return 0}
// inclinación de la rampa en la dirección en que avanza el triciclo
function rampPitch(x,z,h){const t=Math.atan2(x,z),r=Math.hypot(x,z),up=Math.atan2(-Math.cos(t),Math.sin(t));return Math.atan2(RAMP.H,r*(RAMP.tb-RAMP.ta))*Math.cos(h-up)}"""
s = s[:a] + new + s[b:]
old = "const slope=gh>0&&!S.air?Math.atan2(RAMP.H,RAMP.L)*Math.cos(S.mh-RAMP.a):0;"
assert old in s
s = s.replace(old, "const slope=gh>0&&!S.air?rampPitch(S.x,S.z,S.mh):0;")
s = s.replace("<div><b>RAMPA</b>En la plaza hay una rampa amarilla: tómala a toda velocidad para saltar.</div>",
              "<div><b>RAMPA</b>En la plaza hay una rampa amarilla curva que sigue el círculo del piso: recórrela a toda velocidad para saltar.</div>")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
