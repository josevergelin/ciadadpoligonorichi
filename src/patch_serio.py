# Música de fondo más seria: drones graves en tonalidad menor, pulsos sub y oleadas lentas (sin arpegios agudos ni campanitas)
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

a = s.index("  const PAT={"); b = s.index("  function stopAmb(){", a)
s = s[:a] + r"""  // oleada de ruido filtrado que crece y se apaga (como un "swell" de cine)
  function swell(dur,f0,f1,vol){if(!ab)return;const t=T(),src=ctx.createBufferSource(),fl=ctx.createBiquadFilter(),g=ctx.createGain();src.buffer=noiseBuf;src.loop=true;fl.type='lowpass';fl.Q.value=4;
    fl.frequency.setValueAtTime(f0,t);fl.frequency.exponentialRampToValueAtTime(f1,t+dur*.8);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+dur*.8);g.gain.exponentialRampToValueAtTime(.0001,t+dur);
    src.connect(fl);fl.connect(g);g.connect(ab);src.start(t);src.stop(t+dur+.1)}
  const sub=(f,dur,vol)=>pl(f,f*.97,dur,'sine',vol);
  const PAT={
    // Componentes: re menor, latido grave y un eco metálico lejano
    componentes(){if(stp%13===0)sub(73.4,1.8,.05);if(stp%26===13)fm(220,1.5,.8,4,.018);if(stp%40===0)swell(5,200,1800,.018)},
    // Herramientas: maquinaria pesada, pulso industrial en do menor
    herramientas(){if(stp%8===0)sub(65.4,.6,.12);if(stp%8===4)sub(65.4,.4,.05);if(stp%32===16)fm(130.8,1.41,2.5,2.5,.022);if(stp%48===40)swell(4,150,1200,.022)},
    // Topología: espacio profundo en la menor
    topologia(){if(stp%20===0)sub(55,3,.07);if(stp%30===15)fm(110,2,.6,5,.018);if(stp%60===30)swell(6,100,900,.02)},
    // Atajos: secuencia de bajo tensa en mi menor
    atajos(){const seq=[82.4,82.4,98,82.4,110,82.4,98,73.4];pl(seq[stp%8],seq[stp%8],.14,'triangle',.035);if(stp%32===0)swell(4,200,2400,.016)},
    // Flujo: calma grave, acorde abierto que respira
    flujo(){if(stp%24===0)sub(87.3,3,.05);if(stp%36===18)fm(174.6,2,.5,4,.016);if(stp%48===24)swell(5,300,2000,.014)},
    // Academia: solemne, campana grave y coro oscuro en re menor
    academia(){if(stp%32===0){fm(146.8,2.01,1.2,6,.032);sub(73.4,4,.05)}if(stp%64===48)swell(6,200,1500,.016)}};
  const PADS={componentes:()=>padR([73.4,110,174.6],'sawtooth',.012,500,3,.05,250),
    herramientas:()=>{padR([65.4,98,155.6],'sawtooth',.016,380,5,.08,200);wind(3000,.004,.07)},
    topologia:()=>padR([55,82.4,130.8],'triangle',.03,450,6,.03,300),
    atajos:()=>padR([82.4,123.5,196],'sawtooth',.01,600,4,.12,350),
    flujo:()=>{padR([87.3,130.8,164.8,220],'sine',.022,900,1,.03,300);wind(700,.012,.04)},
    academia:()=>padR([73.4,110,146.8,174.6],'sawtooth',.011,700,2,.04,350)};
""" + s[b:]

# ciudad: acorde grave en la menor
rep("[110,164.81,220.5].forEach((f,i)=>{const o=ctx.createOscillator();o.type='sine';o.frequency.value=f;const og=ctx.createGain();og.gain.value=.5;",
    "[55,82.41,130.81].forEach((f,i)=>{const o=ctx.createOscillator();o.type='sine';o.frequency.value=f;const og=ctx.createGain();og.gain.value=.7;")
# avisos más sobrios (puerta, entrar, salir, narrador)
rep("    chime(){if(ok('chime',400))notes([784,1046.5],.09,'sine',.12)},", "    chime(){if(ok('chime',400)){tone(440,440,.6,'sine',.06);tone(659.3,659.3,.6,'sine',.03)}},")
rep("    enter(){if(ok('enter',300)){noise(.45,300,2500,.12,'bandpass',.6);notes([392,523.3,659.3,784],.07,'triangle',.11)}},",
    "    enter(){if(ok('enter',300)){noise(.7,200,2200,.1,'lowpass',2);tone(146.8,146.8,1.3,'triangle',.08);tone(220,220,1.3,'sine',.05);tone(73.4,70,1.3,'sine',.1)}},")
rep("    exit(){if(ok('exit',300)){noise(.4,2500,300,.1,'bandpass',.6);notes([784,659.3,523.3],.07,'triangle',.09)}},",
    "    exit(){if(ok('exit',300)){noise(.6,2200,200,.09,'lowpass',2);tone(110,108,1,'triangle',.07);tone(55,52,1,'sine',.09)}},")
rep("    ai(){if(ok('ai',300)){notes([587.3,880,1174.7,1760],.05,'sine',.06);noise(.45,700,6500,.045,'bandpass',2)}},",
    "    ai(){if(ok('ai',300)){notes([293.7,440,587.3],.07,'sine',.05);noise(.5,300,3000,.04,'lowpass',3)}},")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
