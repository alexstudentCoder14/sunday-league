"""Bake every Polyfork model into sunday-league.html so it works ANYWHERE (including the Claude preview,
which blocks outside downloads). Run on a computer with internet:

    python embed-models.py sunday-league.html

Writes sunday-league-embedded.html (about 5 to 10 MB). Use --dry to just list what it would download."""
import base64, re, sys, urllib.request, json
src = sys.argv[1]; dry = "--dry" in sys.argv
html = open(src, encoding="utf-8").read()
block = re.search(r"URLS=\{(.*?)\};", html, re.S).group(1)
pairs = re.findall(r"(\w+):'([a-z0-9\-]+-[0-9a-f]{6})'", block)
print(len(pairs), "models")
if dry: sys.exit()
emb = {}
for k, slug in pairs:
    url = "https://polyfork.dev/cdn/%s.glb" % slug
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
        emb[k] = "data:model/gltf-binary;base64," + base64.b64encode(data).decode()
        print("ok  ", k, len(data) // 1024, "KB")
    except Exception as e:
        print("FAIL", k, e)
html = html.replace("const EMBED={};", "const EMBED=" + json.dumps(emb) + ";", 1)
out = src.replace(".html", "-embedded.html")
open(out, "w", encoding="utf-8").write(html)
print("saved", out)
