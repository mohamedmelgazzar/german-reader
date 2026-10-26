// Reads the STORIES list from index.html and writes scripts/items.json:
// every sentence (with its id) and every word form that needs a clip.
const fs = require("fs");
const html = fs.readFileSync("index.html", "utf8");
const js = html.split("<script>")[1].split("/* ---------- dictionary")[0];
const STORIES = new Function(js + "\nreturn STORIES;")();

const out = { sentences: [], words: {} };
STORIES.forEach((s, si) => {
  s.sentences.forEach((x, i) => {
    out.sentences.push({ id: si + "-" + i, de: x.de });
    (x.de.match(/[\p{L}\p{N}']+/gu) || []).forEach(w => {
      const k = w.toLowerCase();
      // keep the capitalized form when the word is a noun or name (capitalized mid-sentence)
      if (!out.words[k] || w !== k && out.words[k] === k) out.words[k] = w;
    });
  });
});
fs.writeFileSync("scripts/items.json", JSON.stringify(out, null, 1));
console.log(out.sentences.length + " sentences, " + Object.keys(out.words).length + " words");
