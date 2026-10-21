/* ============ Salas interiores 3D: cada edificio es un salón circular con estaciones animadas ============ */
let mode='city',curHall=null,curB=null,hallNear=null;const HALLS={};
const ss=(a,b,x)=>{x=Math.min(1,Math.max(0,(x-a)/(b-a)));return x*x*(3-2*x)};
const cyc=(t,P)=>(((t%P)+P)%P)/P;
const vfind=(m,x,y,z)=>m.v.findIndex(p=>Math.abs(p[0]-x)<1e-4&&Math.abs(p[1]-y)<1e-4&&Math.abs(p[2]-z)<1e-4);
const CUBE3=PRESETS.cube3(),CUBE1=PRESETS.cube1(),TALL=boxGrid([[-1,0,1],[-1.5,1.5],[-1,0,1]]);
const TOPC=topFaces(CUBE3)[4];
const plain=m=>({v:m.v,f:m.f});
const SUBQ=[CUBE3,plain(subdivide(CUBE3))],SUBQ2=plain(subdivide(SUBQ[1]));SUBQ.push(SUBQ2);
const SUBT=[meshT,plain(subdivide(meshT))];SUBT.push(plain(subdivide(SUBT[1])));
const SUBN=[meshN,plain(subdivide(meshN))];SUBN.push(plain(subdivide(SUBN[1])));

/* --- Animaciones de herramientas (devuelven la malla del momento + lo que se resalta) --- */
function aExtrude(t){const u=cyc(t,4),d=1.1*ss(.15,.6,u)*(u<.92?1:0);const r=extrudeFaces(CUBE3,[TOPC],d);const hl=new Set(r.faces);for(let i=r.mesh.f.length-r.sides;i<r.mesh.f.length;i++)hl.add(i);return{m:r.mesh,hl}}
function bevelBox(f,segs){f=Math.max(f,.002);const prof=[[-1,-1],[1,-1]];for(let i=0;i<=segs;i++){const a=i/segs*Math.PI/2;prof.push([1-f+f*Math.cos(a),1-f+f*Math.sin(a)])}prof.push([-1,1]);
  const n=prof.length,v=[];prof.forEach(([z,y])=>v.push([-1.2,y,z]));prof.forEach(([z,y])=>v.push([1.2,y,z]));
  const F=[],hl=new Set();for(let i=0;i<n;i++){const j=(i+1)%n;F.push([i,j,n+j,n+i]);if(i>=2&&i<2+segs)hl.add(F.length-1)}
  F.push([...Array(n).keys()].reverse());F.push([...Array(n).keys()].map(i=>n+i));return{m:{v,f:F},hl}}
function aBevel(t){const u=cyc(t,4.5),f=.6*ss(.15,.6,u)*(u<.92?1:0);const r=bevelBox(f,3);const o={m:r.m,hl:r.hl};if(u<.15||u>.92)o.hlEdges=[[[-1.2,1,1],[1.2,1,1]]];return o}
const TALL_E=[vfind(TALL,1,-1.5,1),vfind(TALL,1,1.5,1)];
function aLoop(t){const u=cyc(t,4);if(u<.12||u>.94)return{m:TALL,hlEdges:[[TALL.v[TALL_E[0]],TALL.v[TALL_E[1]]]]};const tt=.12+.38*ss(.12,.6,u);const r=insertEdgeLoop(TALL,TALL_E[0],TALL_E[1],tt);
  return{m:r.mesh,hlEdges:r.newEdges.map(([x,y])=>[r.mesh.v[x],r.mesh.v[y]])}}
function aOffset(t){const u=cyc(t,4.5),w=Math.max(.004,.3*ss(.2,.65,u)*(u<.93?1:0));const[a,b]=TALL_E;const r1=insertEdgeLoop(TALL,a,b,.5-w);const m0=TALL.v.length;
  const r2=insertEdgeLoop(r1.mesh,m0,b,(2*w)/(.5+w));const M=r2.mesh;return{m:M,hlEdges:[...r1.newEdges.map(([x,y])=>[M.v[x],M.v[y]]),...r2.newEdges.map(([x,y])=>[M.v[x],M.v[y]])]}}
const BR=(()=>{const L=boxGrid([[-3,-1],[-1,1],[-1,1]]),Rm=boxGrid([[1,3],[-1,1],[-1,1]]);
  const Lf=L.f.filter(f=>!f.every(i=>Math.abs(L.v[i][0]+1)<1e-6)),Rf=Rm.f.filter(f=>!f.every(i=>Math.abs(Rm.v[i][0]-1)<1e-6));
  const m={v:[...L.v,...Rm.v],f:[...Lf,...Rf.map(fc=>fc.map(i=>i+L.v.length))]};const ring=[[-1,-1],[1,-1],[1,1],[-1,1]];
  return{m,ring,Lr:ring.map(([y,z])=>vfind(m,-1,y,z)),Rr:ring.map(([y,z])=>vfind(m,1,y,z))}})();
function aBridge(t){const u=cyc(t,4.5),p=ss(.15,.7,u)*(u<.93?1:0);const v=BR.m.v.slice(),f=BR.m.f.slice(),hl=new Set();let prev=BR.Lr;
  const out={hl};if(u<.15||u>.93)out.hlEdges=[BR.Lr,BR.Rr].flatMap(r=>r.map((a,i)=>[v[a],v[r[(i+1)%4]]]));
  if(p>.001){for(let k=1;k<=3;k++){const x=-1+2*p*k/3;const cur=BR.ring.map(([y,z])=>{v.push([x,y,z]);return v.length-1});for(let s2=0;s2<4;s2++){f.push([prev[s2],prev[(s2+1)%4],cur[(s2+1)%4],cur[s2]]);hl.add(f.length-1)}prev=cur}}
  out.m={v,f};return out}
const MC_L=[[[-1/3,1.01,-1],[-1/3,1.01,1]],[[1/3,1.01,-1],[1/3,1.01,1]],[[-1,1.01,-1/3],[1,1.01,-1/3]],[[-1,1.01,1/3],[1,1.01,1/3]]];
function aMulti(t){const u=cyc(t,5.5);if(u>.8&&u<.97)return{m:meshQ,hl:new Set(topFaces(meshQ))};const out={m:meshN,topo:true,hlEdges:[],pts2:[]};const p=ss(.12,.78,u)*4;
  MC_L.forEach(([A,Bq],i)=>{const k=Math.max(0,Math.min(1,p-i));if(k>0){const E=lerp(A,Bq,k);out.hlEdges.push([A,E]);out.pts2.push(A,E)}});return out}
const WA=vfind(CUBE3,1/3,1,1/3),WB=vfind(CUBE3,1/3,1,-1/3);
function aWeld(t){const u=cyc(t,4);const M=cloneMesh(CUBE3);if(u>.7&&u<.95){M.v[WA]=M.v[WB].slice();return{m:mergeVerts(M,[WB,WA]),topo:true}}
  M.v[WA]=lerp(CUBE3.v[WA],CUBE3.v[WB],ss(.15,.65,u));return{m:M,pts2:[M.v[WA],M.v[WB]],hlEdges:[[M.v[WA],M.v[WB]]]}}
function aPoke(t){const u=cyc(t,4);if(u<.15||u>.94)return{m:CUBE3,hl:new Set([TOPC])};const M=pokeFaces(CUBE3,[TOPC]);const c=M.v.length-1;M.v[c]=add(M.v[c],[0,.9*ss(.3,.65,u),0]);
  return{m:M,hl:new Set([TOPC,TOPC+1,TOPC+2,TOPC+3]),hlColor:0xf2b630,pts2:[M.v[c]]}}
const OPEN={v:meshN.v,f:meshN.f.slice(0,-1)},RING=meshN.f[meshN.f.length-1],RC=avg(RING.map(i=>meshN.v[i]));
function aFill(t){const u=cyc(t,4.5),p=ss(.2,.65,u)*(u<.93?1:0);const out={m:OPEN,hlEdges:RING.map((a,i)=>[meshN.v[a],meshN.v[RING[(i+1)%RING.length]]])};
  if(p>.01){const v=OPEN.v.slice();const ids=RING.map(i=>{v.push(lerp(RC,meshN.v[i],p));return v.length-1});out.m={v,f:[...OPEN.f,ids]};out.hl=new Set([OPEN.f.length]);out.hlColor=0xe5484d}return out}
const smoothCycle=(arr,period=6)=>t=>{const l=Math.floor(cyc(t,period)*3);return{m:arr[l],smooth:l>0,topo:true,label:'Nivel '+l}};
const HALF=compact({v:CUBE3.v,f:CUBE3.f.filter(f=>f.every(i=>CUBE3.v[i][0]<=-1/3+1e-6))});
function aMirror(t){const u=cyc(t,4),p=ss(.15,.6,u)*(u<.93?1:0),n=HALF.v.length,ax=-1/3;
  const v=[...HALF.v,...HALF.v.map(q2=>[ax+(ax-q2[0])*p,q2[1],q2[2]])],f=[...HALF.f,...HALF.f.map(fc=>fc.map(i=>i+n).reverse())],hl=new Set();for(let i=HALF.f.length;i<f.length;i++)hl.add(i);
  return{m:{v,f},hl,hlEdges:[[[ax,-1.5,0],[ax,1.5,0]],[[ax,0,-1.5],[ax,0,1.5]]]}}
/* --- Componentes --- */
const VK=vfind(CUBE3,1,1,1);
function aVertex(t){const M=cloneMesh(CUBE3);M.v[VK]=[1,1+.45*(1+Math.sin(t*2)),1];return{m:M,pts:M.v,pts2:[M.v[VK]]}}
const LOOPE=[...edgeLoop(CUBE3,vfind(CUBE3,1,1/3,-1/3),vfind(CUBE3,1,1/3,1/3))];
function aEdge(t){const k=Math.floor(cyc(t,4)*(LOOPE.length+3));return{m:CUBE3,hlEdges:LOOPE.slice(0,k).map(key=>{const[a,b]=key.split('_').map(Number);return[CUBE3.v[a],CUBE3.v[b]]})}}
function aFace(t){return{m:CUBE3,hl:new Set([Math.floor(t*2.5)%CUBE3.f.length])}}
function aNormal(){return{m:CUBE1,hlEdges:CUBE1.f.map(f=>{const P=f.map(i=>CUBE1.v[i]),c=avg(P),n=newell(P);return[c,add(c,scl(n,.9))]}),pts2:CUBE1.f.map(f=>{const P=f.map(i=>CUBE1.v[i]);return add(avg(P),scl(newell(P),.9))})}}
const ALLE=[...buildEdges(CUBE3).values()].map(e=>[CUBE3.v[e.a],CUBE3.v[e.b]]);
function aObject(){return{m:CUBE3,hlEdges:ALLE,hlColor:0x2ecc71}}
/* --- Topología --- */
const NL=(()=>{const a=vfind(meshN,1/3,-1/3,1),b=vfind(meshN,1/3,1/3,1);return[...edgeLoop(meshN,a,b)]})();
function aLoopStop(t){const k=Math.floor(cyc(t,4)*(NL.length+4));return{m:meshN,topo:true,hlEdges:NL.slice(0,k).map(key=>{const[a,b]=key.split('_').map(Number);return[meshN.v[a],meshN.v[b]]})}}
const POLES=(()=>{const v=[],f=[],c=[];[[3,-1.4],[5,1.4]].forEach(([n,ox])=>{const ci=v.length;v.push([ox,.35,0]);c.push(ci);const s=[],o=[];
  for(let i=0;i<n;i++){const a=i/n*Math.PI*2;v.push([ox+Math.cos(a)*.6,.2,Math.sin(a)*.6]);s.push(v.length-1)}
  for(let i=0;i<n;i++){const a=(i+.5)/n*Math.PI*2;v.push([ox+Math.cos(a)*1.15,0,Math.sin(a)*1.15]);o.push(v.length-1)}
  for(let i=0;i<n;i++)f.push([ci,s[i],o[i],s[(i+1)%n]])});return{m:{v,f},c}})();
function aPoles(){return{m:POLES.m,pts2:POLES.c.map(i=>POLES.m.v[i])}}
/* --- Flujo --- */
const REF=(()=>{const v=CUBE1.v.slice(),f=CUBE1.f.slice(),hl=new Set();const q4=(a,b,c,d)=>{const n=v.length;v.push(a,b,c,d);f.push([n,n+1,n+2,n+3]);hl.add(f.length-1)};
  q4([-1.8,-1.4,-1.4],[-1.8,-1.4,1.4],[-1.8,1.4,1.4],[-1.8,1.4,-1.4]);q4([-1.4,-1.4,-1.8],[1.4,-1.4,-1.8],[1.4,1.4,-1.8],[-1.4,1.4,-1.8]);return{m:{v,f},hl,hlColor:0x9fd0ff}})();
function aRef(){return REF}
function aBlock(t){const s=1+.06*Math.sin(t*2);return{m:{v:CUBE1.v.map(p=>[p[0]*s,p[1],p[2]*s]),f:CUBE1.f}}}
function aDeliver(){return{m:SUBQ2,smooth:true,hlEdges:[[[0,0,0],[1.6,0,0]],[[0,0,0],[0,1.6,0]],[[0,0,0],[0,0,1.6]]],hlColor:0x56a8ff}}

/* --- Visualización de una malla animada --- */
const HMAT=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.8,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1});
const HMAT_S=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.55,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1});
const P_SEL=new THREE.PointsMaterial({color:0xffd21f,size:9,sizeAttenuation:false}),P_VTX=new THREE.PointsMaterial({color:0xc23bd6,size:7,sizeAttenuation:false});
const BASEC=[.89,.89,.9],TRIC=[.95,.71,.19],NGC=[.9,.28,.3];
function dispSet(D,out){D.parts.forEach(o=>{D.g.remove(o);o.geometry.dispose()});D.parts=[];
  const m=out.m,hl=out.hl||new Set(),hc=new THREE.Color(out.hlColor||D.accent),hca=[hc.r,hc.g,hc.b];
  const colOf=(f,fi)=>hl.has(fi)?hca:out.topo?(f.length===3?TRIC:f.length>4?NGC:BASEC):BASEC;
  let geo;
  if(out.smooth){const ig=indexedGeo(m);geo=ig.toNonIndexed();ig.dispose();const cols=[];m.f.forEach((f,fi)=>{const c=colOf(f,fi);for(let j=1;j<f.length-1;j++)for(let k=0;k<3;k++)cols.push(...c)});geo.setAttribute('color',new THREE.Float32BufferAttribute(cols,3))}
  else{const pos=[],cols=[];m.f.forEach((f,fi)=>{const P=f.map(i=>m.v[i]),c=colOf(f,fi);triPoly(P).forEach(tr=>tr.forEach(j=>{pos.push(...P[j]);cols.push(...c)}))});
    geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.setAttribute('color',new THREE.Float32BufferAttribute(cols,3));geo.computeVertexNormals()}
  const add2=o=>{D.g.add(o);D.parts.push(o)};
  add2(new THREE.Mesh(geo,out.smooth?HMAT_S:HMAT));add2(wireLines(lineArr(m)));
  if(out.hlEdges&&out.hlEdges.length){const p=[];out.hlEdges.forEach(([a,b])=>p.push(...a,...b));if(!D.lm||D.lmc!==hc.getHex()){D.lm=new THREE.LineBasicMaterial({color:hc,depthTest:false,transparent:true});D.lmc=hc.getHex()}
    const ls=wireLines(p,D.lm);ls.renderOrder=3;add2(ls)}
  const pts=(arr,mat)=>{if(!arr||!arr.length)return;const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(arr.flat(),3));const o=new THREE.Points(g,mat);o.renderOrder=4;add2(o)};
  pts(out.pts,P_VTX);pts(out.pts2,P_SEL)}

/* --- Holograma de teclado para el edificio Atajos --- */
const KB_ROWS=[[['esc','Esc',1],.5,'f1','f2','f3','f4',.5,'f5','f6','f7','f8',.5,'f9','f10','f11','f12'],
  [['`','`'],'1','2','3','4','5','6','7','8','9','0',['-','-'],['=','='],['bksp','⌫',2]],
  [['tab','Tab',1.5],'q','w','e','r','t','y','u','i','o','p',['[','['],[']',']'],['\\','\\',1.5]],
  [['caps','Bloq',1.75],'a','s','d','f','g','h','j','k','l',[';',';'],["'","'"],['enter','Enter',2.25]],
  [['lshift','Shift',2.25],'z','x','c','v','b','n','m',[',',',  <'],['.','.  >'],['/','/'],['rshift','Shift',2.75]],
  [['lctrl','Ctrl',1.5],['win','Win',1.25],['lalt','Alt',1.25],['space','Espacio',6.25],['ralt','Alt',1.25],['rctrl','Ctrl',1.5]]];
const KB=(()=>{const keys=[];KB_ROWS.forEach((row,r)=>{let x=0;const y=r===0?0:r+.35;row.forEach(k=>{if(typeof k==='number'){x+=k;return}
    const [id,lab,w]=typeof k==='string'?[k,k.toUpperCase(),1]:[k[0],k[1],k[2]||1];keys.push({id,lab,x,y,w});x+=w})});
  [['ins','Ins',15.6,1.35],['home','Inicio',16.6,1.35],['del','Supr',15.6,2.35]].forEach(([id,lab,x,y])=>keys.push({id,lab,x,y,w:1}));return{keys,W:17.6,H:6.35}})();
const KCAT={sel:['Selección y componentes','#56A8FF'],tr:['Transformar y snap','#B08CFF'],mod:['Modelado y edición','#F7C948'],vis:['Vista y navegación','#3CE0C0'],file:['Archivo y animación','#FF6B8A']};
const SHORT=[
 ['sel',['f8'],'F8','Objeto / componentes','Alterna entre seleccionar el objeto y sus componentes.'],
 ['sel',['f9'],'F9','Modo vértice','Selecciona vértices: puntos de la malla.'],
 ['sel',['f10'],'F10','Modo arista','Selecciona aristas. Doble clic toma el edge loop.'],
 ['sel',['f11'],'F11','Modo cara','Selecciona caras para extruir, biselar o borrar.'],
 ['sel',['f12'],'F12','Modo UV','Selecciona UVs para el mapeado de texturas.'],
 ['sel',['q'],'Q','Herramienta de selección','Selecciona sin mover nada.'],
 ['sel',['b'],'B','Soft Selection','Activa la selección suave con caída gradual.'],
 ['sel',['lshift','.'],'Shift + .  ( > )','Crecer selección','Añade el anillo de componentes vecinos.'],
 ['sel',['lshift',','],'Shift + ,  ( < )','Reducir selección','Quita el borde de la selección.'],
 ['sel',['lshift'],'Shift + clic derecho','Marking menu poligonal','Menú radial con Extrude, Bevel, Multi-Cut y más.'],
 ['sel',['lctrl'],'Ctrl + clic derecho','Convertir selección','Pasa la selección a vértices, aristas o caras.'],
 ['tr',['w'],'W','Mover','Herramienta de traslación.'],
 ['tr',['e'],'E','Rotar','Herramienta de rotación.'],
 ['tr',['r'],'R','Escalar','Herramienta de escala.'],
 ['tr',['t'],'T','Mostrar manipulador','Muestra el manipulador de la herramienta activa.'],
 ['tr',['y'],'Y','Última herramienta','Repite la última herramienta usada.'],
 ['tr',['d'],'D (mantener)','Editar pivote','Mueve el pivote mientras mantienes D.'],
 ['tr',['ins'],'Insert','Modo pivote','Activa o desactiva la edición del pivote.'],
 ['tr',['x'],'X (mantener)','Snap a la cuadrícula','Ajusta el movimiento a la grilla.'],
 ['tr',['c'],'C (mantener)','Snap a curva','Ajusta el movimiento a una curva.'],
 ['tr',['v'],'V (mantener)','Snap a punto','Ajusta el movimiento a vértices.'],
 ['mod',['lctrl','e'],'Ctrl + E','Extrude','Saca caras, aristas o vértices creando nuevas caras.'],
 ['mod',['lctrl','b'],'Ctrl + B','Bevel','Redondea o achaflana aristas.'],
 ['mod',['lctrl','del'],'Ctrl + Supr','Delete Edge/Vertex','Borra aristas y sus vértices sueltos.'],
 ['mod',['lctrl','d'],'Ctrl + D','Duplicar','Copia el objeto seleccionado.'],
 ['mod',['lshift','d'],'Shift + D','Duplicar con transformación','Duplica y repite el último movimiento.'],
 ['mod',['lctrl','g'],'Ctrl + G','Agrupar','Agrupa los objetos seleccionados.'],
 ['mod',['p'],'P','Emparentar','Hace al último seleccionado padre de los demás.'],
 ['mod',['lshift','p'],'Shift + P','Desemparentar','Quita la relación padre-hijo.'],
 ['mod',['g'],'G','Repetir comando','Repite el último comando ejecutado.'],
 ['mod',['lalt','lshift','d'],'Alt + Shift + D','Borrar historial','Limpia el historial de construcción del objeto.'],
 ['vis',['1'],'1','Malla original','Vista sin suavizar.'],
 ['vis',['2'],'2','Jaula + suavizado','Muestra la caja de control sobre la vista suavizada.'],
 ['vis',['3'],'3','Vista suavizada','Previsualiza el suavizado Catmull-Clark.'],
 ['vis',['4'],'4','Wireframe','Solo aristas.'],
 ['vis',['5'],'5','Sombreado','Superficies sombreadas.'],
 ['vis',['6'],'6','Texturas','Sombreado con texturas.'],
 ['vis',['7'],'7','Luces','Usa las luces de la escena.'],
 ['vis',['f'],'F','Encuadrar selección','Centra la cámara en lo seleccionado.'],
 ['vis',['a'],'A','Encuadrar todo','Muestra toda la escena.'],
 ['vis',['space'],'Espacio (toque)','1 o 4 vistas','Alterna entre una vista y las cuatro.'],
 ['vis',['lalt'],'Alt + arrastrar','Navegar','Izq.: orbitar · Medio: desplazar · Der.: zoom.'],
 ['vis',['lctrl','h'],'Ctrl + H','Ocultar','Oculta la selección.'],
 ['vis',['lctrl','lshift','h'],'Ctrl + Shift + H','Mostrar lo oculto','Vuelve a mostrar lo último que ocultaste.'],
 ['vis',['f2'],'F2','Menús Modeling','Cambia al conjunto de menús de modelado.'],
 ['vis',['f3'],'F3','Menús Rigging','Conjunto de menús de rigging.'],
 ['vis',['f4'],'F4','Menús Animation','Conjunto de menús de animación.'],
 ['vis',['f5'],'F5','Menús FX','Conjunto de menús de efectos.'],
 ['vis',['f6'],'F6','Menús Rendering','Conjunto de menús de render.'],
 ['file',['lctrl','z'],'Ctrl + Z','Deshacer','Deshace la última acción.'],
 ['file',['lshift','z'],'Shift + Z','Rehacer','Rehace lo deshecho.'],
 ['file',['lctrl','s'],'Ctrl + S','Guardar','Guarda la escena.'],
 ['file',['lctrl','n'],'Ctrl + N','Nueva escena','Crea una escena vacía.'],
 ['file',['lctrl','o'],'Ctrl + O','Abrir','Abre una escena.'],
 ['file',['lctrl','a'],'Ctrl + A','Attribute Editor','Muestra u oculta el editor de atributos.'],
 ['file',['s'],'S','Keyframe','Inserta una clave de animación.']];
function drawKeyboard(x,W,H,hi,opt={}){const u=W/(KB.W+.6),ox=u*.3,oy=(H-KB.H*u)/2;x.clearRect(0,0,W,H);if(opt.bg){x.fillStyle=opt.bg;x.fillRect(0,0,W,H)}
  const rr=(X,Y,w,h,r)=>{x.beginPath();x.moveTo(X+r,Y);x.arcTo(X+w,Y,X+w,Y+h,r);x.arcTo(X+w,Y+h,X,Y+h,r);x.arcTo(X,Y+h,X,Y,r);x.arcTo(X,Y,X+w,Y,r);x.closePath()};
  KB.keys.forEach(k=>{const X=ox+k.x*u+u*.06,Y=oy+k.y*u+u*.06,w=k.w*u-u*.12,h=u*.88,c=hi.get(k.id);rr(X,Y,w,h,u*.14);
    if(c){x.fillStyle=c;x.fill()}else if(opt.keyFill){x.fillStyle=opt.keyFill;x.fill()}x.lineWidth=Math.max(1.5,u*.035);x.strokeStyle=c||opt.stroke||'rgba(140,220,255,.85)';x.stroke();
    x.fillStyle=c?'#0b1240':(opt.text||'#d8f4ff');x.font=`800 ${Math.round(u*(k.lab.length>3?.24:.36))}px Montserrat, Arial, sans-serif`;x.textAlign='center';x.textBaseline='middle';x.fillText(k.lab,X+w/2,Y+h/2,w-u*.1)})}
const shortHi=sc=>{const m=new Map();const col=KCAT[sc[0]][1];sc[1].forEach(id=>m.set(id,col));return m};

/* --- Estaciones de cada edificio --- */
const TK=id=>TOOLS.flatMap(c=>c.items).find(x=>x.id===id);
const toolSt=(id,anim,extra={})=>{const t=TK(id);return Object.assign({name:t.n,sub:t.menu.split('>').pop().trim(),desc:t.d,key:t.key,anim,tool:id},extra)};
const TERM=(name,sub,desc)=>({name,sub,desc,terminal:true});
const STN={
 componentes:[{name:'Vértice',sub:'F9',desc:'Punto con coordenadas X, Y, Z. Moverlo cambia la forma de todas las caras que lo comparten.',key:'F9',anim:aVertex,anat:'vertex'},
  {name:'Arista',sub:'F10',desc:'Línea entre dos vértices. Las aristas en fila forman un edge loop que recorre el modelo.',key:'F10',anim:aEdge,anat:'edge'},
  {name:'Cara',sub:'F11',desc:'Superficie cerrada por aristas: triángulo (3), quad (4) o N-gon (5+). Aquí se recorren las 54 caras del cubo.',key:'F11',anim:aFace,anat:'face'},
  {name:'Normal',sub:'Display > Polygons',desc:'Flecha perpendicular a cada cara que indica hacia dónde mira. Define el sombreado y el lado visible.',key:'Display > Polygons > Face Normals',anim:aNormal,anat:'face'},
  {name:'Objeto',sub:'F8',desc:'La malla completa como una sola pieza con su pivote. En Maya la selección de objeto se ve en verde.',key:'F8',anim:aObject,anat:'object'},
  TERM('Práctica','Visor de componentes','Abre el visor interactivo para seleccionar vértices, aristas y caras.')],
 herramientas:[toolSt('extrude',aExtrude),toolSt('bevel',aBevel),toolSt('loop',aLoop),toolSt('offset',aOffset),toolSt('bridge',aBridge,{scale:1.25}),
  toolSt('multicut',aMulti),toolSt('targetweld',aWeld),toolSt('poke',aPoke),toolSt('fillhole',aFill),toolSt('smooth',smoothCycle(SUBQ)),toolSt('mirror2',aMirror),
  TERM('Taller','Modeling Toolkit','Abre el taller práctico y la ficha completa de todas las herramientas.')],
 topologia:[{name:'Quads',sub:'Suavizado limpio',desc:'Con solo quads el suavizado es uniforme y simétrico, y los loops recorren todo el modelo.',key:'3',anim:smoothCycle(SUBQ)},
  {name:'Triángulos',sub:'Bultos y pellizcos',desc:'Las diagonales de los triángulos generan bultos asimétricos al suavizar.',key:'Mesh > Quadrangulate',anim:smoothCycle(SUBT)},
  {name:'N-gon',sub:'Polo de 12 aristas',desc:'Al subdividir un N-gon aparece un polo con muchas aristas: la superficie se aplana en estrella.',key:'Mesh > Cleanup',anim:smoothCycle(SUBN)},
  {name:'Loop detenido',sub:'Edge loop',desc:'El edge loop avanza cruzando quads y se detiene al llegar al N-gon rojo.',key:'Doble clic en una arista',anim:aLoopStop},
  {name:'Polos',sub:'3 y 5 aristas',desc:'Vértices con 3 o 5 aristas. Son necesarios para cambiar el flujo; colócalos en zonas planas.',key:'—',anim:aPoles},
  TERM('Comparador','Quads vs N-gons','Abre la comparación interactiva con niveles de suavizado.')],
 atajos:[{name:'Teclado holográfico',sub:'Pulsa E para el siguiente',desc:'El holograma recorre los atajos de Maya. Pulsa E sobre este anillo para pasar al siguiente.',key:'—',holo:true},
  ...Object.keys(KCAT).map(c=>({name:KCAT[c][0],sub:SHORT.filter(s=>s[0]===c).length+' atajos',desc:'Panel de la infografía con los atajos de esta categoría.',key:'—',panel:c})),
  TERM('Reto de atajos','Juego e infografía','Abre la infografía completa del teclado y el reto de 10 rondas.')],
 flujo:[{name:'1 · Referencias',sub:'Image Plane',desc:'Importa imágenes de frente y perfil (View > Image Plane) para respetar proporciones.',key:'View > Image Plane',anim:aRef},
  {name:'2 · Blocking',sub:'Primitivas',desc:'Forma general con primitivas de baja resolución. Pocas caras, solo volumen.',key:'Create > Polygon Primitives',anim:aBlock},
  {name:'3 · Forma principal',sub:'Extrude',desc:'Desarrolla la silueta con Extrude, Bridge, Multi-Cut e Insert Edge Loop.',key:'Ctrl + E',anim:aExtrude},
  {name:'4 · Detalle',sub:'Bevel',desc:'Bevel y loops de soporte para que las esquinas resistan el suavizado.',key:'Ctrl + B',anim:aBevel},
  {name:'5 · Limpieza',sub:'Sin N-gons',desc:'Mesh > Cleanup para hallar N-gons; reconéctalos con Multi-Cut.',key:'Mesh > Cleanup',anim:aMulti},
  {name:'6 · Verificación',sub:'Vista 3',desc:'Revisa el suavizado (3), las normales y la simetría.',key:'3',anim:smoothCycle(SUBQ)},
  {name:'7 · Entrega',sub:'Historial y pivote',desc:'Borra historial, congela transformaciones, centra el pivote y nombra los objetos.',key:'Alt + Shift + D',anim:aDeliver},
  TERM('Ordenar etapas','Ejercicio','Abre el ejercicio para ordenar las 7 etapas del flujo.')],
 academia:[{name:'Repaso: Extrude',sub:'Ctrl + E',desc:'Saca volumen creando caras nuevas.',key:'Ctrl + E',anim:aExtrude},
  {name:'Repaso: Edge Loop',sub:'Insert Edge Loop',desc:'Añade resolución alrededor del modelo.',key:'Mesh Tools',anim:aLoop},
  {name:'Repaso: N-gons',sub:'Topología',desc:'Recuerda: los N-gons deforman el suavizado.',key:'Mesh > Cleanup',anim:smoothCycle(SUBN)},
  TERM('Examen final','Autoevaluación','Abre la autoevaluación de modelado poligonal.')]};

/* --- Construcción del salón --- */
function hallPlate(t1,t2,color,w=12){const c=document.createElement('canvas');c.width=1024;c.height=300;const x=c.getContext('2d');
  const rr=(X,Y,W,H,r)=>{x.beginPath();x.moveTo(X+r,Y);x.arcTo(X+W,Y,X+W,Y+H,r);x.arcTo(X+W,Y+H,X,Y+H,r);x.arcTo(X,Y+H,X,Y,r);x.arcTo(X,Y,X+W,Y,r);x.closePath()};
  const draw=()=>{x.clearRect(0,0,1024,300);x.fillStyle='#141628';rr(8,8,1008,284,36);x.fill();x.lineWidth=12;x.strokeStyle=color;x.stroke();x.textAlign='center';
    x.fillStyle=color;x.font='900 italic 120px Montserrat, Arial, sans-serif';x.fillText(t1,512,150,960);x.fillStyle='#fff';x.font='700 54px Montserrat, Arial, sans-serif';x.fillText(t2,512,245,960);tex.needsUpdate=true};
  const tex=new THREE.CanvasTexture(c);draw();rampPaint.push(draw);if(R)tex.anisotropy=R.capabilities.getMaxAnisotropy();
  return new THREE.Mesh(new THREE.PlaneGeometry(w,w*300/1024),new THREE.MeshBasicMaterial({map:tex,fog:false}))}
function terminal(color){const g=new THREE.Group();g.add(clayW(new THREE.BoxGeometry(4.5,3.2,2.6,3,2,2),[0,1.6,0]));
  const c=document.createElement('canvas');c.width=512;c.height=320;const x=c.getContext('2d');const draw=()=>{x.fillStyle='#0b1240';x.fillRect(0,0,512,320);x.strokeStyle=color;x.lineWidth=10;x.strokeRect(10,10,492,300);
    x.fillStyle=color;x.textAlign='center';x.font='900 italic 64px Montserrat, Arial';x.fillText('LECCIÓN',256,135);x.fillStyle='#fff';x.font='700 38px Montserrat, Arial';x.fillText('Pulsa E',256,215);tex.needsUpdate=true};
  const tex=new THREE.CanvasTexture(c);draw();rampPaint.push(draw);const scr=new THREE.Mesh(new THREE.PlaneGeometry(4.2,2.6),new THREE.MeshBasicMaterial({map:tex}));scr.position.set(0,4.4,.2);scr.rotation.x=-.35;
  g.add(clayW(new THREE.BoxGeometry(4.6,2.9,.3,2,2,1),[0,4.4,0]),scr);g.children[1].rotation.x=-.35;return g}
function catPanel(cat){const [title,color]=KCAT[cat],items=SHORT.filter(s=>s[0]===cat);const c=document.createElement('canvas');c.width=640;c.height=1024;const x=c.getContext('2d');
  const draw=()=>{x.fillStyle='rgba(10,16,52,.92)';x.fillRect(0,0,640,1024);x.strokeStyle=color;x.lineWidth=10;x.strokeRect(5,5,630,1014);x.fillStyle=color;x.fillRect(5,5,630,96);
    x.fillStyle='#0b1240';x.font='900 italic 40px Montserrat, Arial';x.textAlign='center';x.fillText(title.toUpperCase(),320,68,600);
    const lh=Math.min(64,880/items.length);items.forEach((s,i)=>{const y=150+i*lh;x.textAlign='left';x.fillStyle=color;x.font=`800 ${Math.round(lh*.42)}px JetBrains Mono, monospace`;x.fillText(s[2],30,y,250);
      x.fillStyle='#e8edff';x.font=`600 ${Math.round(lh*.42)}px Montserrat, Arial`;x.fillText(s[3],300,y,320)});tex.needsUpdate=true};
  const tex=new THREE.CanvasTexture(c);draw();rampPaint.push(draw);const m=new THREE.Mesh(new THREE.PlaneGeometry(7,11.2),new THREE.MeshBasicMaterial({map:tex,side:THREE.DoubleSide}));return m}
function buildHall(b){const accent=b.color===0xffffff?0x0076d6:b.color,acs=hex(accent);const sc=new THREE.Scene();sc.background=new THREE.Color(0x5b5e64);sc.fog=new THREE.Fog(0x5b5e64,70,170);
  sc.add(new THREE.HemisphereLight(0xffffff,0x5a5c60,.95));const dl=new THREE.DirectionalLight(0xffffff,.6);dl.position.set(30,80,20);sc.add(dl);
  const RH=62;const fl=new THREE.Mesh(new THREE.CircleGeometry(RH,72),new THREE.MeshStandardMaterial({color:0x9a9da2,roughness:.95}));fl.rotation.x=-Math.PI/2;sc.add(fl);
  {const pl=[];for(let i=1;i<=7;i++){const r=i*8.5;for(let k=0;k<48;k++){const a1=k/48*Math.PI*2,a2=(k+1)/48*Math.PI*2;pl.push(Math.sin(a1)*r,.05,Math.cos(a1)*r,Math.sin(a2)*r,.05,Math.cos(a2)*r)}}
   for(let k=0;k<32;k++){const a=k/32*Math.PI*2;pl.push(Math.sin(a)*8.5,.05,Math.cos(a)*8.5,Math.sin(a)*RH,.05,Math.cos(a)*RH)}sc.add(wireLines(pl,new THREE.LineBasicMaterial({color:0x4a4c51})))}
  const wg=new THREE.CylinderGeometry(RH,RH,22,48,6,true);const wall=new THREE.Mesh(wg,new THREE.MeshStandardMaterial({color:0xd9dadd,roughness:.9,side:THREE.BackSide,polygonOffset:true,polygonOffsetFactor:1}));
  wall.add(wireLines(quadEdges(wg)));wall.position.y=11;sc.add(wall);
  [.3,21.7].forEach(y=>{const r=new THREE.Mesh(new THREE.TorusGeometry(RH-.3,.3,6,96),new THREE.MeshBasicMaterial({color:accent}));r.rotation.x=Math.PI/2;r.position.y=y;sc.add(r)});
  const title=hallPlate(b.name,'Interior · '+b.sub,acs,30);title.position.set(0,19,-RH+.6);sc.add(title);
  const list=STN[b.id],n=list.length,st=[],cols=[];
  list.forEach((s,k)=>{const a=Math.PI+(k-(n-1)/2)*(2*Math.PI*.78/n);const R0=s.holo?0:40,x=Math.sin(a)*R0,z=Math.cos(a)*R0;const g=new THREE.Group();g.position.set(x,0,z);g.rotation.y=a+Math.PI;sc.add(g);
    const o={s,a,g,px:0,pz:0,off:k*.37};
    if(s.holo){// teclado holográfico en el centro del salón
      const holo=new THREE.Group();holo.position.set(0,6.5,-2);holo.rotation.x=.55;const u=1.85;const keyM={};
      const baseMat=()=>new THREE.MeshBasicMaterial({color:0x56e0ff,transparent:true,opacity:.16,blending:THREE.AdditiveBlending,depthWrite:false});
      KB.keys.forEach(k=>{const geo=new THREE.BoxGeometry(k.w*u*.9,.35,u*.9);const m=new THREE.Mesh(geo,baseMat());m.position.set((k.x+k.w/2-KB.W/2)*u,0,(k.y+.5-KB.H/2)*u);
        const e=new THREE.LineSegments(new THREE.EdgesGeometry(geo),new THREE.LineBasicMaterial({color:0x8fe8ff,transparent:true,opacity:.75}));m.add(e);holo.add(m);keyM[k.id]=m});
      const lc=document.createElement('canvas');lc.width=2048;lc.height=Math.round(2048*KB.H/(KB.W+.6));const ltex=new THREE.CanvasTexture(lc);
      const drawL=()=>{drawKeyboard(lc.getContext('2d'),lc.width,lc.height,new Map(),{stroke:'rgba(0,0,0,0)',text:'#e9fbff'});ltex.needsUpdate=true};drawL();rampPaint.push(drawL);
      const lab=new THREE.Mesh(new THREE.PlaneGeometry((KB.W+.6)*u,lc.height/lc.width*(KB.W+.6)*u),new THREE.MeshBasicMaterial({map:ltex,transparent:true,depthWrite:false}));lab.rotation.x=-Math.PI/2;lab.position.y=.2;holo.add(lab);
      const frame=new THREE.Mesh(new THREE.PlaneGeometry((KB.W+1.2)*u,(KB.H+1)*u),new THREE.MeshBasicMaterial({color:0x56a8ff,transparent:true,opacity:.08,side:THREE.DoubleSide,depthWrite:false}));frame.rotation.x=-Math.PI/2;frame.position.y=-.25;holo.add(frame);
      const base=clayW(new THREE.CylinderGeometry(3,4,1.2,16,1),[0,.6,-2]);g.add(base);
      const beam=new THREE.Mesh(new THREE.CylinderGeometry(2.6,3.6,6,24,1,true),new THREE.MeshBasicMaterial({color:0x56e0ff,transparent:true,opacity:.1,side:THREE.DoubleSide,depthWrite:false}));beam.position.set(0,3.8,-2);g.add(beam);
      // panel de información sobre el teclado
      const ic=document.createElement('canvas');ic.width=1024;ic.height=360;const itex=new THREE.CanvasTexture(ic);const info=new THREE.Mesh(new THREE.PlaneGeometry(24,8.4),new THREE.MeshBasicMaterial({map:itex,transparent:true,depthWrite:false}));
      info.position.set(0,15.5,-8);g.add(info,holo);o.holo={keyM,itex,ic,idx:0,tNext:0};colliders0(o,{r:5,dx:0,dz:-2});o.px=x+Math.sin(a+Math.PI)*0;
      const pz=12;o.px=x+Math.sin(a)*-pz*-1;o.pz=z;}
    else{g.add(clayW(new THREE.CylinderGeometry(5,5.6,2.4,20,1),[0,1.2,0]));const ring=new THREE.Mesh(new THREE.TorusGeometry(5.3,.18,6,48),new THREE.MeshBasicMaterial({color:accent}));ring.rotation.x=Math.PI/2;ring.position.y=2.45;g.add(ring);
      if(s.terminal){const tm=terminal(acs);tm.position.y=2.4;g.add(tm)}
      else if(s.panel){const p=catPanel(s.panel);p.position.set(0,8.4,0);g.add(p)}
      else{const D={g:new THREE.Group(),parts:[],accent};D.g.position.y=2.4+(s.scale||2.2)*1.25;D.g.scale.setScalar(s.scale||2.2);g.add(D.g);o.D=D;dispSet(D,s.anim(0))}
      const pl=hallPlate(s.name,s.sub,acs,11);pl.position.set(0,s.panel?16:12.5,0);g.add(pl);
      cols.push({x,z,r:6});o.px=Math.sin(a)*31;o.pz=Math.cos(a)*31}
    const pad=new THREE.Mesh(new THREE.RingGeometry(2.6,3.4,40),new THREE.MeshBasicMaterial({color:accent,transparent:true,opacity:.9,side:THREE.DoubleSide}));pad.rotation.x=-Math.PI/2;pad.position.set(o.px,.08,o.pz);sc.add(pad);o.pad=pad;st.push(o)});
  // centro: teclado (Atajos) o letrero en el piso
  const holoSt=st.find(o=>o.s.holo);if(holoSt){holoSt.g.position.set(0,0,0);holoSt.g.rotation.y=0;holoSt.px=0;holoSt.pz=17;holoSt.pad.position.set(0,.08,17);cols.push({x:0,z:-2,r:5})}
  else{const gs=groundSign(b.name,b.sub,acs);gs.position.set(0,.1,0);gs.scale.setScalar(.9);const gg=new THREE.Group();gg.add(gs);gg.rotation.y=Math.PI;sc.add(gg)}
  // salida
  const ex={x:0,z:RH-8};const exPad=new THREE.Mesh(new THREE.RingGeometry(3,4,40),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.9,side:THREE.DoubleSide}));exPad.rotation.x=-Math.PI/2;exPad.position.set(ex.x,.08,ex.z);sc.add(exPad);
  const exS=hallPlate('SALIDA','Volver a la ciudad','#ffffff',10);exS.position.set(0,9,RH-.6);exS.rotation.y=Math.PI;sc.add(exS);
  return{sc,st,cols,ex,exPad,accent,RH}}
function colliders0(){}
function getHall(b){return HALLS[b.id]||(HALLS[b.id]=buildHall(b))}

/* --- Holograma: avanza al siguiente atajo --- */
function holoShow(o,i){const H=o.holo;H.idx=(i+SHORT.length)%SHORT.length;const sc=SHORT[H.idx],col=KCAT[sc[0]][1],hi=shortHi(sc);
  Object.entries(H.keyM).forEach(([id,m])=>{const on=hi.has(id)||(id==='rshift'&&hi.has('lshift'))||(id==='rctrl'&&hi.has('lctrl'))||(id==='ralt'&&hi.has('lalt'));
    m.material.color.set(on?col:0x56e0ff);m.material.opacity=on?.85:.16;m.userData.on=on});
  const x=H.ic.getContext('2d');x.clearRect(0,0,1024,360);x.fillStyle='rgba(8,14,48,.85)';x.fillRect(0,0,1024,360);x.strokeStyle=col;x.lineWidth=10;x.strokeRect(5,5,1014,350);
  x.fillStyle=col;x.fillRect(5,5,1014,64);x.fillStyle='#0b1240';x.font='800 34px Montserrat, Arial';x.textAlign='left';x.fillText(KCAT[sc[0]][0].toUpperCase(),30,50);
  x.textAlign='right';x.fillText(`${H.idx+1} / ${SHORT.length}`,994,50);x.textAlign='center';x.fillStyle=col;x.font='800 76px JetBrains Mono, monospace';x.fillText(sc[2],512,160,980);
  x.fillStyle='#fff';x.font='900 italic 56px Montserrat, Arial';x.fillText(sc[3],512,235,980);x.fillStyle='#c9d3f5';x.font='600 34px Montserrat, Arial';x.fillText(sc[4],512,300,980);H.itex.needsUpdate=true;H.tNext=performance.now()+3600}

/* --- Entrar, salir y conducir dentro del salón --- */
function enterHall(b){for(const k in keys)keys[k]=false;curB=b;curHall=getHall(b);mode='hall';near=null;hallNear=null;q('prompt').hidden=true;
  curHall.sc.add(trike);S.x=curHall.ex.x;S.z=curHall.ex.z-2;S.h=S.mh=Math.PI;S.v=0;S.y=0;S.air=false;S.drift=false;
  const fx=Math.sin(S.h),fz=Math.cos(S.h);cam.position.set(S.x-fx*9,4.4,S.z-fz*9);cam.lookAt(S.x+fx*5,1.9,S.z+fz*5);
  const firstAll=!visited.has(b.id)&&visited.size===B.length-1;visited.add(b.id);store.set('cp_visited',[...visited]);renderProg();SFX.init();SFX.enter();if(firstAll)setTimeout(()=>SFX.win(),450);
  const h=curHall.st.find(o=>o.holo);if(h)holoShow(h,h.holo.idx);trick(`Interior · ${b.name}`)}
function exitHall(){if(mode!=='hall')return;mode='city';scene.add(trike);hallNear=null;q('prompt').hidden=true;q('enterBtn').innerHTML='Entrar <kbd>E</kbd>';placeAt(curB);S.h=S.mh=curB.angle+Math.PI;snapCam();SFX.exit()}
function hallAction(){if(!hallNear)return;if(hallNear==='exit'){exitHall();return}const o=hallNear,s=o.s;
  if(s.holo){holoShow(o,o.holo.idx+1);SFX.click();return}openLesson(curB,s)}
function openLesson(b,s){openInterior(b);setTimeout(()=>{if(s.tool&&typeof showTool==='function'){showTool(s.tool);q('toolkit').scrollIntoView()}
  else if(s.anat&&typeof setAnatMode==='function')setAnatMode(s.anat);
  else if(s.panel){q('kbInfo').scrollIntoView();kbFilter(s.panel)}},50)}
function showHallPrompt(){const P=q('prompt');if(!hallNear){P.hidden=true;return}P.hidden=false;SFX.chime();
  if(hallNear==='exit'){P.style.setProperty('--c','#ffffff');q('promptN').textContent='SALIDA';q('promptS').textContent='Vuelve a la ciudad.';q('enterBtn').innerHTML='Salir <kbd>E</kbd>';return}
  const s=hallNear.s;P.style.setProperty('--c',hex(curHall.accent));q('promptN').textContent=s.name;q('promptS').textContent=s.desc+(s.key&&s.key!=='—'?`  ·  ${s.key}`:'');
  q('enterBtn').innerHTML=s.holo?'Siguiente atajo <kbd>E</kbd>':'Ver lección <kbd>E</kbd>'}
function updateHall(dt,t){const H=curHall;
  const bNow=!!(keys.boost&&keys.up);if(bNow&&!boostWas&&Math.abs(S.v)>3)SFX.turbo();boostWas=bNow;
  const max=keys.boost?32:22;if(keys.up)S.v+=(keys.boost?20:13)*dt;else if(keys.down)S.v-=(S.v>0?26:9)*dt;else S.v-=Math.sign(S.v)*Math.min(Math.abs(S.v),7*dt);
  S.v=Math.max(-8,Math.min(max,S.v>max?S.v-30*dt:S.v));const st=(keys.left?1:0)-(keys.right?1:0);S.steer+=(st-S.steer)*Math.min(1,dt*8);
  S.drift=!!keys.drift&&S.v>7;S.h+=S.steer*dt*1.9*(S.drift?1.75:1)*Math.tanh(S.v/6);let dh=S.h-S.mh;dh=Math.atan2(Math.sin(dh),Math.cos(dh));S.mh+=dh*Math.min(1,dt*(S.drift?2.2:10));
  S.x+=Math.sin(S.mh)*S.v*dt;S.z+=Math.cos(S.mh)*S.v*dt;const v0=Math.abs(S.v);
  for(const c of H.cols){const dx=S.x-c.x,dz=S.z-c.z,d=Math.hypot(dx,dz),m=c.r+1.6;if(d<m&&d>0){S.x=c.x+dx/d*m;S.z=c.z+dz/d*m;S.v*=.4}}
  const r=Math.hypot(S.x,S.z),lim=H.RH-2.5;if(r>lim){S.x*=lim/r;S.z*=lim/r;S.v*=.4}if(v0>5&&Math.abs(S.v)<v0*.7)SFX.thud(v0/25);
  trike.position.set(S.x,0,S.z);trike.rotation.set(0,S.h,0);trike.rotateZ(-S.steer*Math.min(1,Math.abs(S.v)/25)*(S.drift?.3:.18));trikeVisual(dt,t);
  const fx=Math.sin(S.h),fz=Math.cos(S.h),back=9+Math.abs(S.v)*.08;const want=new THREE.Vector3(S.x-Math.sin(S.mh)*back,4.4+Math.abs(S.v)*.03,S.z-Math.cos(S.mh)*back);
  const wr=Math.hypot(want.x,want.z);if(wr>H.RH-1.5){want.x*=(H.RH-1.5)/wr;want.z*=(H.RH-1.5)/wr}cam.position.lerp(want,1-Math.exp(-dt*4));cam.lookAt(S.x+fx*5,1.9,S.z+fz*5);
  cam.fov+=((62+Math.abs(S.v)*.35)-cam.fov)*Math.min(1,dt*3);cam.updateProjectionMatrix();
  let nt=null;for(const o of H.st)if(Math.hypot(S.x-o.px,S.z-o.pz)<4.2)nt=o;if(!nt&&Math.hypot(S.x-H.ex.x,S.z-H.ex.z)<4.2)nt='exit';if(nt!==hallNear){hallNear=nt;showHallPrompt()}
  q('spd').parentElement.style.borderColor=S.drift?'#F7C948':'';q('spd').textContent=Math.round(Math.abs(S.v)*3.6)}
let hallFrame=0;
function animHall(dt,t){const H=curHall;hallFrame++;
  H.st.forEach((o,i)=>{const s2=1+Math.sin(t*3+i)*.08;o.pad.scale.set(s2,s2,1);
    if(o.D){o.D.g.rotation.y+=.3*dt;const d=Math.hypot(S.x-o.g.position.x,S.z-o.g.position.z);if(d<45||hallFrame%8===i%8)dispSet(o.D,o.s.anim(t+o.off))}
    if(o.holo){if(performance.now()>o.holo.tNext)holoShow(o,o.holo.idx+1);Object.values(o.holo.keyM).forEach(m=>{m.position.y=m.userData.on?.35+Math.sin(t*6)*.12:0})}});
  H.exPad.scale.setScalar(1+Math.sin(t*3)*.06)}
function drawMiniHall(){const W=mc.width,H=curHall,sc=W/2/(H.RH+6);mx.clearRect(0,0,W,W);mx.save();mx.translate(W/2,W/2);
  mx.fillStyle='rgba(5,10,46,.6)';mx.beginPath();mx.arc(0,0,W/2,0,7);mx.fill();mx.strokeStyle=hex(H.accent);mx.lineWidth=6;mx.beginPath();mx.arc(0,0,H.RH*sc,0,7);mx.stroke();
  const P=(x,z)=>[-x*sc,-z*sc];H.st.forEach(o=>{const p=P(o.g.position.x,o.g.position.z);mx.fillStyle=hex(H.accent);mx.beginPath();mx.arc(p[0],p[1],10,0,7);mx.fill()});
  {const p=P(H.ex.x,H.ex.z);mx.fillStyle='#fff';mx.fillRect(p[0]-7,p[1]-7,14,14)}
  const p=P(S.x,S.z);mx.save();mx.translate(p[0],p[1]);mx.rotate(-S.h+Math.PI);mx.fillStyle='#F7C948';mx.beginPath();mx.moveTo(0,-16);mx.lineTo(11,13);mx.lineTo(0,6);mx.lineTo(-11,13);mx.closePath();mx.fill();mx.restore();mx.restore()}

/* --- Infografía del teclado en la lección de Atajos --- */
function kbFilter(cat){const list=q('kbList');if(!list)return;[...list.querySelectorAll('.kbcat')].forEach(el=>el.hidden=!!cat&&el.dataset.cat!==cat);
  [...q('kbTabs').querySelectorAll('button')].forEach(b=>b.setAttribute('aria-pressed',(b.dataset.cat||'')===(cat||'')))}
function kbRender(sc){const c=q('kbCanvas');if(!c)return;const w=c.width,h=c.height;drawKeyboard(c.getContext('2d'),w,h,sc?shortHi(sc):new Map(),{bg:'#0a1240',keyFill:'rgba(86,168,255,.08)'});
  const sh=sc?(id=>sc[1].includes(id)):()=>false;if(sc){q('kbNow').innerHTML=`<b style="color:${KCAT[sc[0]][1]}">${sc[2]}</b> · ${sc[3]}<br><span>${sc[4]}</span>`}}
(function(){const tabs=q('kbTabs'),list=q('kbList');if(!tabs)return;
  tabs.innerHTML=`<button data-cat="" aria-pressed="true">Todas</button>`+Object.entries(KCAT).map(([k,[n,c]])=>`<button data-cat="${k}" style="--c:${c}" aria-pressed="false">${n}</button>`).join('');
  list.innerHTML=Object.entries(KCAT).map(([k,[n,c]])=>`<div class="kbcat" data-cat="${k}"><h5 style="color:${c}">${n}</h5>${SHORT.map((s,i)=>s[0]===k?`<button data-i="${i}"><kbd>${s[2]}</kbd><span>${s[3]}</span></button>`:'').join('')}</div>`).join('');
  tabs.addEventListener('click',e=>{const bt=e.target.closest('button');if(bt)kbFilter(bt.dataset.cat)});
  list.addEventListener('click',e=>{const bt=e.target.closest('button');if(!bt)return;list.querySelectorAll('button').forEach(x=>x.classList.remove('on'));bt.classList.add('on');kbRender(SHORT[+bt.dataset.i])});
  kbRender(SHORT[21]);rampPaint.push(()=>kbRender(SHORT[21]))})();
