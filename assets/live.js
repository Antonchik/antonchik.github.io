/* Live demos on the home page: wind triangle, unit converter, sample quiz, ISA and pressure sliders.
   Plain JS, no dependencies. Everything degrades to static content without JS. */
(function () {
  "use strict";
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var RAD = Math.PI / 180;
  var $ = function (id) { return document.getElementById(id); };
  var set = function (id, text) { var el = $(id); if (el) el.textContent = text; };
  function pad3(deg) { var d = Math.round(deg) % 360; if (d <= 0) d += 360; return ("00" + d).slice(-3); }
  function f(n) { return n.toFixed(1); }

  /* ------------------------------------------------------------------
     Wind triangle. North-up disc, 1.4 px per knot, TAS fixed at 100 kt.
     Inputs: heading (drag the marker on the ring), wind (drag the arrow tip).
     Outputs: track, ground speed, drift, head/tailwind.
     ------------------------------------------------------------------ */
  (function wind() {
    var svg = $("wt-svg"); if (!svg) return;
    var root = $("wt"), dyn = $("wt-dyn"), plane = $("wt-plane"), hA = $("wt-hA"), hG = $("wt-hG"), streaks = $("wt-streaks");
    var C = 230, K = 1.4, RING = 196, TAS = 100, MAXW = 40;
    var NAVY = "#0a3492", SKY = "#6f8bd0", RED = "#dc1038";
    var s = { hdg: 34, wd: 300, ws: 28 };
    var idle = !RM, drag = null;

    function pt(brg, r) { return [C + r * Math.sin(brg * RAD), C - r * Math.cos(brg * RAD)]; }

    function arrow(p, q, col, w, dash) {
      var a = Math.atan2(q[1] - p[1], q[0] - p[0]), len = Math.hypot(q[0] - p[0], q[1] - p[1]);
      if (len < 1) return "";
      var h = Math.min(13, len * 0.6), bx = q[0] - h * Math.cos(a), by = q[1] - h * Math.sin(a);
      var nx = Math.sin(a) * h * 0.42, ny = -Math.cos(a) * h * 0.42;
      return '<line x1="' + f(p[0]) + '" y1="' + f(p[1]) + '" x2="' + f(bx) + '" y2="' + f(by) + '" stroke="' + col +
        '" stroke-width="' + w + '" stroke-linecap="round"' + (dash ? ' stroke-dasharray="' + dash + '"' : "") + "/>" +
        '<path d="M' + f(q[0]) + " " + f(q[1]) + "L" + f(bx + nx) + " " + f(by + ny) + "L" + f(bx - nx) + " " + f(by - ny) + 'Z" fill="' + col + '"/>';
    }

    // Text along the vector p→q, placed on the side facing away from `avoid`.
    function label(p, q, avoid, txt, col) {
      var len = Math.hypot(q[0] - p[0], q[1] - p[1]); if (len < 44) return "";
      var a = Math.atan2(q[1] - p[1], q[0] - p[0]), mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
      var nx = -Math.sin(a) * 15, ny = Math.cos(a) * 15;
      var d1 = Math.hypot(mx + nx - avoid[0], my + ny - avoid[1]), d2 = Math.hypot(mx - nx - avoid[0], my - ny - avoid[1]);
      var x = d1 >= d2 ? mx + nx : mx - nx, y = d1 >= d2 ? my + ny : my - ny;
      var rot = a / RAD; if (rot > 90) rot -= 180; if (rot < -90) rot += 180;
      return '<text x="' + f(x) + '" y="' + f(y) + '" fill="' + col + '" font-size="13" letter-spacing=".05em" text-anchor="middle" dominant-baseline="central"' +
        ' stroke="#fff" stroke-width="5" stroke-linejoin="round" paint-order="stroke" transform="rotate(' + f(rot) + " " + f(x) + " " + f(y) + ')">' + txt + "</text>";
    }

    function render() {
      var A = pt(s.hdg, TAS * K), to = s.wd + 180;
      var G = [A[0] + s.ws * K * Math.sin(to * RAD), A[1] - s.ws * K * Math.cos(to * RAD)];
      var gx = G[0] - C, gy = C - G[1];
      var trk = (Math.atan2(gx, gy) / RAD + 360) % 360, gs = Math.hypot(gx, gy) / K;
      var drift = ((trk - s.hdg + 540) % 360) - 180;
      var hw = s.ws * Math.cos((s.wd - s.hdg) * RAD);
      var B = pt(s.hdg, RING), O = [C, C];

      var h = '<line x1="' + f(A[0]) + '" y1="' + f(A[1]) + '" x2="' + f(B[0]) + '" y2="' + f(B[1]) + '" stroke="' + NAVY + '" stroke-opacity=".25" stroke-dasharray="2 5"/>';
      if (Math.abs(drift) >= 1) {
        var r = 56, p1 = pt(s.hdg, r), p2 = pt(trk, r), pm = pt(s.hdg + drift / 2, r + 17);
        h += '<path d="M' + f(p1[0]) + " " + f(p1[1]) + "A" + r + " " + r + " 0 0 " + (drift > 0 ? 1 : 0) + " " + f(p2[0]) + " " + f(p2[1]) + '" fill="none" stroke="' + RED + '" stroke-width="1.3"/>' +
          '<text x="' + f(pm[0]) + '" y="' + f(pm[1]) + '" fill="' + RED + '" font-size="12" text-anchor="middle" dominant-baseline="central" stroke="#fff" stroke-width="3" paint-order="stroke">' + Math.round(Math.abs(drift)) + "°</text>";
      }
      h += arrow(O, A, NAVY, 3) + arrow(A, G, SKY, 2.8, "7 5") + arrow(O, G, RED, 3);
      h += label(O, A, G, "HDG " + pad3(s.hdg), NAVY) + label(O, G, A, "TRK " + pad3(trk), RED);
      dyn.innerHTML = h;

      plane.setAttribute("transform", "translate(230 230) rotate(" + f(s.hdg) + ") scale(.8)");
      hA.setAttribute("transform", "translate(" + f(B[0]) + " " + f(B[1]) + ")");
      hG.setAttribute("transform", "translate(" + f(G[0]) + " " + f(G[1]) + ")");
      streaks.setAttribute("transform", "translate(230 230) rotate(" + f(to) + ")");
      streaks.style.opacity = Math.min(1, s.ws / 12);
      hA.setAttribute("aria-valuenow", Math.round(s.hdg) || 360);
      hG.setAttribute("aria-valuenow", Math.round(s.ws));
      hG.setAttribute("aria-valuetext", "Wind " + pad3(s.wd) + " degrees, " + Math.round(s.ws) + " knots");

      set("wt-hdg", pad3(s.hdg) + "°");
      set("wt-wind", pad3(s.wd) + "°/" + Math.round(s.ws));
      set("wt-hw-l", hw >= 0 ? "Headwind" : "Tailwind");
      set("wt-hw", Math.round(Math.abs(hw)) + " kt");
      set("wt-trk", pad3(trk) + "°");
      set("wt-gs", Math.round(gs) + " kt");
      var dr = Math.round(Math.abs(drift));
      set("wt-drift", dr === 0 ? "0°" : dr + "° " + (drift > 0 ? "R" : "L"));
    }

    // Wind streaks: short lines drifting across the disc in the wind direction.
    var lines = [];
    for (var i = 0; i < 18; i++) {
      var el = document.createElementNS("http://www.w3.org/2000/svg", "line");
      var x = -175 + 350 * (i + 0.5) / 18 + ((i * 37) % 11 - 5), len = 18 + (i * 29) % 24;
      el.setAttribute("x1", f(x)); el.setAttribute("x2", f(x)); el.setAttribute("y1", 0); el.setAttribute("y2", len);
      el.setAttribute("stroke", SKY); el.setAttribute("stroke-width", 1.6); el.setAttribute("stroke-linecap", "round");
      el.setAttribute("opacity", (0.28 + ((i * 13) % 10) / 30).toFixed(2));
      streaks.appendChild(el);
      lines.push({ el: el, y0: (i * 83) % 400, sp: 0.7 + ((i * 17) % 10) / 16 });
    }
    function flow(off) {
      for (var j = 0; j < lines.length; j++) {
        var l = lines[j], y = (((l.y0 - off * l.sp) % 400) + 400) % 400 - 200;
        l.el.setAttribute("transform", "translate(0 " + f(y) + ")");
      }
    }

    function touched() { idle = false; root.classList.add("is-touched"); }
    function local(e) {
      var r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
      return [vb.x + (e.clientX - r.left) * vb.width / r.width, vb.y + (e.clientY - r.top) * vb.height / r.height];
    }
    function move(which, e) {
      var p = local(e);
      if (which === "A") {
        s.hdg = (Math.atan2(p[0] - C, C - p[1]) / RAD + 360) % 360;
      } else {
        var A = pt(s.hdg, TAS * K), vx = p[0] - A[0], vy = p[1] - A[1], sp = Math.hypot(vx, vy) / K;
        if (sp > 0.5) s.wd = (Math.atan2(vx, -vy) / RAD + 180 + 360) % 360;
        s.ws = Math.min(MAXW, sp);
      }
      render();
    }
    function bind(handle, which) {
      handle.addEventListener("pointerdown", function (e) {
        drag = which; touched(); e.preventDefault();
        try { handle.setPointerCapture(e.pointerId); } catch (err) {}
        move(which, e);
      });
      // iOS Safari: keep the page from scrolling while a handle is being dragged
      handle.addEventListener("touchstart", function (e) { e.preventDefault(); }, { passive: false });
      handle.addEventListener("pointermove", function (e) { if (drag === which) move(which, e); });
      var end = function () { if (drag === which) drag = null; };
      handle.addEventListener("pointerup", end); handle.addEventListener("pointercancel", end);
      handle.addEventListener("keydown", function (e) {
        var k = e.key, step = e.shiftKey ? 10 : 1, used = true;
        if (which === "A") {
          if (k === "ArrowRight" || k === "ArrowUp") s.hdg = (s.hdg + step) % 360;
          else if (k === "ArrowLeft" || k === "ArrowDown") s.hdg = (s.hdg - step + 360) % 360;
          else used = false;
        } else {
          if (k === "ArrowRight") s.wd = (s.wd + 5 * step) % 360;
          else if (k === "ArrowLeft") s.wd = (s.wd - 5 * step + 360) % 360;
          else if (k === "ArrowUp") s.ws = Math.min(MAXW, s.ws + step);
          else if (k === "ArrowDown") s.ws = Math.max(0, s.ws - step);
          else used = false;
        }
        if (used) { touched(); e.preventDefault(); render(); }
      });
    }
    bind(hA, "A"); bind(hG, "G");

    render(); flow(0);
    if (RM) return;

    var visible = true, last = 0, t0 = null, off = 0;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(svg);
    }
    function tick(ts) {
      if (t0 === null) { t0 = ts; last = ts; }
      var dt = Math.min(0.05, (ts - last) / 1000); last = ts;
      if (visible && !document.hidden) {
        if (idle) {
          var t = (ts - t0) / 1000;
          s.wd = 300 + 40 * Math.sin(t * 0.35);
          s.ws = 28 + 9 * Math.sin(t * 0.23);
          render();
        }
        off += (6 + s.ws * 1.8) * dt; flow(off);
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  })();

  /* ------------------------------------------------------------------
     Unit converter (NavCalc preview): edit any field, the rest follow.
     ------------------------------------------------------------------ */
  (function converter() {
    var rows = $("cv-rows"), tabs = $("cv-tabs"); if (!rows || !tabs) return;
    var lin = function (k) { return [function (v) { return v / k; }, function (b) { return b * k; }]; };
    var Q = [
      { name: "Speed", base: 120, units: [["kt", lin(1)], ["km/h", lin(1.852)], ["m/s", lin(0.514444)], ["mph", lin(1.150779)]] },
      { name: "Distance", base: 100, units: [["NM", lin(1)], ["km", lin(1.852)], ["mi", lin(1.150779)], ["ft", lin(6076.115)]] },
      { name: "Height", base: 3000, units: [["ft", lin(1)], ["m", lin(0.3048)], ["FL", lin(0.01)]] },
      { name: "Temp", base: 15, units: [["°C", lin(1)], ["°F", [function (v) { return (v - 32) / 1.8; }, function (b) { return b * 1.8 + 32; }]],
        ["K", [function (v) { return v - 273.15; }, function (b) { return b + 273.15; }]]] }
    ];
    var cur = 0;
    function fmt(v) {
      if (!isFinite(v)) return "";
      var a = Math.abs(v), d = a >= 10000 ? 0 : a >= 1000 ? 1 : a >= 10 ? 2 : 3;
      return String(+v.toFixed(d));
    }
    function fill(skip) {
      var q = Q[cur], inputs = rows.querySelectorAll("input");
      for (var i = 0; i < inputs.length; i++) if (inputs[i] !== skip) inputs[i].value = fmt(q.units[i][1][1](q.base));
    }
    function build() {
      var q = Q[cur], h = "";
      for (var i = 0; i < q.units.length; i++) {
        h += '<label class="cv-row"><span>' + q.units[i][0] + '</span><input type="text" inputmode="decimal" autocomplete="off" data-i="' + i + '" aria-label="' + (q.name === "Temp" ? "Temperature" : q.name) + " in " + q.units[i][0] + '"></label>';
      }
      rows.innerHTML = h; fill(null);
      var b = tabs.querySelectorAll("button");
      for (var j = 0; j < b.length; j++) { b[j].classList.toggle("is-on", j === cur); b[j].setAttribute("aria-selected", j === cur); }
    }
    var th = "";
    for (var i = 0; i < Q.length; i++) th += '<button type="button" role="tab" data-q="' + i + '">' + Q[i].name + "</button>";
    tabs.innerHTML = th;
    tabs.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return; cur = +b.getAttribute("data-q"); build();
    });
    rows.addEventListener("input", function (e) {
      var inp = e.target, v = parseFloat(String(inp.value).replace(",", "."));
      if (!isFinite(v)) return;
      Q[cur].base = Q[cur].units[+inp.getAttribute("data-i")][1][0](v); fill(inp);
    });
    build();
  })();

  /* ------------------------------------------------------------------
     Sample quiz (Pilotiq preview). Illustrative questions.
     ------------------------------------------------------------------ */
  (function quiz() {
    var box = $("qz"); if (!box) return;
    var QS = [
      { q: "In the ICAO Standard Atmosphere, the temperature at mean sea level is:", o: ["0 °C", "15 °C", "20 °C"], a: 1,
        x: "ISA at sea level: 15 °C and 1013.25 hPa." },
      { q: "With QNH set, an altimeter on the ground at an aerodrome indicates:", o: ["Zero", "Aerodrome elevation", "Pressure altitude"], a: 1,
        x: "QNH gives altitude above mean sea level. With QFE set it would read zero." },
      { q: "Heading 090°, wind from 360°. The aircraft drifts:", o: ["To the left", "To the right", "Not at all"], a: 1,
        x: "Wind from the north pushes the aircraft south — to the right of an easterly heading. Try it in the wind triangle above." }
    ];
    var i = 0, score = 0;
    function show() {
      var q = QS[i], h = '<p class="qz-q">' + q.q + "</p>";
      for (var k = 0; k < q.o.length; k++) h += '<button type="button" class="qz-o" data-k="' + k + '"><i>' + "ABC"[k] + "</i>" + q.o[k] + "</button>";
      h += '<div class="qz-x" id="qz-x" aria-live="polite"></div>';
      box.innerHTML = h; set("qz-n", "Sample · " + (i + 1) + "/" + QS.length);
    }
    function done() {
      box.innerHTML = '<p class="qz-q">' + score + " of " + QS.length + " correct" + (score === QS.length ? " — cleared for take-off." : ".") +
        '</p><p class="qz-x">The app has hundreds more, grouped by subject, for PPL(A), PPL(H), PL(G) and PL(FB).</p>' +
        '<div class="qz-actions"><a class="qz-next" href="/pilotiq_support/">About Pilotiq</a><button type="button" class="qz-again" data-again="1">Try again</button></div>';
      set("qz-n", "Sample · done");
    }
    box.addEventListener("click", function (e) {
      if (e.target.closest("[data-again]")) { i = 0; score = 0; show(); return; }
      if (e.target.closest("[data-next]")) { i++; if (i < QS.length) show(); else done(); return; }
      var b = e.target.closest(".qz-o"); if (!b || b.disabled) return;
      var q = QS[i], k = +b.getAttribute("data-k"), all = box.querySelectorAll(".qz-o");
      for (var n = 0; n < all.length; n++) { all[n].disabled = true; if (n === q.a) all[n].classList.add("is-ok"); }
      if (k === q.a) score++; else b.classList.add("is-no");
      $("qz-x").innerHTML = "<p>" + (k === q.a ? "Correct. " : "Not quite. ") + q.x + '</p><button type="button" class="qz-next" data-next="1">' +
        (i + 1 < QS.length ? "Next question" : "See result") + "</button>";
    });
    show();
  })();

  /* ------------------------------------------------------------------
     Range sliders: ISA (isa package) and pressure units (measures package).
     ------------------------------------------------------------------ */
  function track(r) { r.style.setProperty("--p", ((r.value - r.min) / (r.max - r.min) * 100) + "%"); }

  (function isa() {
    var r = $("isa-h"); if (!r) return;
    function upd() {
      var h = +r.value, T, p;                       // geopotential altitude, m
      if (h <= 11000) { T = 288.15 - 0.0065 * h; p = 1013.25 * Math.pow(T / 288.15, 5.25588); }
      else { T = 216.65; p = 226.321 * Math.exp(-(h - 11000) / 6341.62); }
      var rho = p * 100 / (287.05287 * T), a = Math.sqrt(1.4 * 287.05287 * T);
      set("isa-alt", h.toLocaleString("en-US") + " m · " + Math.round(h / 0.3048).toLocaleString("en-US") + " ft");
      set("isa-t", (T - 273.15).toFixed(1).replace("-", "−") + " °C");
      set("isa-p", (p >= 1000 ? p.toFixed(2) : p.toFixed(1)) + " hPa");
      set("isa-rho", rho.toFixed(3) + " kg/m³");
      set("isa-a", Math.round(a / 0.514444) + " kt");
      set("isa-layer", h <= 11000 ? "Troposphere · temperature falls 6.5 °C per km" : "Above the tropopause · temperature constant at −56.5 °C");
      track(r);
    }
    r.addEventListener("input", upd); upd();
  })();

  (function pressure() {
    var r = $("ms-h"); if (!r) return;
    function upd() {
      var hpa = +r.value;
      set("ms-v", hpa + " hPa");
      set("ms-inhg", (hpa * 0.0295300).toFixed(2));
      set("ms-mmhg", (hpa * 0.750062).toFixed(1));
      set("ms-psi", (hpa * 0.0145038).toFixed(2));
      track(r);
    }
    r.addEventListener("input", upd); upd();
  })();
})();
