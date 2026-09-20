// Type three digits to go to a page, as on a television's remote control.
// The left and right arrows go to the page before, and the page after.
const screen = document.querySelector(".screen");
let typed = "";

document.addEventListener("keydown", (event) => {
  const { before, after } = screen.dataset;
  if (event.key === "ArrowLeft" && before) location.href = `${before}.html`;
  if (event.key === "ArrowRight" && after) location.href = `${after}.html`;
  if (event.key.length > 1 || event.key < "0" || event.key > "9") return;
  typed += event.key;
  if (typed.length === 3) location.href = `${typed}.html`;
});
