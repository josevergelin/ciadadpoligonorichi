# Sonidos sintetizados con Web Audio (sin archivos): motor, turbo, drift, saltos, choques, esferas, edificios e interfaz
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)

rep("/* Bucle */", r"""/* ============ Sonido (Web Audio, sintetizado) ============ */
const SFX=(()=>{let ctx=null,master=null,noiseBuf=null,eng=null,scr=null,amb=null,on=store.get('cp_sound',true);const last={};
  function init(){if(ctx){if(ctx.state==='suspended')ctx.resume();return}
    try{ctx=new (window.AudioContext||window.webkitAudioContext)()}catch(e){return}
    master=ctx.createGain();master.gain.value=on?.8:0;
    const comp=ctx.createDynamicsCompressor();master.connect(comp);comp.connect(ctx.destination);
    noiseBuf=ctx.createBuffer(1,ctx.sampleRate*2,ctx.sampleRate);const d=noiseBuf.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;
    // motor eléctrico retro: dos osciladores desafinados + filtro
    const o1=ctx.createOscillator(),o2=ctx.createOscillator(),lp=ctx.createBiquadFilter(),g=ctx.createGain();o1.type='sawtooth';o2.type='square';o2.detune.value=9;
    lp.type='lowpass';lp.frequency.value=300;lp.Q.value=4;g.gain.value=0;o1.connect(lp);o2.connect(lp);lp.connect(g);g.connect(master);o1.start();o2.start();eng={o1,o2,lp,g};
    // chirrido de llantas para el drift
    const ns=ctx.createBufferSource();ns.buffer=noiseBuf;ns.loop=true;const bp=ctx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=2300;bp.Q.value=8;const sg=ctx.createGain();sg.gain.value=0;
    ns.connect(bp);bp.connect(sg);sg.connect(master);ns.start();scr={bp,g:sg};
    // ambiente de ciudad: acorde grave y suave con respiración lenta
    const ag=ctx.createGain();ag.gain.value=.022;ag.connect(master);[110,164.81,220.5].forEach((f,i)=>{const o=ctx.createOscillator();o.type='sine';o.frequency.value=f;const og=ctx.createGain();og.gain.value=.5;
      const lfo=ctx.createOscillator(),lg=ctx.createGain();lfo.frequency.value=.07+i*.03;lg.gain.value=.45;lfo.connect(lg);lg.connect(og.gain);lfo.start();o.connect(og);og.connect(ag);o.start()});amb=ag}
  const T=()=>ctx.currentTime;
  const ok=(k,gap)=>{if(!ctx||!on)return false;const n=performance.now();if(last[k]&&n-last[k]<gap)return false;last[k]=n;return true};
  function tone(f0,f1,dur,type='sine',vol=.25,delay=0){const t=T()+delay,o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(Math.max(20,f1),t+dur);
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.012);g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(g);g.connect(master);o.start(t);o.stop(t+dur+.05)}
  function noise(dur,f0,f1,vol=.3,type='bandpass',q=1,delay=0){const t=T()+delay,src=ctx.createBufferSource(),fl=ctx.createBiquadFilter(),g=ctx.createGain();src.buffer=noiseBuf;fl.type=type;fl.Q.value=q;
    fl.frequency.setValueAtTime(f0,t);fl.frequency.exponentialRampToValueAtTime(f1,t+dur);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+dur);
    src.connect(fl);fl.connect(g);g.connect(master);src.start(t,Math.random());src.stop(t+dur+.05)}
  const notes=(fs,step,type,vol)=>fs.forEach((f,i)=>tone(f,f*1.002,step*1.6,type,vol,i*step));
  return{init,
    toggle(){on=!on;store.set('cp_sound',on);if(master)master.gain.setTargetAtTime(on?.8:0,T(),.05);return on},isOn:()=>on,
    drive(v,boost,drift,air,t){if(!ctx)return;const sp=Math.abs(v),now=T();
      eng.o1.frequency.setTargetAtTime(48+sp*3.2+(boost?18:0)+(air?40:0),now,.08);eng.o2.frequency.setTargetAtTime(96+sp*6.4+(boost?36:0)+(air?80:0),now,.08);
      eng.lp.frequency.setTargetAtTime(260+sp*38+(boost?500:0),now,.1);eng.g.gain.setTargetAtTime(.035+Math.min(.09,sp*.0035)+(boost&&sp>2?.03:0),now,.1);
      scr.g.gain.setTargetAtTime(drift?.16:0,now,drift?.05:.08);scr.bp.frequency.setTargetAtTime(2100+Math.sin(t*23)*350+sp*12,now,.03);amb.gain.setTargetAtTime(.022,now,.5)},
    quiet(){if(!ctx)return;const now=T();eng.g.gain.setTargetAtTime(0,now,.08);scr.g.gain.setTargetAtTime(0,now,.05);amb.gain.setTargetAtTime(.012,now,.5)},
    turbo(){if(ok('turbo',300)){noise(.6,600,3200,.18,'bandpass',.8);tone(160,420,.45,'sawtooth',.05)}},
    mini(){if(ok('mini',300)){notes([523.3,659.3,784,1046.5],.06,'square',.07);noise(.5,900,4000,.15,'bandpass',.8)}},
    jump(){if(ok('jump',300)){tone(220,880,.35,'triangle',.18);noise(.4,500,2400,.12,'bandpass',.7)}},
    land(k){if(ok('land',200)){const v=Math.min(1,k);tone(140,45,.35,'sine',.35*v+.15);noise(.25,900,200,.22*v+.08,'lowpass',.7)}},
    boing(k){if(ok('boing',45)){const v=Math.min(1,k);const f=380+Math.random()*160;tone(f,f*.45,.32,'sine',.12+.22*v);tone(f*2.01,f*.9,.18,'triangle',.05+.08*v)}},
    thud(k){if(ok('thud',350)){const v=Math.min(1,k);tone(110,50,.22,'sine',.2+.25*v);noise(.18,1200,300,.15*v+.05,'lowpass',1)}},
    chime(){if(ok('chime',400))notes([784,1046.5],.09,'sine',.12)},
    enter(){if(ok('enter',300)){noise(.45,300,2500,.12,'bandpass',.6);notes([392,523.3,659.3,784],.07,'triangle',.11)}},
    exit(){if(ok('exit',300)){noise(.4,2500,300,.1,'bandpass',.6);notes([784,659.3,523.3],.07,'triangle',.09)}},
    click(){if(ok('click',40))tone(1200,900,.05,'square',.035)},
    right(){if(ok('right',100))notes([659.3,987.8],.08,'sine',.16)},
    wrong(){if(ok('wrong',100)){tone(200,140,.28,'sawtooth',.08);tone(206,146,.28,'square',.04)}},
    win(){if(ok('win',500))notes([523.3,659.3,784,1046.5,1318.5],.09,'triangle',.13)}}})();
// el audio solo puede empezar tras una interacción del usuario
['pointerdown','keydown'].forEach(ev=>addEventListener(ev,()=>SFX.init(),{capture:true}));
document.addEventListener('visibilitychange',()=>{if(document.hidden)SFX.quiet()});
// sonidos de interfaz en los interiores (botones, quiz, herramientas)
document.addEventListener('click',e=>{const bt=e.target.closest('button');if(!bt)return;
  if(bt.closest('.q')){if(bt.classList.contains('right'))SFX.right();else if(bt.classList.contains('wrong'))SFX.wrong();return}
  if(bt.closest('#hkO')||bt.id==='flowC')return;SFX.click()});
q('sndBtn').addEventListener('click',()=>{const on=SFX.toggle();q('sndBtn').textContent=on?'Sonido: sí':'Sonido: no';q('sndBtn').setAttribute('aria-pressed',on)});
q('sndBtn').textContent=SFX.isOn()?'Sonido: sí':'Sonido: no';q('sndBtn').setAttribute('aria-pressed',SFX.isOn());

/* Bucle */""")

# HUD: botón de sonido y atajo N
rep('  <div class="prog" id="prog"></div>', '  <div class="prog" id="prog"></div>\n  <button class="snd" id="sndBtn" aria-pressed="true">Sonido: sí</button>')
rep("#hudTop .mark b{", ".snd{justify-self:start;font:800 .66rem var(--f-display);letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:4px 10px;border:1px solid rgba(255,255,255,.3);background:transparent;color:#C9D3F5;cursor:pointer}\n.snd[aria-pressed=\"true\"]{background:#F7C948;color:#141B45;border-color:#F7C948}\n#hudTop .mark b{")
rep("<span><kbd>M</kbd> mapa</span>", "<span><kbd>M</kbd> mapa</span><span><kbd>N</kbd> sonido</span>")
rep("  if(e.code==='KeyM'){toggleStart();return}", "  if(e.code==='KeyM'){toggleStart();return}\n  if(e.code==='KeyN'){q('sndBtn').click();return}")

# motor y efectos de manejo
rep("function loop(now){requestAnimationFrame(loop);const dt=Math.min(.05,(now-last)/1000);last=now;const t=now/1000;\n  if(!R||document.hidden)return;if(!q('interior').hidden)return;",
    "function loop(now){requestAnimationFrame(loop);const dt=Math.min(.05,(now-last)/1000);last=now;const t=now/1000;\n  if(!R||document.hidden)return;if(!q('interior').hidden){SFX.quiet();return}\n  if(paused||!q('start').hidden)SFX.quiet();else SFX.drive(S.v,keys.boost&&keys.up,S.drift,S.air,t);")
rep("function update(dt,t){", "let boostWas=false;\nfunction update(dt,t){\n  const bNow=!!(keys.boost&&keys.up);if(bNow&&!boostWas&&Math.abs(S.v)>3)SFX.turbo();boostWas=bNow;")
rep("trick(`¡Mini turbo! Drift ${S.dt0.toFixed(1)} s`)", "trick(`¡Mini turbo! Drift ${S.dt0.toFixed(1)} s`);SFX.mini()")
rep("if(S.airT>.35){trick(`¡Salto! ${S.airT.toFixed(2)} s en el aire`);landPuff()}", "if(S.airT>.35){trick(`¡Salto! ${S.airT.toFixed(2)} s en el aire`);landPuff();SFX.land(S.airT)}")
rep("S.ringJump=S.lastVy>1}", "S.ringJump=S.lastVy>1;if(S.lastVy>1)SFX.jump()}")
rep("b.v.y=Math.max(b.v.y,5+sp*.5);S.v*=.9}}", "b.v.y=Math.max(b.v.y,5+sp*.5);S.v*=.9;SFX.boing(rel/18)}}")
# choques con edificios
rep("function collide(){const pr=1.6;", "function collide(){const pr=1.6,v0=Math.abs(S.v);")
rep("  const r=Math.hypot(S.x,S.z);if(r>340){S.x*=340/r;S.z*=340/r;S.v*=.5}}", "  const r=Math.hypot(S.x,S.z);if(r>340){S.x*=340/r;S.z*=340/r;S.v*=.5}\n  if(v0>5&&Math.abs(S.v)<v0*.7)SFX.thud(v0/25)}")
# edificios
rep("if(nb!==near){near=nb;const P=q('prompt');P.hidden=!nb;if(nb){", "if(nb!==near){near=nb;const P=q('prompt');P.hidden=!nb;if(nb){SFX.chime();")
rep("function openInterior(b){for(const k in keys)keys[k]=false;S.v=0;", "function openInterior(b){for(const k in keys)keys[k]=false;S.v=0;SFX.init();SFX.enter();const firstAll=!visited.has(b.id)&&visited.size===B.length-1;if(firstAll)setTimeout(()=>SFX.win(),450);")
rep("function closeInterior(){q('interior').hidden=true;", "function closeInterior(){SFX.exit();q('interior').hidden=true;")
# reto de atajos y flujo
rep("  if(ok){hk.streak++;", "  ok?SFX.right():SFX.wrong();\n  if(ok){hk.streak++;")
rep("  if(hk.pts>hk.best){", "  if(hk.pts>=600)SFX.win();\n  if(hk.pts>hk.best){")
rep("  if(okN===flow.length){m.className='helpline ok';", "  okN===flow.length?SFX.win():SFX.wrong();\n  if(okN===flow.length){m.className='helpline ok';")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
