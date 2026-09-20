// Draws the table of scores on a <canvas>, and draws it again whenever the
// server says that there's a new score.
const COLOURS = ["#f00", "#ff0", "#0f0", "#0ff", "#f0f", "#fff"];
const canvas = document.querySelector("#board");
const pen = canvas.getContext("2d");
const chooser = document.querySelector("#game");
let events = null;

async function draw(game) {
  const scores = await (await fetch(`scores/${game}?limit=10`)).json();
  const best = Math.max(1, ...scores.map((row) => row.score));
  pen.fillStyle = "#000";
  pen.fillRect(0, 0, canvas.width, canvas.height);
  pen.font = "bold 20px monospace";
  pen.textBaseline = "middle";
  scores.forEach((row, place) => {
    const y = 22 + place * 38;
    pen.fillStyle = COLOURS[place % COLOURS.length];
    pen.fillRect(200, y - 14, (row.score / best) * 330, 28);
    pen.fillText(`${String(row.rank).padStart(2)} ${row.player}`, 12, y);
    pen.fillStyle = "#fff";
    pen.fillText(row.score, 540, y);
  });
}

function watch(game) {
  if (events) events.close();
  events = new EventSource(`scores/${game}/events`);
  events.onmessage = () => draw(game);
}

async function start() {
  const games = await (await fetch("games")).json();
  for (const { game } of games) chooser.add(new Option(game));
  const wanted = new URLSearchParams(location.search).get("game");
  if (wanted) chooser.value = wanted;
  chooser.onchange = () => watch(chooser.value);
  if (chooser.value) watch(chooser.value);
}

start();
