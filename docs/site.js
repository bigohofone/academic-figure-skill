// Shared by every page: the grayscale switch (remembered across pages), the GitHub star count, copy buttons,
// and the with / without switches. Loaded in <head>, so a page opens already in grayscale when it was left so.
try { if (localStorage.getItem("bw") === "1") document.documentElement.classList.add("bw"); } catch (e) {}

document.addEventListener("DOMContentLoaded", () => {
  const sw = document.createElement("button");
  sw.type = "button";
  sw.className = "bw-switch";
  sw.textContent = "Grayscale";
  document.body.append(sw);
  document.querySelectorAll(".bw-switch").forEach(b => {
    b.setAttribute("aria-pressed", document.documentElement.classList.contains("bw"));
    b.addEventListener("click", () => {
      const on = document.documentElement.classList.toggle("bw");
      b.setAttribute("aria-pressed", on);
      try { localStorage.setItem("bw", on ? "1" : "0"); } catch (e) {}
    });
  });

  fetch("https://api.github.com/repos/bigohofone/academic-figure-skill").then(r => r.json()).then(d => {
    if (typeof d.stargazers_count !== "number") return;
    const n = d.stargazers_count >= 1000 ? (d.stargazers_count / 1000).toFixed(1) + "k" : String(d.stargazers_count);
    document.querySelectorAll(".count").forEach(c => { c.textContent = "★ " + n; c.hidden = false; });
  }).catch(() => {});

  document.querySelectorAll(".copy").forEach(b => b.addEventListener("click", () => {
    navigator.clipboard.writeText(b.dataset.text).then(() => { b.textContent = "Copied"; setTimeout(() => b.textContent = "Copy", 1500); });
  }));

  document.querySelectorAll("[data-show]").forEach(box => {
    box.querySelectorAll(".switch button").forEach(b => b.addEventListener("click", () => {
      box.dataset.show = b.dataset.v;
      box.querySelectorAll(".switch button").forEach(o => o.setAttribute("aria-pressed", o === b));
    }));
  });
});
