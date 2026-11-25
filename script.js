(()=>{
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches, $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
const FINE=matchMedia('(pointer:fine)').matches;
/* loader: rings grow, then the log splits open (home only, once per session) */
const ld=$('.loader');
if(ld){ if(RM||sessionStorage.getItem('fst-ld')){ld.classList.add('done')} else {sessionStorage.setItem('fst-ld','1');setTimeout(()=>ld.classList.add('go'),1250);setTimeout(()=>ld.classList.add('done'),2350)} }
/* reveals */
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}}),{threshold:.14,rootMargin:'0px 0px -6% 0px'});
$$('.rv,.split,.gauge,.cta,.storm,.big-score').forEach(el=>RM?el.classList.add('in'):io.observe(el));
// hero headline reveals right after loader
const hh=$('.hero .split,.phero .split'); if(hh&&!RM){setTimeout(()=>hh.classList.add('in'),ld&&!ld.classList.contains('done')?1350:150)}
/* counters */
function count(el){const to=parseFloat(el.dataset.to),dec=+el.dataset.dec||0;if(RM){el.textContent=to.toFixed(dec);return}
 const t0=performance.now(),d=1600;const step=t=>{const k=Math.min(1,(t-t0)/d),v=to*(1-Math.pow(1-k,3));el.textContent=v.toFixed(dec);if(k<1)requestAnimationFrame(step);else el.textContent=to.toFixed(dec)};requestAnimationFrame(step)}
const cio=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){count(en.target);cio.unobserve(en.target)}}),{threshold:.4});
$$('[data-to]').forEach(el=>cio.observe(el));
/* nav + progress vine + mobile bar + service timeline */
const nav=$('.nav'),vine=$('.vine'),mbar=$('.mbar'),trunk=$('.steps');
function onScroll(){const y=scrollY,h=document.documentElement.scrollHeight-innerHeight;
 nav&&nav.classList.toggle('scrolled',y>40);vine&&vine.style.setProperty('--p',h>0?(y/h).toFixed(4):0);
 mbar&&mbar.classList.toggle('show',y>innerHeight*.6);
 if(trunk){const r=trunk.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.7-r.top)/r.height));trunk.style.setProperty('--tp',RM?1:p.toFixed(3))}}
addEventListener('scroll',onScroll,{passive:true});onScroll();
/* mobile menu */
const mb=$('.menu-btn'),mm=$('.mmenu');
if(mb&&mm){const set=o=>{mb.setAttribute('aria-expanded',o);mb.setAttribute('aria-label',o?'Close menu':'Open menu');mm.classList.toggle('open',o);mm.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';if(o)setTimeout(()=>$('a',mm).focus(),300)};
 mb.addEventListener('click',()=>set(mb.getAttribute('aria-expanded')!=='true'));addEventListener('keydown',e=>{if(e.key==='Escape'&&mm.classList.contains('open')){set(false);mb.focus()}});$$('a',mm).forEach(a=>a.addEventListener('click',()=>set(false)))}
/* live badge: Google lists "Open 24 hours" every day (America/New_York) */
const HOURS={0:[0,24],1:[0,24],2:[0,24],3:[0,24],4:[0,24],5:[0,24],6:[0,24]};
function live(){const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',weekday:'short',hour:'numeric',hour12:false}).formatToParts(new Date());
 const wd=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(p.find(x=>x.type==='weekday').value),hr=+p.find(x=>x.type==='hour').value%24,h=HOURS[wd],open=h&&hr>=h[0]&&hr<h[1];
 $$('[data-live]').forEach(b=>{b.querySelector('span').textContent=open?(h[1]-h[0]===24?'Open now · 24 hours':'Open now'):'Closed now';b.classList.toggle('closed',!open)})}
live();setInterval(live,60000);
/* magnetic buttons (fine pointers only; no cursor follower) */
if(FINE&&!RM)$$('.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.28}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});
/* tilt cards */
if(FINE&&!RM)$$('.tilt').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',(x*8)+'deg');c.style.setProperty('--rx',(-y*8)+'deg')});c.addEventListener('pointerleave',()=>{c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg')})});
/* hero parallax */
const art=$('.h-art'),pol=$('.polaroid');
if(art&&!RM){addEventListener('scroll',()=>{const y=scrollY;if(y<innerHeight*1.2){art.style.transform=`translateY(${y*.08}px)`;pol&&(pol.style.translate=`0 ${-y*.12}px`)}},{passive:true})}
/* hotspot pins */
$$('.pin').forEach(p=>p.addEventListener('click',e=>{e.stopPropagation();const o=p.getAttribute('aria-expanded')==='true';$$('.pin').forEach(q=>q.setAttribute('aria-expanded','false'));p.setAttribute('aria-expanded',!o)}));
document.addEventListener('click',()=>$$('.pin').forEach(q=>q.setAttribute('aria-expanded','false')));
/* reviews carousel (pauses on hover/focus) */
$$('[data-car]').forEach(car=>{const sl=$$('.slide',car),dots=$('.car-dots',car);let i=0,tm=null,paused=false;
 sl.forEach((s,k)=>{const b=document.createElement('button');b.setAttribute('aria-label','Show review '+(k+1));b.addEventListener('click',()=>go(k));dots.appendChild(b)});
 function go(k){i=(k+sl.length)%sl.length;sl.forEach((s,n)=>{s.classList.toggle('on',n===i);s.setAttribute('aria-hidden',n!==i)});$$('button',dots).forEach((d,n)=>d.setAttribute('aria-current',n===i))}
 $('.prev',car).addEventListener('click',()=>go(i-1));$('.next',car).addEventListener('click',()=>go(i+1));
 car.addEventListener('mouseenter',()=>paused=true);car.addEventListener('mouseleave',()=>paused=false);car.addEventListener('focusin',()=>paused=true);car.addEventListener('focusout',()=>paused=false);
 let sx=null;car.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});car.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)go(i+(dx<0?1:-1));sx=null});
 go(0);if(!RM)tm=setInterval(()=>{if(!paused&&!document.hidden)go(i+1)},6500)});
/* drag rail */
$$('.rail').forEach(r=>{let down=false,sx=0,sl=0;r.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;sx=e.clientX;sl=r.scrollLeft;r.classList.add('drag')});
 addEventListener('pointerup',()=>{down=false;r.classList.remove('drag')});r.addEventListener('pointermove',e=>{if(!down)return;r.scrollLeft=sl-(e.clientX-sx)});
 r.addEventListener('keydown',e=>{if(e.key==='ArrowRight')r.scrollBy({left:300,behavior:'smooth'});if(e.key==='ArrowLeft')r.scrollBy({left:-300,behavior:'smooth'})})});
/* gallery filter */
$$('.fbtn').forEach(b=>b.addEventListener('click',()=>{const f=b.dataset.f;$$('.fbtn').forEach(x=>x.setAttribute('aria-pressed',x===b));$$('.gi').forEach(g=>{g.classList.toggle('off',f!=='all'&&g.dataset.tag!==f);g.classList.add('in')})}));
/* lightbox: keyboard, swipe, focus trap */
const lb=$('.lbx');
if(lb){const im=$('img',lb),cap=$('figcaption',lb);let list=[],i=0,last=null;
 const vis=()=>$$('.gi:not(.off) .gi-b');
 function show(k){list=vis();i=(k+list.length)%list.length;const b=list[i];im.src=b.dataset.full;im.alt=b.dataset.cap;cap.textContent=b.dataset.cap}
 function open(b){last=b;lb.hidden=false;document.body.style.overflow='hidden';show(vis().indexOf(b));$('.lbx-x',lb).focus()}
 function close(){lb.hidden=true;document.body.style.overflow='';last&&last.focus()}
 $$('.gi-b').forEach(b=>b.addEventListener('click',()=>open(b)));
 $('.lbx-x',lb).addEventListener('click',close);$('.lbx-p',lb).addEventListener('click',()=>show(i-1));$('.lbx-n',lb).addEventListener('click',()=>show(i+1));
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1);
  if(e.key==='Tab'){const f=$$('button',lb);const a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
 let sx=null;lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)show(i+(dx<0?1:-1));sx=null})}
/* estimate form -> prefilled text message */
$$('form[data-sms]').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(f);
 if(!d.get('name')||!d.get('phone')){f.reportValidity();return}
 const body=`Hi, I'd like a free estimate.\nName: ${d.get('name')}\nPhone: ${d.get('phone')}\nWhere: ${d.get('where')||'-'}\nService: ${d.get('svc')}\n${d.get('msg')||''}`;
 location.href=`sms:${f.dataset.sms}?&body=${encodeURIComponent(body)}`}));
/* demo pill */
const dm=$('.demo');if(dm){if(sessionStorage.getItem('fst-demo'))dm.classList.add('hide');$('button',dm).addEventListener('click',()=>{dm.classList.add('hide');sessionStorage.setItem('fst-demo','1')})}
})();
