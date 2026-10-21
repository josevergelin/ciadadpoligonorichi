// Cielo gris de viewport de Maya + planeta de quads
const sky=new THREE.Mesh(new THREE.SphereGeometry(1000,32,16),new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,
  vertexShader:'varying vec3 vP;void main(){vP=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:'varying vec3 vP;void main(){float h=vP.y;vec3 hor=vec3(.40,.405,.42);vec3 top=vec3(.25,.255,.27);vec3 c=mix(hor,top,smoothstep(0.,.8,h));gl_FragColor=vec4(c,1.);}'}));
scene.add(sky);
function indexedGeo(m,scale=1,off=[0,0,0]){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(m.v.flatMap(p=>[p[0]*scale+off[0],p[1]*scale+off[1],p[2]*scale+off[2]]),3));
  const idx=[];m.f.forEach(f=>{for(let j=1;j<f.length-1;j++)idx.push(f[0],f[j],f[j+1])});g.setIndex(idx);g.computeVertexNormals();return g}
function lineArr(m,scale=1,off=[0,0,0]){const p=[];for(const e of buildEdges(m).values())for(const v of[m.v[e.a],m.v[e.b]])p.push(v[0]*scale+off[0],v[1]*scale+off[1],v[2]*scale+off[2]);return p}
const quadSphere=(()=>{let s=subdivide(subdivide(PRESETS.cube3()));s.v=s.v.map(p=>norm(p));return s})();
const halfSphere=(()=>compact({v:quadSphere.v,f:quadSphere.f.filter(f=>f.every(i=>quadSphere.v[i][1]>-1e-6))}))();
const planet=new THREE.Group();
{const pm=new THREE.Mesh(indexedGeo(quadSphere,70),new THREE.MeshStandardMaterial({color:0xcfd1d4,roughness:.9,fog:false,polygonOffset:true,polygonOffsetFactor:1}));
 const pw=wireLines(lineArr(quadSphere,70.2),new THREE.LineBasicMaterial({color:0x2a2b2f,fog:false}));
 const tg=new THREE.TorusGeometry(115,5,6,72);const tr=new THREE.Mesh(tg,new THREE.MeshStandardMaterial({color:0xbfc2c6,fog:false,polygonOffset:true,polygonOffsetFactor:1}));
 tr.add(wireLines(quadEdges(tg),new THREE.LineBasicMaterial({color:0x2a2b2f,fog:false})));tr.rotation.x=1.25;planet.add(pm,pw,tr)}
planet.position.set(-420,300,-700);sky.add(planet);

// Suelo, retícula y vías
const ground=new THREE.Mesh(new THREE.PlaneGeometry(1400,1400),new THREE.MeshStandardMaterial({color:0x7c7f84,roughness:.95}));ground.rotation.x=-Math.PI/2;scene.add(ground);
const grid=new THREE.GridHelper(1400,350,0x3a3c40,0x4a4c51);grid.position.y=.03;grid.material.transparent=true;grid.material.opacity=.6;scene.add(grid);
const flat=(geo,color,y,op)=>{const m=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color,transparent:op!==undefined,opacity:op??1,side:THREE.DoubleSide}));m.rotation.x=-Math.PI/2;m.position.y=y;scene.add(m);return m};
flat(new THREE.CircleGeometry(54,64),0x8d9095,.05);
flat(new THREE.RingGeometry(53,54.2,96),0xf7c948,.07,.95);
flat(new THREE.RingGeometry(56,70,96),0x4a4c51,.06);
flat(new THREE.RingGeometry(62.6,63.4,96),0xeeeeee,.08,.8);
flat(new THREE.RingGeometry(150,164,128),0x4a4c51,.06);
flat(new THREE.RingGeometry(156.6,157.4,128),0xeeeeee,.08,.8);
// Retícula radial del plaza (una malla de quads vista desde arriba)
{const pl=[];for(let i=1;i<=6;i++){const r=i*9;for(let k=0;k<24;k++){const a1=k/24*Math.PI*2,a2=(k+1)/24*Math.PI*2;pl.push(Math.sin(a1)*r,.09,Math.cos(a1)*r,Math.sin(a2)*r,.09,Math.cos(a2)*r)}}
 for(let k=0;k<24;k++){const a=k/24*Math.PI*2;pl.push(Math.sin(a)*9,.09,Math.cos(a)*9,Math.sin(a)*54,.09,Math.cos(a)*54)}scene.add(wireLines(pl,new THREE.LineBasicMaterial({color:0x2e3034})))}
const AVE=[];for(let k=0;k<6;k++){const a=(k*60+30)*Math.PI/180;AVE.push(a);
  const road=new THREE.Mesh(new THREE.PlaneGeometry(14,400),new THREE.MeshBasicMaterial({color:0x4a4c51}));road.rotation.x=-Math.PI/2;road.rotation.z=-a;
  road.position.set(Math.sin(a)*(70+200),.055,Math.cos(a)*(70+200));scene.add(road);
  for(let d=76;d<470;d+=9){const s=new THREE.Mesh(new THREE.PlaneGeometry(.5,4),new THREE.MeshBasicMaterial({color:0xeeeeee,transparent:true,opacity:.85}));s.rotation.x=-Math.PI/2;s.rotation.z=-a;s.position.set(Math.sin(a)*d,.08,Math.cos(a)*d);scene.add(s)}}

/* Torres: cajas, cilindros y cajas suavizadas con Catmull-Clark, todas con su malla visible */
const colliders=[];let seed=12345;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
function nearAvenue(x,z,pad){for(const a of AVE){const dx=Math.sin(a),dz=Math.cos(a);const along=x*dx+z*dz;if(along<0)continue;if(Math.abs(x*dz-z*dx)<pad)return true}return false}
const lin=(a,b,step,sup)=>{const n=Math.max(1,Math.round((b-a-2*sup)/step));const o=[a,a+sup];for(let i=1;i<n;i++)o.push(a+sup+(b-a-2*sup)*i/n);o.push(b-sup,b);return o};
const roundTower=(w,h,d)=>subdivide(boxGrid([lin(-w/2,w/2,3,1.1),lin(0,h,3.5,1.1),lin(-d/2,d/2,3,1.1)]));
for(let gx=-264;gx<=264;gx+=24)for(let gz=-264;gz<=264;gz+=24){
  const x=gx+(rnd()-.5)*5,z=gz+(rnd()-.5)*5,r=Math.hypot(x,z);if(r<112||r>330)continue;if(Math.abs(r-157)<17)continue;
  const w=8+rnd()*6,d=8+rnd()*6;if(nearAvenue(x,z,10+Math.max(w,d)/2))continue;
  const h=14+rnd()*30+Math.max(0,(r-120))*.18*rnd()*1.6;const kind=rnd();
  if(kind<.55){const g=new THREE.BoxGeometry(w,h,d,Math.max(1,Math.round(w/2.4)),Math.max(1,Math.round(h/2.6)),Math.max(1,Math.round(d/2.4)));
    const m=new THREE.Mesh(g,CLAY);m.position.set(x,h/2,z);scene.add(m);bake(quadEdges(g),x,h/2,z);
    if(rnd()<.35){const t=new THREE.BoxGeometry(w*.55,6,d*.55,2,2,2);const tm=new THREE.Mesh(t,CLAY);tm.position.set(x,h+3,z);scene.add(tm);bake(quadEdges(t),x,h+3,z)}
    colliders.push({type:'box',minx:x-w/2,maxx:x+w/2,minz:z-d/2,maxz:z+d/2})}
  else if(kind<.78){const rr=Math.min(w,d)/2,g=new THREE.CylinderGeometry(rr*.82,rr,h,16,Math.max(2,Math.round(h/3)));
    const m=new THREE.Mesh(g,CLAY);m.position.set(x,h/2,z);scene.add(m);bake(quadEdges(g),x,h/2,z);colliders.push({type:'circle',x,z,r:rr})}
  else{const s=roundTower(w,h,d);scene.add(new THREE.Mesh(indexedGeo(s,1,[x,-.5,z]),CLAY));cityLines.push(...lineArr(s,1,[x,-.5,z]));
    colliders.push({type:'box',minx:x-w/2,maxx:x+w/2,minz:z-d/2,maxz:z+d/2})}}
scene.add(wireLines(cityLines));

/* Letreros pintados en el suelo frente a cada edificio */
function groundSign(t1,t2,color){const c=document.createElement('canvas');c.width=1024;c.height=512;const x=c.getContext('2d');
  const rr=(X,Y,W,H,r)=>{x.beginPath();x.moveTo(X+r,Y);x.arcTo(X+W,Y,X+W,Y+H,r);x.arcTo(X+W,Y+H,X,Y+H,r);x.arcTo(X,Y+H,X,Y,r);x.arcTo(X,Y,X+W,Y,r);x.closePath()};
  x.fillStyle='rgba(20,22,40,.9)';rr(12,12,1000,488,48);x.fill();x.lineWidth=14;x.strokeStyle=color;x.stroke();
  x.textAlign='center';x.save();x.scale(1,1.65);x.fillStyle=color;x.font='900 italic 150px Montserrat, Arial, sans-serif';x.fillText(t1,512,185,940);x.restore();
  x.fillStyle='#ffffff';x.font='800 64px Montserrat, Arial, sans-serif';x.fillText(t2.toUpperCase(),512,440,940);
  const tex=new THREE.CanvasTexture(c);if(R)tex.anisotropy=R.capabilities.getMaxAnisotropy();
  const m=new THREE.Mesh(new THREE.PlaneGeometry(26,13),new THREE.MeshBasicMaterial({map:tex,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2}));m.rotation.x=-Math.PI/2;return m}
function keyLabel(t,color){const c=document.createElement('canvas');c.width=256;c.height=256;const x=c.getContext('2d');x.fillStyle='#e9eaec';x.fillRect(0,0,256,256);x.fillStyle=color;x.textAlign='center';x.font='900 italic 110px Montserrat, Arial';x.fillText(t,128,165);
  return new THREE.Mesh(new THREE.PlaneGeometry(8,8),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c)}))}

/* Construcción de los edificios */
const spinners=[],pulses=[];
const accentMat=c=>new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:.35,roughness:.5,polygonOffset:true,polygonOffsetFactor:1});
function meshLines(m,scale,color){return wireLines(lineArr(m,scale),new THREE.LineBasicMaterial({color}))}
function meshPoints(m,scale,color,size=6){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(m.v.flatMap(p=>scl(p,scale)),3));return new THREE.Points(g,new THREE.PointsMaterial({color,size,sizeAttenuation:false}))}
function solid(m,scale,color,op){return new THREE.Mesh(indexedGeo(m,scale),new THREE.MeshStandardMaterial({color,transparent:op<1,opacity:op,roughness:.85,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:1,depthWrite:op>=1}))}
const clayW=(geo,pos)=>{const m=clayWire(geo);if(pos)m.position.set(...pos);return m};
const BUILDERS={
 componentes(g,c){g.add(clayW(new THREE.BoxGeometry(16,24,16,6,9,6),[0,12,0]));
   const top=new THREE.Group();top.position.y=36;const cube=PRESETS.cube3();top.add(solid(cube,6,0xe2e3e5,1),meshLines(cube,6.02,0x1d1e21),meshPoints(cube,6.05,c,9));g.add(top);spinners.push([top,.35])},
 herramientas(g,c){[[20,10,0],[14,9,10],[8.5,8,19]].forEach(([s,h,y])=>{const m=clayW(new THREE.CylinderGeometry(s/1.4,s/1.25,h,8,4),[0,y+h/2,0]);m.rotation.y=Math.PI/8;g.add(m)});
   const ar=new THREE.Group();const cone=clayWire(new THREE.ConeGeometry(3,5,4,2),accentMat(c));cone.position.y=4;
   const stem=clayWire(new THREE.BoxGeometry(1.6,4,1.6,1,2,1),accentMat(c));stem.position.y=.5;ar.add(cone,stem);ar.position.y=31;g.add(ar);spinners.push([ar,.8])},
 topologia(g,c){g.add(clayW(new THREE.CylinderGeometry(7,9,26,12,8),[0,13,0]));
   const sph=new THREE.Group();sph.position.y=38;sph.add(solid(quadSphere,9,0xe2e3e5,1),meshLines(quadSphere,9.03,c));g.add(sph);spinners.push([sph,.25])},
 atajos(g,c){g.add(clayW(new THREE.BoxGeometry(20,16,12,8,6,5),[0,8,0]));
   const key=new THREE.Group();key.add(clayW(new THREE.BoxGeometry(11,3,11,4,1,4)));const kl=keyLabel('F10',hex(c));kl.rotation.x=-Math.PI/2;kl.position.y=1.55;key.add(kl);
   key.position.y=19;key.rotation.x=-.25;g.add(key);spinners.push([key,.4])},
 flujo(g,c){[[9,8,0],[7.5,8,8.5],[6,8,17],[4.5,8,25.5]].forEach(([r,h,y],i)=>{g.add(clayW(new THREE.CylinderGeometry(r,r+.6,h,16,3),[0,y+h/2,0]));
   const ring=new THREE.Mesh(new THREE.TorusGeometry(r+1.4,.22,6,48),new THREE.MeshBasicMaterial({color:i%2?0xf7c948:c}));ring.rotation.x=Math.PI/2;ring.position.y=y+h;g.add(ring);pulses.push([ring,i])})},
 academia(g,c){g.add(clayW(new THREE.CylinderGeometry(13,14,6,24,2),[0,3,0]));
   const dome=new THREE.Group();dome.position.y=6;dome.add(solid(halfSphere,12,0xe2e3e5,1),meshLines(halfSphere,12.03,0x1d1e21));g.add(dome);
   const sp=new THREE.Mesh(new THREE.ConeGeometry(1,10,8),new THREE.MeshBasicMaterial({color:0xf7c948}));sp.position.y=23;g.add(sp)}};
const RB=90;
B.forEach((b,k)=>{const a=k*60*Math.PI/180;const x=Math.sin(a)*RB,z=Math.cos(a)*RB;const g=new THREE.Group();g.position.set(x,0,z);g.rotation.y=a+Math.PI;scene.add(g);
  const bc=b.color===0xffffff?0x0076d6:b.color;b.ui=hex(bc);
  g.add(clayW(new THREE.CylinderGeometry(15,15.5,.8,32,1),[0,.4,0]));
  const pr=new THREE.Mesh(new THREE.TorusGeometry(15.2,.22,6,64),new THREE.MeshBasicMaterial({color:bc}));pr.rotation.x=Math.PI/2;pr.position.y=.8;g.add(pr);
  BUILDERS[b.id](g,bc);
  // puerta: arco + anillo de entrada
  const arch=new THREE.Mesh(new THREE.TorusGeometry(4,.35,8,32,Math.PI),new THREE.MeshBasicMaterial({color:bc}));arch.position.set(0,0,9.5);g.add(arch);
  const door=new THREE.Mesh(new THREE.PlaneGeometry(7,4),new THREE.MeshBasicMaterial({color:bc,transparent:true,opacity:.45,side:THREE.DoubleSide}));door.position.set(0,2,9.4);g.add(door);
  const pad=new THREE.Mesh(new THREE.RingGeometry(3,4,40),new THREE.MeshBasicMaterial({color:bc,transparent:true,opacity:.9,side:THREE.DoubleSide}));pad.rotation.x=-Math.PI/2;pad.position.set(0,.12,19);g.add(pad);
  const beam=new THREE.Mesh(new THREE.CylinderGeometry(3.5,3.5,10,32,1,true),new THREE.MeshBasicMaterial({color:bc,transparent:true,opacity:.12,side:THREE.DoubleSide,depthWrite:false}));beam.position.set(0,5,19);g.add(beam);
  b.pad=pad;b.beam=beam;b.door=new THREE.Vector3(Math.sin(a)*(RB-19),0,Math.cos(a)*(RB-19));b.angle=a;b.group=g;
  colliders.push({type:'circle',x,z,r:15.3})});

// Holograma central: cubo de quads + marca
const holo=new THREE.Group();holo.position.y=26;const hc=PRESETS.cube3();holo.add(meshLines(hc,7,0xf7c948),meshPoints(hc,7,0x0076d6,8),solid(hc,7,0xffffff,.25));scene.add(holo);
scene.add(clayW(new THREE.CylinderGeometry(2,3,14,6,4),[0,7,0]));colliders.push({type:'circle',x:0,z:0,r:3.5});
let brand=null;

// Autos voladores (arcilla con malla visible)
const carGeo=new THREE.BoxGeometry(1.4,.7,3,2,1,3);
const cars=[];for(let i=0;i<34;i++){const g=new THREE.Group();const body=clayWire(carGeo);
  const tail=new THREE.Mesh(new THREE.BoxGeometry(1.5,.25,.2),new THREE.MeshBasicMaterial({color:i%3?0xd9363e:0xf7c948}));tail.position.z=-1.55;const head=new THREE.Mesh(new THREE.BoxGeometry(1.2,.2,.2),new THREE.MeshBasicMaterial({color:0x0076d6}));head.position.z=1.55;
  g.add(body,tail,head);scene.add(g);cars.push({g,r:80+Math.random()*220,h:22+Math.random()*50,w:(Math.random()<.5?-1:1)*(.04+Math.random()*.08),p:Math.random()*7})}

