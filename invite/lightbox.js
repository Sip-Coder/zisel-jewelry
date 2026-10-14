/* Zisel lightbox: swipe, arrows, keys, captions, counter, wrap-around, neighbor preload.
   Usage: ZLB.init([{el, src, cap}, ...]) — clicking el opens at that index. */
(function(){
const css=`.zlbx{position:fixed;inset:0;z-index:1000;background:rgba(4,10,26,.95);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity .25s,visibility .25s;touch-action:pan-y;-webkit-user-select:none;user-select:none}
.zlbx.on{opacity:1;visibility:visible}
.zlbx .st{position:relative;display:flex;align-items:center;justify-content:center;width:100%;flex:1 1 auto;min-height:0;padding:56px 64px 8px}
.zlbx figure{margin:0;display:flex;flex-direction:column;align-items:center;max-width:100%;max-height:100%;transition:transform .25s ease,opacity .25s ease}
.zlbx .fr{padding:5px;background:linear-gradient(135deg,#7a5a14,#c99a3a 18%,#fff1b8 32%,#d8b35a 46%,#8f6b1e 60%,#e8c870 76%,#fff5cc 88%,#a97d25);box-shadow:0 20px 60px rgba(0,0,0,.6);line-height:0}
.zlbx img{display:block;max-width:min(92vw,1100px);max-height:calc(100svh - 190px);object-fit:contain;background:#0d1f45}
.zlbx figcaption{display:none!important;margin-top:14px;text-align:center;color:#fff;font:500 clamp(16px,2.2vw,20px)/1.3 "ZPlay","Playfair Display",Georgia,serif;letter-spacing:.02em;padding:0 12px}
.zlbx .ct{margin-top:6px;color:#e9cf7a;font:600 12px/1 "ZSans",Montserrat,system-ui,sans-serif;letter-spacing:.25em}
.zlbx button{position:absolute;background:rgba(13,31,69,.7);color:#e9cf7a;border:1px solid rgba(233,207,122,.7);border-radius:50%;width:48px;height:48px;font-size:26px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}
.zlbx button:hover{background:rgba(233,207,122,.2)}
.zlbx .x{top:12px;right:12px;font-size:30px}.zlbx .pv{left:10px;top:50%;transform:translateY(-50%)}.zlbx .nx{right:10px;top:50%;transform:translateY(-50%)}
@media (max-width:640px){.zlbx .st{padding:60px 8px 8px}.zlbx .pv,.zlbx .nx{top:auto;bottom:18px;transform:none;width:44px;height:44px}.zlbx .pv{left:calc(50% - 64px)}.zlbx .nx{right:calc(50% - 64px)}.zlbx{padding-bottom:72px}.zlbx img{max-height:calc(100svh - 230px)}}`;
let items=[],i=0,box,img,cap,ct,fig,cache={};
function build(){
  const s=document.createElement('style');s.textContent=css;document.head.appendChild(s);
  box=document.createElement('div');box.className='zlbx';box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-label','Photo viewer');
  box.innerHTML='<div class="st"><figure><div class="fr"><img alt=""></div><figcaption></figcaption><div class="ct"></div></figure></div><button class="pv" aria-label="Previous photo">‹</button><button class="nx" aria-label="Next photo">›</button><button class="x" aria-label="Close">×</button>';
  document.body.appendChild(box);img=box.querySelector('img');cap=box.querySelector('figcaption');ct=box.querySelector('.ct');fig=box.querySelector('figure');
  box.querySelector('.pv').onclick=e=>{e.stopPropagation();go(-1)};box.querySelector('.nx').onclick=e=>{e.stopPropagation();go(1)};box.querySelector('.x').onclick=close;
  box.addEventListener('click',e=>{if(e.target===box||e.target.classList.contains('st'))close()});
  document.addEventListener('keydown',e=>{if(!box.classList.contains('on'))return;if(e.key==='ArrowRight'){go(1);e.preventDefault()}else if(e.key==='ArrowLeft'){go(-1);e.preventDefault()}else if(e.key==='Escape')close()});
  let sx=0,sy=0,dx=0,t=false;
  box.addEventListener('touchstart',e=>{if(e.touches.length!==1)return;sx=e.touches[0].clientX;sy=e.touches[0].clientY;dx=0;t=true;fig.style.transition='none'},{passive:true});
  box.addEventListener('touchmove',e=>{if(!t)return;dx=e.touches[0].clientX-sx;const dy=e.touches[0].clientY-sy;if(Math.abs(dx)>Math.abs(dy))fig.style.transform=`translateX(${dx}px)`},{passive:true});
  box.addEventListener('touchend',()=>{if(!t)return;t=false;fig.style.transition='';fig.style.transform='';if(Math.abs(dx)>50)go(dx<0?1:-1)});
}
function pre(k){const s=items[(k+items.length)%items.length].src;if(!cache[s]){cache[s]=new Image();cache[s].src=s}}
function show(){const it=items[i];img.src=it.src;img.alt=it.cap;cap.textContent=it.cap;ct.textContent=`${i+1} / ${items.length}`;pre(i+1);pre(i-1)}
function go(d){i=(i+d+items.length)%items.length;fig.style.opacity=0;setTimeout(()=>{show();fig.style.opacity=1},120)}
function open(k){i=k;show();box.classList.add('on');document.documentElement.style.overflow='hidden';box.querySelector('.x').focus({preventScroll:true})}
function close(){box.classList.remove('on');document.documentElement.style.overflow=''}
window.ZLB={init(list){if(!box)build();items=list;list.forEach((it,k)=>{it.el.style.cursor='zoom-in';it.el.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();open(k)})})},open,go,close};
})();
