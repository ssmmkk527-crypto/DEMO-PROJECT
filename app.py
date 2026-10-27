
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="왁뿌볼", page_icon="🟡", layout="centered")

HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
body{margin:0;padding:12px;background:#fff8ef;color:#49382e;font-family:Arial,sans-serif}
h1{text-align:center;margin:5px 0;font-size:32px}
.subtitle{text-align:center;color:#92796b;margin-bottom:15px}
.panel{background:white;border:2px solid #efdfd2;border-radius:18px;padding:14px;margin-bottom:12px}
.hidden{display:none!important}
.names,.scores{display:grid;grid-template-columns:1fr 1fr;gap:10px}
label{font-size:13px;color:#8c7467;display:block;margin-bottom:5px}
input{width:100%;padding:10px;border:1px solid #e6d4c7;border-radius:10px;font-size:16px}
button{border:0;border-radius:11px;padding:11px 13px;background:#8055c7;color:white;font-weight:bold;font-size:14px;cursor:pointer}
.secondary{background:#eee4dc;color:#5c493d}
.selected{outline:3px solid #76519e;outline-offset:1px}
.toolbar{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0}
.toolbar button{flex:1;min-width:65px}
.status{text-align:center;font-weight:bold;font-size:19px;margin:8px 0}
.small{text-align:center;color:#9b8274;font-size:13px;line-height:1.5}
canvas{display:block;width:100%;height:auto;border-radius:14px;touch-action:none}
#drawCanvas{background:#fffdf9;border:1px solid #eaded2}
#ballCanvas{max-width:440px;margin:auto;cursor:pointer}
.scorebox{background:#fff6ed;padding:10px;border-radius:12px;text-align:center}
.score{font-size:26px;font-weight:bold}
.palette{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:9px 0 14px}
.color-option{height:36px;min-width:0!important;padding:0;border:3px solid white;box-shadow:0 0 0 1px #e5d8cd}
.color-option.selected{box-shadow:0 0 0 3px #76519e}
.choice-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin:8px 0 14px}
.choice-grid button{padding:10px 4px}
.section-title{font-size:14px;font-weight:bold;margin-top:12px}
.big-button{width:100%;padding:16px;font-size:18px;background:#8055c7}
.center{text-align:center}
</style>
</head>
<body>

<!-- 첫 화면 -->
<div id="homePage">
  <h1>🟡 왁뿌볼</h1>
  <div class="subtitle">내 그림이 그려진 왁스볼을 직접 으깨 봐!</div>
  <div class="panel">
    <div class="names">
      <div><label>플레이어 1</label><input id="name1" value="플레이어 1" maxlength="14"></div>
      <div><label>플레이어 2</label><input id="name2" value="플레이어 2" maxlength="14"></div>
    </div>
    <div style="margin-top:16px" class="small">각자 그림을 그리고 공을 3개씩 부수면 돼.</div>
    <div class="toolbar"><button class="big-button" onclick="goToDrawing()">왁뿌볼 시작하기 →</button></div>
  </div>
</div>

<!-- 그림 및 공 설정 화면 -->
<div id="drawPage" class="hidden">
  <h1>🎨 그림 만들기</h1>
  <div class="panel">
    <div class="status" id="drawTitle">플레이어 1의 그림</div>
    <div class="small">그림을 그리고 공의 모양과 색깔을 선택해.</div>
    <div class="toolbar">
      <button id="penBtn" class="selected" onclick="setTool('pen')">✏️ 그리기</button>
      <button id="eraserBtn" class="secondary" onclick="setTool('eraser')">지우개</button>
      <button class="secondary" onclick="undoStroke()">한 획 취소</button>
      <button class="secondary" onclick="clearDrawing()">전체 지우기</button>
    </div>
    <div class="small">그림 색깔</div>
    <div class="palette" id="drawPalette"></div>
    <canvas id="drawCanvas" width="800" height="420"></canvas>

    <div class="section-title">① 공 모양 선택</div>
    <div class="choice-grid" id="shapeChoices">
      <button class="selected" onclick="setShape('circle',this)">⚪ 동그라미</button>
      <button onclick="setShape('heart',this)">💗 하트</button>
      <button onclick="setShape('star',this)">⭐ 별</button>
      <button onclick="setShape('egg',this)">🥚 달걀</button>
      <button onclick="setShape('lemon',this)">🍋 레몬</button>
    </div>

    <div class="section-title">② 공 색깔 선택</div>
    <div class="palette" id="ballPalette"></div>

    <div class="toolbar"><button class="big-button" onclick="finishDrawing()">그림 완성하고 왁뿌볼로 →</button></div>
    <div class="small" id="drawingOrder">플레이어 1이 먼저 그림을 그려.</div>
  </div>
</div>

<!-- 실제 왁뿌볼 게임 화면 -->
<div id="gamePage" class="hidden">
  <h1>🟡 왁뿌볼</h1>
  <div class="panel">
    <div class="scores">
      <div class="scorebox"><div id="scoreName1">플레이어 1</div><div class="score" id="score1">0</div></div>
      <div class="scorebox"><div id="scoreName2">플레이어 2</div><div class="score" id="score2">0</div></div>
    </div>
  </div>
  <div class="panel">
    <div class="status" id="turnTitle"></div>
    <div class="small" id="turnHint">공을 눌러서 부숴 봐!</div>
    <div class="center" style="margin:8px 0"><b id="attemptText">1 / 3</b></div>
    <canvas id="ballCanvas" width="440" height="440"></canvas>
    <div class="small" id="ballHint">공을 눌러 봐!</div>
  </div>
</div>

<!-- 결과 화면 -->
<div id="finalPage" class="hidden">
  <h1>🏆 게임 종료!</h1>
  <div class="panel center">
    <h2 id="winner"></h2>
    <p id="finalScore"></p>
    <button class="big-button" onclick="restart()">다시 하기</button>
  </div>
</div>

<script>
const drawCanvas=document.getElementById('drawCanvas');
const dctx=drawCanvas.getContext('2d');
const ballCanvas=document.getElementById('ballCanvas');
const bctx=ballCanvas.getContext('2d');

let drawings=[[],[]];
let playerShapes=['circle','circle'];
let playerColors=['#f3c969','#a8d5bd'];
let currentDrawingPlayer=0;
let strokes=[],activeStroke=null,isDrawing=false,drawingDone=false;
let tool='pen',color='#49382e';
let turn=0,scores=[0,0],busy=false,crushed=false;
let audioCtx=null,pressMark=null,dentProgress=0,crackProgress=0,breakProgress=0;
let ballShape='circle',ballColor='#f3c969',animationId=null;

const inkColors=['#49382e','#d95f59','#e78c53','#e9bd4f','#78ad77','#4c9c91','#5798c9','#626cbd','#9974b7','#d78ca7','#a77c62','#777777'];
const waxColors=[
{name:'버터 옐로',value:'#f3c969'},{name:'피치',value:'#efb19a'},
{name:'로즈 핑크',value:'#e9a5ba'},{name:'라벤더',value:'#b9a8df'},
{name:'민트',value:'#a8d5bd'},{name:'스카이 블루',value:'#a6c9e9'},
{name:'크림',value:'#f1dfb6'},{name:'세이지',value:'#b9c4a0'},
{name:'코랄',value:'#e98978'},{name:'웜 그레이',value:'#c7beb5'},
{name:'라일락',value:'#d1b9d8'},{name:'아이스 블루',value:'#c2e0e4'}
];

function playerName(i){
 return document.getElementById('name'+(i+1)).value.trim()||('플레이어 '+(i+1));
}
function updateNames(){
 document.getElementById('scoreName1').textContent=playerName(0);
 document.getElementById('scoreName2').textContent=playerName(1);
}
document.getElementById('name1').addEventListener('input',updateNames);
document.getElementById('name2').addEventListener('input',updateNames);

function showPage(id){
 ['homePage','drawPage','gamePage','finalPage'].forEach(p=>document.getElementById(p).classList.add('hidden'));
 document.getElementById(id).classList.remove('hidden');
}
function goToDrawing(){
 currentDrawingPlayer=0;
 strokes=[];drawingDone=false;
 document.getElementById('drawTitle').textContent=playerName(0)+'의 그림';
 document.getElementById('drawingOrder').textContent='플레이어 1이 먼저 그림을 그려.';
 refreshSettings();buildDrawPalette();renderDrawing();
 showPage('drawPage');
}

function makePalette(elementId,items,onPick,selectedValue){
 const el=document.getElementById(elementId);el.innerHTML='';
 items.forEach(item=>{
   const value=typeof item==='string'?item:item.value;
   const name=typeof item==='string'?item:item.name;
   const b=document.createElement('button');
   b.className='color-option'+(value===selectedValue?' selected':'');
   b.style.background=value;b.title=name;b.setAttribute('aria-label',name);
   b.onclick=()=>{
     el.querySelectorAll('button').forEach(x=>x.classList.remove('selected'));
     b.classList.add('selected');onPick(value);
   };
   el.appendChild(b);
 });
}
function buildDrawPalette(){
 makePalette('drawPalette',inkColors,v=>{color=v;setTool('pen')},color);
}
function buildBallPalette(){
 makePalette('ballPalette',waxColors,v=>{playerColors[currentDrawingPlayer]=v},playerColors[currentDrawingPlayer]);
}
function setTool(t){
 tool=t;
 document.getElementById('penBtn').classList.toggle('selected',t==='pen');
 document.getElementById('eraserBtn').classList.toggle('selected',t==='eraser');
}
function setShape(s,el){
 playerShapes[currentDrawingPlayer]=s;
 document.querySelectorAll('#shapeChoices button').forEach(b=>b.classList.remove('selected'));
 el.classList.add('selected');
}
function refreshSettings(){
 document.querySelectorAll('#shapeChoices button').forEach(b=>b.classList.remove('selected'));
 const idx=['circle','heart','star','egg','lemon'].indexOf(playerShapes[currentDrawingPlayer]);
 const buttons=document.querySelectorAll('#shapeChoices button');
 if(buttons[idx])buttons[idx].classList.add('selected');
 buildBallPalette();
}
function pointerPos(canvas,e){
 const r=canvas.getBoundingClientRect();
 return {x:(e.clientX-r.left)*canvas.width/r.width,y:(e.clientY-r.top)*canvas.height/r.height};
}
function drawBackground(){
 dctx.fillStyle='#fffdf9';dctx.fillRect(0,0,800,420);
}
function paintStroke(ctx,s){
 if(!s||!s.points.length)return;
 ctx.save();ctx.lineCap='round';ctx.lineJoin='round';
 if(s.tool==='eraser'){
   ctx.globalCompositeOperation='destination-out';ctx.strokeStyle='rgba(0,0,0,1)';
 }else{
   ctx.globalCompositeOperation='source-over';ctx.strokeStyle=s.color;
 }
 ctx.lineWidth=s.tool==='eraser'?34:s.width;
 ctx.beginPath();ctx.moveTo(s.points[0].x,s.points[0].y);
 for(let i=1;i<s.points.length;i++)ctx.lineTo(s.points[i].x,s.points[i].y);
 if(s.points.length===1)ctx.lineTo(s.points[0].x+.1,s.points[0].y+.1);
 ctx.stroke();ctx.restore();
}
function renderDrawing(){
 drawBackground();strokes.forEach(s=>paintStroke(dctx,s));
 if(activeStroke)paintStroke(dctx,activeStroke);
}
drawCanvas.addEventListener('pointerdown',e=>{
 if(drawingDone)return;
 isDrawing=true;drawCanvas.setPointerCapture(e.pointerId);
 activeStroke={color,tool,width:7,points:[pointerPos(drawCanvas,e)]};renderDrawing();
});
drawCanvas.addEventListener('pointermove',e=>{
 if(!isDrawing||!activeStroke)return;
 activeStroke.points.push(pointerPos(drawCanvas,e));renderDrawing();
});
function endDraw(){
 if(!isDrawing)return;
 isDrawing=false;if(activeStroke)strokes.push(activeStroke);
 activeStroke=null;renderDrawing();
}
drawCanvas.addEventListener('pointerup',endDraw);
drawCanvas.addEventListener('pointercancel',endDraw);
function clearDrawing(){if(!drawingDone){strokes=[];activeStroke=null;renderDrawing();}}
function undoStroke(){if(!drawingDone){strokes.pop();renderDrawing();}}

function finishDrawing(){
 if(isDrawing)endDraw();
 drawings[currentDrawingPlayer]=JSON.parse(JSON.stringify(strokes));
 drawingDone=true;
 if(currentDrawingPlayer===0){
   currentDrawingPlayer=1;
   strokes=[];activeStroke=null;drawingDone=false;
   document.getElementById('drawTitle').textContent=playerName(1)+'의 그림';
   document.getElementById('drawingOrder').textContent='플레이어 1 완료! 이제 플레이어 2가 그림과 공을 설정해.';
   refreshSettings();buildDrawPalette();renderDrawing();
 }else{
   turn=0;scores=[0,0];updateScore();
   showPage('gamePage');prepareBall();
 }
}

function shapePath(ctx,shape,cx,cy,r){
 ctx.beginPath();
 if(shape==='circle')ctx.arc(cx,cy,r,0,Math.PI*2);
 else if(shape==='heart'){
   ctx.moveTo(cx,cy+r*.75);
   ctx.bezierCurveTo(cx-r*1.3,cy,cx-r*.85,cy-r*1.2,cx,cy-r*.45);
   ctx.bezierCurveTo(cx+r*.85,cy-r*1.2,cx+r*1.3,cy,cx,cy+r*.75);
 }else if(shape==='star'){
   for(let i=0;i<10;i++){
     const a=-Math.PI/2+i*Math.PI/5,rr=i%2===0?r:r*.48;
     const x=cx+Math.cos(a)*rr,y=cy+Math.sin(a)*rr;
     if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
   }ctx.closePath();
 }else if(shape==='egg'){
   ctx.moveTo(cx,cy-r);
   ctx.bezierCurveTo(cx+r*.95,cy-r*.95,cx+r*.95,cy+r*.65,cx,cy+r);
   ctx.bezierCurveTo(cx-r*.95,cy+r*.65,cx-r*.95,cy-r*.95,cx,cy-r);
 }else{
   ctx.moveTo(cx-r*.8,cy-r*.45);
   ctx.quadraticCurveTo(cx-r*1.15,cy,cx-r*.55,cy+r*.65);
   ctx.quadraticCurveTo(cx,cy+r*1.05,cx+r*.55,cy+r*.65);
   ctx.quadraticCurveTo(cx+r*1.15,cy,cx+r*.8,cy-r*.45);
   ctx.quadraticCurveTo(cx,cy-r*.9,cx-r*.8,cy-r*.45);
 }
 ctx.closePath();
}
function paintStoredDrawing(ctx,player,shape,cx,cy,r){
 const temp=document.createElement('canvas');temp.width=800;temp.height=420;
 const tc=temp.getContext('2d');tc.clearRect(0,0,800,420);
 drawings[player].forEach(s=>paintStroke(tc,s));
 ctx.save();shapePath(ctx,shape,cx,cy,r);ctx.clip();
 ctx.drawImage(temp,cx-r*.9,cy-r*.72,r*1.8,r*1.44);ctx.restore();
}
function drawBall(){
 const ctx=bctx,cx=220,cy=220,r=154;
 ctx.clearRect(0,0,440,440);
 ctx.fillStyle='rgba(75,45,30,.15)';
 ctx.beginPath();ctx.ellipse(cx+4,cy+r*.92,r*.78,r*.17,0,0,Math.PI*2);ctx.fill();

 ctx.save();
 ctx.translate(cx,cy);
 ctx.scale(1-dentProgress*.055,1-dentProgress*.07);
 ctx.translate(-cx,-cy);
 shapePath(ctx,ballShape,cx,cy,r);
 const grad=ctx.createRadialGradient(cx-r*.42,cy-r*.48,r*.06,cx,cy,r*1.18);
 grad.addColorStop(0,'#fff9e8');grad.addColorStop(.2,ballColor);
 grad.addColorStop(.76,ballColor);grad.addColorStop(1,'#927052');
 ctx.fillStyle=grad;ctx.fill();ctx.clip();
 for(let i=0;i<80;i++){
   const x=cx+Math.sin(i*78.13)*r*.8,y=cy+Math.cos(i*31.77)*r*.8;
   ctx.fillStyle=i%2?'rgba(255,255,255,.055)':'rgba(100,65,45,.035)';
   ctx.beginPath();ctx.arc(x,y,1+i%2,0,Math.PI*2);ctx.fill();
 }
 paintStoredDrawing(ctx,turn<3?0:1,ballShape,cx,cy,r*.82);

 if(pressMark&&dentProgress>0){
   const px=pressMark.x,py=pressMark.y,rr=38+dentProgress*27;
   ctx.save();ctx.translate(px,py);ctx.scale(1+dentProgress*.2,1-dentProgress*.36);
   const hollow=ctx.createRadialGradient(-5,-8,2,0,0,rr*1.45);
   hollow.addColorStop(0,`rgba(56,29,22,${.9*dentProgress})`);
   hollow.addColorStop(.38,`rgba(87,44,29,${.85*dentProgress})`);
   hollow.addColorStop(.68,`rgba(134,76,43,${.7*dentProgress})`);
   hollow.addColorStop(.86,`rgba(255,218,154,${.8*dentProgress})`);
   hollow.addColorStop(1,'rgba(255,255,255,0)');
   ctx.fillStyle=hollow;ctx.beginPath();ctx.ellipse(0,0,rr*1.3,rr,0,0,Math.PI*2);ctx.fill();

   const rays=[-2.4,-1.6,-.7,.25,1.3,2.35,3.05];
   rays.forEach((a,i)=>{
     const p=Math.max(0,Math.min(1,(crackProgress-i*.07)/.65));if(p<=0)return;
     const len=rr*(1.15+(i%3)*.18)*p;
     ctx.strokeStyle=`rgba(69,37,26,${.95*p})`;ctx.lineWidth=3.5*p;
     ctx.beginPath();ctx.moveTo(Math.cos(a)*rr*.2,Math.sin(a)*rr*.2);
     ctx.lineTo(Math.cos(a+.12)*len*.48,Math.sin(a+.12)*len*.48);
     ctx.lineTo(Math.cos(a-.06)*len,Math.sin(a-.06)*len);ctx.stroke();
     ctx.lineTo(Math.cos(a-.6)*len*.7,Math.sin(a-.6)*len*.7);ctx.stroke();
   });
   ctx.restore();
 }
 ctx.restore();

 // 표면이 여러 방향으로 벌어져 갈라지는 효과
 if(breakProgress>0){
   const p=breakProgress;
   const lines=[[-1,-1,1,-.1],[-.7,-.9,-.1,1],[.3,-1,1,.5],[-1,.2,.2,1],[.2,.1,1,1]];
   ctx.save();ctx.lineCap='round';
   lines.forEach((v,i)=>{
     const cx1=220+v[0]*45,cy1=220+v[1]*45;
     const cx2=220+v[2]*130,cy2=220+v[3]*130;
     ctx.strokeStyle='#68402e';ctx.lineWidth=7*p;
     ctx.beginPath();ctx.moveTo(cx1,cy1);ctx.lineTo(cx2,cy2);ctx.stroke();
     ctx.strokeStyle='rgba(255,232,183,.9)';ctx.lineWidth=2*p;
     ctx.beginPath();ctx.moveTo(cx1-2,cy1-2);ctx.lineTo(cx2-2,cy2-2);ctx.stroke();
   });
   ctx.restore();
 }
 ctx.save();shapePath(ctx,ballShape,cx,cy,r);ctx.clip();
 const shine=ctx.createRadialGradient(cx-r*.4,cy-r*.52,2,cx-r*.32,cy-r*.43,r*.48);
 shine.addColorStop(0,'rgba(255,255,255,.72)');shine.addColorStop(1,'rgba(255,255,255,0)');
 ctx.fillStyle=shine;ctx.beginPath();ctx.ellipse(cx-r*.32,cy-r*.42,r*.4,r*.28,-.6,0,Math.PI*2);ctx.fill();
 ctx.restore();
}
function playCrunch(){
 try{
   if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();
   if(audioCtx.state==='suspended')audioCtx.resume();
   const ctx=audioCtx,now=ctx.currentTime;
   for(let i=0;i<7;i++){
     const start=now+i*.035,duration=.07+Math.random()*.05;
     const buffer=ctx.createBuffer(1,Math.floor(ctx.sampleRate*duration),ctx.sampleRate);
     const data=buffer.getChannelData(0);
     for(let j=0;j<data.length;j++)data[j]=(Math.random()*2-1)*(1-j/data.length);
     const src=ctx.createBufferSource();src.buffer=buffer;
     const filter=ctx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=450+Math.random()*850;
     const gain=ctx.createGain();
     gain.gain.setValueAtTime(.0001,start);gain.gain.exponentialRampToValueAtTime(.22,start+.008);
     gain.gain.exponentialRampToValueAtTime(.0001,start+duration);
     src.connect(filter);filter.connect(gain);gain.connect(ctx.destination);
     src.start(start);src.stop(start+duration);
   }
   const osc=ctx.createOscillator(),gain=ctx.createGain();
   osc.type='triangle';osc.frequency.setValueAtTime(100,now);
   osc.frequency.exponentialRampToValueAtTime(38,now+.24);
   gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(.18,now+.012);
   gain.gain.exponentialRampToValueAtTime(.0001,now+.26);
   osc.connect(gain);gain.connect(ctx.destination);osc.start(now);osc.stop(now+.27);
 }catch(e){}
}
function updateScore(){
 document.getElementById('score1').textContent=scores[0];
 document.getElementById('score2').textContent=scores[1];updateNames();
}
function prepareBall(){
 busy=false;crushed=false;pressMark=null;
 dentProgress=0;crackProgress=0;breakProgress=0;
 const player=turn<3?0:1;
 ballShape=playerShapes[player];ballColor=playerColors[player];
 document.getElementById('turnTitle').textContent=playerName(player)+' 차례';
 document.getElementById('attemptText').textContent=(turn%3+1)+' / 3';
 document.getElementById('turnHint').textContent=playerName(player)+'이 선택한 공이야!';
 document.getElementById('ballHint').textContent='공을 눌러서 깨뜨려 봐!';
 drawBall();
}
function beginPlayerTwo(){
 currentDrawingPlayer=1;strokes=[];activeStroke=null;drawingDone=false;
 document.getElementById('drawTitle').textContent=playerName(1)+'의 그림';
 document.getElementById('drawingOrder').textContent='플레이어 1 차례 완료! 플레이어 2가 그림을 그려.';
 refreshSettings();buildDrawPalette();renderDrawing();showPage('drawPage');
}
function showFinal(){
 showPage('finalPage');
 document.getElementById('winner').textContent=
   scores[0]>scores[1]?playerName(0)+' 승리! 🎉':
   scores[1]>scores[0]?playerName(1)+' 승리! 🎉':'무승부! 🤝';
 document.getElementById('finalScore').textContent=
   playerName(0)+' '+scores[0]+'점 · '+playerName(1)+' '+scores[1]+'점';
}
function crush(event){
 if(busy||crushed)return;
 const p=pointerPos(ballCanvas,event);
 bctx.save();shapePath(bctx,ballShape,220,220,154);
 const inside=bctx.isPointInPath(p.x,p.y);bctx.restore();if(!inside)return;
 playCrunch();busy=true;crushed=true;pressMark=p;
 const start=performance.now(),duration=1050;
 function animate(now){
   const t=Math.min(1,(now-start)/duration);
   dentProgress=Math.min(1,t/.32);
   crackProgress=Math.max(0,Math.min(1,(t-.12)/.55));
   breakProgress=Math.max(0,Math.min(1,(t-.68)/.32));
   drawBall();
   if(t<1)animationId=requestAnimationFrame(animate);
   else{
     scores[turn<3?0:1]++;updateScore();
     document.getElementById('ballHint').textContent='와그작! 공이 깨졌어!';
     setTimeout(()=>{
       turn++;
       if(turn===3)beginPlayerTwo();
       else if(turn>=6)showFinal();
       else prepareBall();
     },500);
   }
 }
 animationId=requestAnimationFrame(animate);
}
ballCanvas.addEventListener('pointerdown',crush);

function restart(){
 if(animationId)cancelAnimationFrame(animationId);
 drawings=[[],[]];playerShapes=['circle','circle'];
 playerColors=['#f3c969','#a8d5bd'];strokes=[];activeStroke=null;
 currentDrawingPlayer=0;drawingDone=false;turn=0;scores=[0,0];busy=false;crushed=false;
 goToDrawing();updateScore();
}
buildDrawPalette();refreshSettings();renderDrawing();updateNames();
</script>
</body>
</html>
"""

components.html(HTML, height=1250, scrolling=False)
