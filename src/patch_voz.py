# Voz de narrador estilo IA (tono calmado y sintético, como el anuncio de referencia): bienvenida en la esfera central y nombre de cada edificio al entrar
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, 'shell.html')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# destello digital que antecede a cada anuncio
rep("    step(){if(ok('step',140)){", "    ai(){if(ok('ai',300)){notes([587.3,880,1174.7,1760],.05,'sine',.06);noise(.45,700,6500,.045,'bandpass',2)}},\n    step(){if(ok('step',140)){")

# narrador: elige la mejor voz en español disponible y le da un tono pausado y sintético
rep("q('sndBtn').textContent=SFX.isOn()?'Sonido: sí':'Sonido: no';", r"""const VOICE=(()=>{const has='speechSynthesis' in window;let v=null;
  const pickV=()=>{const vs=speechSynthesis.getVoices(),es=vs.filter(x=>/^es/i.test(x.lang)),good=x=>/natural|neural|online|google/i.test(x.name);
    v=es.find(x=>/(MX|US|419|EC|CO)/i.test(x.lang)&&good(x))||es.find(good)||es.find(x=>/(MX|US|419|EC|CO)/i.test(x.lang))||es[0]||null};
  if(has){pickV();speechSynthesis.addEventListener&&speechSynthesis.addEventListener('voiceschanged',pickV)}
  return{say(text){if(!has||!SFX.isOn())return;try{speechSynthesis.cancel();SFX.ai();const u=new SpeechSynthesisUtterance(text);u.lang=v?v.lang:'es-ES';if(v)u.voice=v;
    u.rate=.88;u.pitch=.8;u.volume=1;setTimeout(()=>speechSynthesis.speak(u),380)}catch(e){}},stop(){if(has)try{speechSynthesis.cancel()}catch(e){}}}})();
q('sndBtn').addEventListener('click',()=>{if(!SFX.isOn())VOICE.stop()});
q('sndBtn').textContent=SFX.isOn()?'Sonido: sí':'Sonido: no';""")

# bienvenida al acercarse a la esfera del centro (se vuelve a activar al alejarse)
rep("let boostWas=false;", "let boostWas=false,welcomed=false;")
rep("  updateSmoke(dt);q('spd').parentElement.style.borderColor=S.drift?'#F7C948':'';",
    "  {const dc=Math.hypot(S.x,S.z);if(dc<26&&!welcomed){welcomed=true;VOICE.say('Bienvenido a Universidad Israel');trick('Bienvenido a Universidad Israel')}else if(dc>44)welcomed=false}\n  updateSmoke(dt);q('spd').parentElement.style.borderColor=S.drift?'#F7C948':'';")

# nombre del edificio al entrar
rep("SFX.enter();SFX.hallAmb(b.id);", "SFX.enter();SFX.hallAmb(b.id);VOICE.say(b.name.charAt(0)+b.name.slice(1).toLowerCase());")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
