
(function(){
  // header: transparent over the hero, solid after
  var hd=document.querySelector('header.top'), hero=document.querySelector('.hero');
  function onScroll(){ if(!hero){return;} hd.classList.toggle('solid', window.scrollY > hero.offsetHeight - hd.offsetHeight); }
  onScroll(); addEventListener('scroll', onScroll, {passive:true});

  // hover previews
  var canHover = matchMedia('(hover:hover)').matches;
  document.querySelectorAll('.tile').forEach(function(t){
    var v=t.querySelector('video'); if(!v||!canHover) return;
    t.addEventListener('mouseenter', function(){
      if(!v.getAttribute('src')){ v.setAttribute('src', v.dataset.src); v.load(); }
      var p=v.play(); if(p&&p.then){ p.then(function(){ t.classList.add('playing'); }).catch(function(){}); } else { t.classList.add('playing'); }
    });
    t.addEventListener('mouseleave', function(){ t.classList.remove('playing'); v.pause(); try{ v.currentTime=0; }catch(e){} });
  });

  // reveal on scroll
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }); },{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });
  } else { document.querySelectorAll('.reveal').forEach(function(el){ el.classList.add('in'); }); }

  // lightbox
  var cells=[].slice.call(document.querySelectorAll('.gallery .cell'));
  if(cells.length){
    var lb=document.createElement('div'); lb.className='lb';
    lb.innerHTML='<button class="x" aria-label="Close">×</button><button class="prev" aria-label="Previous">‹</button><img alt=""><button class="next" aria-label="Next">›</button>';
    document.body.appendChild(lb);
    var im=lb.querySelector('img'), i=0;
    function show(n){ i=(n+cells.length)%cells.length; im.src=cells[i].dataset.full; lb.classList.add('open'); document.body.style.overflow='hidden'; }
    function hide(){ lb.classList.remove('open'); document.body.style.overflow=''; }
    cells.forEach(function(c,n){ c.addEventListener('click', function(){ show(n); }); });
    lb.querySelector('.x').onclick=hide; lb.querySelector('.prev').onclick=function(e){e.stopPropagation();show(i-1);} ; lb.querySelector('.next').onclick=function(e){e.stopPropagation();show(i+1);};
    lb.addEventListener('click', function(e){ if(e.target===lb||e.target===im) hide(); });
    addEventListener('keydown', function(e){ if(!lb.classList.contains('open')) return; if(e.key==='Escape') hide(); if(e.key==='ArrowRight') show(i+1); if(e.key==='ArrowLeft') show(i-1); });
  }

  // contact form -> mail client
  var f=document.querySelector('form.contact-form');
  if(f){ f.addEventListener('submit', function(e){
    e.preventDefault();
    var b='Name: '+f.first.value+' '+f.last.value+'\nEmail: '+f.email.value+'\nPhone: '+f.phone.value+'\n\n'+f.message.value;
    location.href='mailto:gala.kaplun@gmail.com?subject='+encodeURIComponent('Website contact from '+f.first.value)+'&body='+encodeURIComponent(b);
  }); }
})();
