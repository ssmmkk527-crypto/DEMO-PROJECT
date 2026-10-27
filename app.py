import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="왁뿌볼", page_icon="🫧")
st.title("🫧 왁뿌볼")
st.write("그림을 그리고 나만의 왁뿌볼을 만들어 보세요!")

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
body {font-family:Arial,sans-serif;background:#fff7fc;color:#754866}
.box {background:white;padding:15px;border-radius:18px}
canvas {width:100%;border-radius:15px;touch-action:none}
button,select,input {
  padding:10px;border:0;border-radius:10px;margin:3px;
}
button {background:#ed78b1;color:white;font-weight:bold;cursor:pointer}
.secondary {background:#eee3f3;color:#754866}
.row {display:flex;gap:6px;flex-wrap:wrap}
.row button {flex:1}
.score {display:flex;gap:10px;text-align:center}
.score div {flex:1;background:#fff0f7;padding:10px;border-radius:12px}
strong {font-size:24px;color:#d34d91}
</style>
</head>
<body>
<div class="box">
  <div class="row">
    <input id="p1" value="나" placeholder="플레이어 1">
    <input id="p2" value="친구" placeholder="플레이어 2">
  </div>

  <p>왁스 색깔</p>
  <select id="color">
    <option value="#f178b0">딸기 핑크</option>
    <option value="#68bde8">소다 블루</option>
    <option value="#a98be8">포도 보라</option>
    <option value="#68cfb5">민트</option>
    <option value="#f1c94f">레몬 옐로</option>
    <option value="#f49b6c">복숭아 오렌지</option>
  </select>

  <div class="score">
    <div><span id="name1">나</span><br><strong id="s1">0</strong></div>
    <div><span id="name2">친구</span><br><strong id="s2">0</strong></div>
  </div>

  <h3>1. 왁뿌볼 그림 그리기</h3>
  <canvas id="drawing" width="600" height="200"
    style="border:2px dashed #e8b9d3;background:white"></canvas>
  <div class="row">
    <button class="secondary" id="clearDrawing">그림 지우기</button>
    <button id="makeBall">이 그림으로 공 만들기</button>
  </div>

  <h3>2. 왁뿌볼 부수기</h3>
  <canvas id="game" width="600" height="330"></canvas>
  <p id="turn" style="text-align:center">나 차례!</p>
  <div class="row">
    <button id="crush">💥 와그작 부수기</button>
    <button class="secondary" id="sound">🔊 소리 켜짐</button>
  </div>
  <div class="row">
    <button class="secondary" id="reset">↻ 점수·공 리셋</button>
    <button class="secondary" id="resetAll">전체 처음부터</button>
  </div>
</div>

<script>
(function () {
  const $ = id => document.getElementById(id);
  const draw = $("drawing");
  const dc = draw.getContext("2d");
  const game = $("game");
  const gc = game.getContext("2d");

  let painting = false;
  let last = null;
  let customImage = null;
  let scores = [0, 0];
  let player = 0;
  let damage = 0;
  let soundOn = true;
  let audio = null;
  let pieces = [];

  function getColor() {
    return $("color").value;
  }

  function point(e) {
    const r = draw.getBoundingClientRect();
    return {
      x: (e.clientX - r.left) * draw.width / r.width,
      y: (e.clientY - r.top) * draw.height / r.height
    };
  }

  draw.addEventListener("pointerdown", e => {
    painting = true;
    last = point(e);
    draw.setPointerCapture(e.pointerId);
    dc.beginPath();
    dc.arc(last.x, last.y, 4, 0, Math.PI * 2);
    dc.fillStyle = getColor();
    dc.fill();
  });

  draw.addEventListener("pointermove", e => {
    if (!painting) return;
    const p = point(e);
    dc.beginPath();
    dc.moveTo(last.x, last.y);
    dc.lineTo(p.x, p.y);
    dc.strokeStyle = getColor();
    dc.lineWidth = 7;
    dc.lineCap = "round";
    dc.stroke();
    last = p;
  });

  function stopDrawing() {
    painting = false;
    last = null;
  }

  draw.addEventListener("pointerup", stopDrawing);
  draw.addEventListener("pointercancel", stopDrawing);

  $("clearDrawing").onclick = () => {
    dc.clearRect(0, 0, draw.width, draw.height);
  };

  $("makeBall").onclick = () => {
    customImage = new Image();
    customImage.onload = () => {
      damage = 0;
      pieces = [];
    };
    customImage.src = draw.toDataURL("image/png");
  };

  function update() {
    const n1 = $("p1").value.trim() || "플레이어 1";
    const n2 = $("p2").value.trim() || "플레이어 2";

    $("name1").textContent = n1;
    $("name2").textContent = n2;
    $("s1").textContent = scores[0];
    $("s2").textContent = scores[1];
    $("turn").textContent = (player === 0 ? n1 : n2) + " 차례!";
    $("crush").textContent =
      "💥 와그작 부수기 (" + (player === 0 ? n1 : n2) + ")";
  }

  function crunchSound() {
    if (!soundOn) return;

    try {
      if (!audio) {
        audio = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audio.state === "suspended") audio.resume();

      const now = audio.currentTime;

      for (let j = 0; j < 12; j++) {
        const duration = 0.04 + Math.random() * 0.09;
        const length = Math.floor(audio.sampleRate * duration);
        const buffer = audio.createBuffer(1, length, audio.sampleRate);
        const data = buffer.getChannelData(0);

        for (let i = 0; i < length; i++) {
          data[i] = (Math.random() * 2 - 1) *
            Math.pow(1 - i / length, 1.5);
        }

        const source = audio.createBufferSource();
        const filter = audio.createBiquadFilter();
        const gain = audio.createGain();
        const start = now + j * 0.012;

        source.buffer = buffer;
        filter.type = "highpass";
        filter.frequency.value = 500 + Math.random() * 1200;

        gain.gain.setValueAtTime(0.001, start);
        gain.gain.linearRampToValueAtTime(0.12, start + 0.005);
        gain.gain.exponentialRampToValueAtTime(
          0.001, start + duration
        );

        source.connect(filter);
        filter.connect(gain);
        gain.connect(audio.destination);
        source.start(start);
        source.stop(start + duration);
      }
    } catch (e) {
      // 브라우저에서 소리를 지원하지 않으면 게임은 계속 실행됩니다.
    }
  }

  function crush() {
    scores[player] += Math.floor(Math.random() * 91) + 10;
    player = 1 - player;
    damage = Math.min(0.85, damage + 0.18);
    crunchSound();

    for (let i = 0; i < 25; i++) {
      pieces.push({
        x: 300 + (Math.random() - 0.5) * 180,
        y: 145,
        vx: (Math.random() - 0.5) * 8,
        vy: -Math.random() * 6,
        life: 1,
        size: 4 + Math.random() * 10
      });
    }
    update();
  }

  $("crush").onclick = crush;

  $("sound").onclick = () => {
    soundOn = !soundOn;
    $("sound").textContent = soundOn ?
      "🔊 소리 켜짐" : "🔇 소리 꺼짐";
  };

  function reset() {
    scores = [0, 0];
    player = 0;
    damage = 0;
    pieces = [];
    update();
  }

  $("reset").onclick = reset;

  $("resetAll").onclick = () => {
    reset();
    customImage = null;
    dc.clearRect(0, 0, draw.width, draw.height);
  };

  $("p1").addEventListener("input", update);
  $("p2").addEventListener("input", update);

  game.addEventListener("click", crush);

  function render() {
    const w = game.width;
    const h = game.height;
    const x = w / 2;
    const y = h / 2 - 5;
    const rx = 135;
    const ry = 115;

    gc.clearRect(0, 0, w, h);

    gc.fillStyle = "rgba(100,60,100,0.15)";
    gc.beginPath();
    gc.ellipse(x, 280, 115, 12, 0, 0, Math.PI * 2);
    gc.fill();

    const gradient = gc.createRadialGradient(
      x - 40, y - 40, 5, x, y, 150
    );
    gradient.addColorStop(0, "#fff0f8");
    gradient.addColorStop(0.5, getColor());
    gradient.addColorStop(1, "#8e477a");

    gc.save();
    gc.beginPath();
    gc.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2);
    gc.clip();

    gc.fillStyle = gradient;
    gc.fillRect(x - rx, y - ry, rx * 2, ry * 2);

    if (customImage && customImage.complete &&
        customImage.naturalWidth > 0) {
      gc.drawImage(
        customImage, x - rx * 0.8, y - ry * 0.8,
        rx * 1.6, ry * 1.6
      );
    }

    if (damage > 0) {
      gc.strokeStyle = "#7e3567";
      gc.lineWidth = 4;
      for (let i = 0; i < Math.floor(damage * 12); i++) {
        const a = i * 2.4;
        const px = x + Math.cos(a) * rx * 0.65;
        const py = y + Math.sin(a) * ry * 0.65;
        gc.beginPath();
        gc.moveTo(px - 10, py - 8);
        gc.lineTo(px, py + 3);
        gc.lineTo(px + 8, py - 12);
        gc.stroke();
      }
    }
    gc.restore();

    pieces.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.15;
      p.life -= 0.018;

      gc.globalAlpha = Math.max(0, p.life);
      gc.fillStyle = getColor();
      gc.beginPath();
      gc.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      gc.fill();
      gc.globalAlpha = 1;
    });

    pieces = pieces.filter(p => p.life > 0 && p.y < h + 20);
    requestAnimationFrame(render);
  }

  update();
  render();
})();
</script>
</body>
</html>
"""

components.html(html, height=900, scrolling=True)