var busy=false;
function finish(id,f,size,st,res){
  var p=Math.round((1-size/f.size)*100),u="/result/"+id+"?c="+CODE;
  st.textContent="";
  var s=document.createElement("div");s.className=p>0?"good":"err";
  s.textContent=fmt(f.size)+" ← "+fmt(size)+(p>0?"  (وفّرت "+p+"%)":"  (الحجم صار أكبر، جرّب جودة أقل)");
  var v=document.createElement("video");v.controls=true;v.playsInline=true;v.src=u;
  var l=document.createElement("a");l.className="dl";l.href=u;l.textContent="حفظ الفيديو";
  res.appendChild(s);res.appendChild(v);res.appendChild(l);
}
function poll(id,f,st,res,end){
  fetch("/status/"+id+"?c="+CODE).then(function(r){return r.json()}).then(function(j){
    if(j.state==="run"){
      st.textContent="جاري الضغط على السيرفر... "+j.pct+"%";
      setTimeout(function(){poll(id,f,st,res,end)},3000);
    }else if(j.state==="done"){finish(id,f,j.size,st,res);end()}
    else{
      st.className="st err";
      st.textContent=j.state==="gone"?"انتهت العملية، أعد المحاولة":"فشل الضغط، جرّب فيديو ثاني";
      end();
    }
  }).catch(function(){setTimeout(function(){poll(id,f,st,res,end)},5000)});
}
function start(f,d,btn){
  if(busy){alert("استنى لين يخلص الفيديو الحالي");return}
  busy=true;btn.disabled=true;
  var st=d.querySelector(".st"),res=d.querySelector(".res");
  st.className="st";res.textContent="";
  var fd=new FormData();
  fd.append("file",f);fd.append("q",$("q").value);
  fd.append("mh",$("mh").value);fd.append("pr",$("pr").value);
  var x=new XMLHttpRequest();
  x.open("POST","/upload");x.setRequestHeader("X-Code",CODE);
  function end(){busy=false;btn.disabled=false}
  x.upload.onprogress=function(e){
    if(e.lengthComputable)st.textContent="جاري رفع الفيديو... "+Math.round(e.loaded/e.total*100)+"%";
  };
  x.onload=function(){
    if(x.status!==200){st.className="st err";st.textContent="تعذر رفع الفيديو (خطأ "+x.status+")";end();return}
    var id=JSON.parse(x.responseText).id;
    st.textContent="جاري الضغط على السيرفر... 0%";
    poll(id,f,st,res,end);
  };
  x.onerror=function(){st.className="st err";st.textContent="انقطع الاتصال أثناء الرفع، جرّب مرة ثانية";end()};
  x.send(fd);
}
$("file").onchange=function(e){
  Array.prototype.forEach.call(e.target.files,function(f){
    var d=document.createElement("div");d.className="card";
    d.innerHTML='<div class="nm"></div><div class="sz"></div><div class="st"></div><div class="res"></div><div class="act"></div>';
    d.querySelector(".nm").textContent=f.name;
    d.querySelector(".sz").textContent=fmt(f.size);
    var b=document.createElement("button");b.textContent="ابدأ الضغط";
    b.onclick=function(){start(f,d,b)};
    d.querySelector(".act").appendChild(b);
    $("list").appendChild(d);
  });
  e.target.value="";
};
