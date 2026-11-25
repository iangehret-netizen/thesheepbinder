#!/usr/bin/env python3
"""The Sheep Binder builder.

Turns the newest Gehret Sheep Co app (a clone of iangehret-netizen/gehretsheepco) into a
branded Sheep Binder app: the demo, or a customer's copy.

    python3 build.py --src /path/to/gehretsheepco --intake intake.json --out /path/to/out

intake.json (see intake-example.json):
  name, shortName        farm / app name shown everywhere, short name for "own" animals
  storagePrefix          4+ chars ending in ":"; unique per app on the same web address
  collection             Firestore collection prefix (<collection>_sync, <collection>_sm)
  syncEmail              the hidden sync login (Authentication user) for the passcode
  firebase               the firebaseConfig object
  years, examplesYear    year tabs on first open; year the examples go in
  examples               true = test entries load on first open
  palette                dark, accent, accentLight, accentMid, bg, border, borderLight, muted
  logo                   path to a PNG logo (transparent background works best), or "" for the
                         Sheep Binder wordmark; logoOnDark: optional separate logo for the black header/cover
  version                integer; bump on every rebuild so phones pick up the update
"""
import argparse, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template")

SKIP = {"Southdown-Ref-Sires-added.csv", "bundle.js.seed.json", "SHOWMAN-CODES-SETUP.txt", ".git"}

# Gehret's colors -> palette slot
COLOR_SLOTS = {
    "#1B1B1B": "dark", "#B8963F": "accent", "#E4CC96": "accentLight", "#D9C089": "accentMid",
    "#FAF8F3": "bg", "#DDD8CC": "border", "#EEE9DC": "borderLight", "#EEE9DD": "borderLight",
    "#F1EFEA": "bgAlt", "#F3F1EC": "bgAlt", "#8A8270": "muted", "#2A251C": "coverMid", "#121110": "coverEdge",
}
DEFAULT_PALETTE = {  # The Sheep Binder: black / white / silver / gold
    "dark": "#111111", "accent": "#C9A227", "accentLight": "#E8D38A", "accentMid": "#DCC36A",
    "bg": "#F6F7F8", "border": "#C9CDD2", "borderLight": "#E6E8EB", "bgAlt": "#F1F2F4",
    "muted": "#6B7078", "coverMid": "#2B2D31", "coverEdge": "#0A0A0A",
}

# Gehret's real records baked into the bundle: emptied
DATA_LITERALS = ["J6", "Q6", "nle", "ile", "ole", "e8", "t8", "r8", "F26_WEIGHTS", "F26_WEIGHTS_V3", "F26_FEEDS",
                 "F26_V2_NEWSHEEP", "F26_V2_SHOWS", "F26_V2_RESULTS", "J25E", "J25S", "J25W", "JATE", "JATS", "JATR",
                 "JF26E", "JF26S", "JF26C", "JF26R", "JF26W"]
SEED_LITERALS = ["OS", "WD", "FD"]  # `let X={...}` inside the one-time loaders


def die(msg):
    print("BUILD ERROR:", msg); sys.exit(1)


def rep(s, a, b, count=1, label=""):
    n = s.count(a)
    if count is not None and n != count:
        die("%s: expected %d of %r, found %d" % (label or "replace", count, a[:80], n))
    return s.replace(a, b)


def match_end(s, i):
    """i = index of an opening [ or {; returns index of its matching closer."""
    depth, q = 0, None
    while i < len(s):
        c = s[i]
        if q:
            if c == "\\": i += 2; continue
            if c == q: q = None
        elif c in "\"'`": q = c
        elif c in "[{": depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0: return i
        i += 1
    die("unbalanced literal")


def blank_literal(s, name, decl=r"(?:\bvar |\blet |,)"):
    m = list(re.finditer(decl + re.escape(name) + r"=([\[{])", s))
    m = [x for x in m if match_end(s, x.start(1)) - x.start(1) > 2]
    if not m: return s, False
    if len(m) > 1:
        # keep only the data-sized one (OS also names a Math constant elsewhere)
        m = [x for x in m if match_end(s, x.start(1)) - x.start(1) > 200]
    for x in sorted(m, key=lambda x: -x.start(1)):
        a = x.start(1); b = match_end(s, a)
        s = s[:a] + ("[]" if s[a] == "[" else "{}") + s[b + 1:]
    return s, True


def recolor(s, pal):
    for hx, slot in COLOR_SLOTS.items():
        s = re.sub(re.escape(hx), pal[slot], s, flags=re.I)
    return s


def build_bundle(s, cfg, pal):
    for n in DATA_LITERALS:
        s, ok = blank_literal(s, n)
        if not ok: print("  note: literal", n, "not found (fine if removed upstream)")
    for n in SEED_LITERALS:
        s, ok = blank_literal(s, n, decl=r"\blet ")
        if not ok: die("seed literal %s not found" % n)
    # first-open year list comes from the config
    s = rep(s, '["All Time","2025","2026","Fall 2026"]', '(window.TSB_CONFIG.years||["All Time"]).slice()', label="years")
    # storage prefix (each app on the same web address needs its own)
    n = s.count('"gsc:')
    if n < 8: die("expected the gsc: storage prefix in the bundle, found %d" % n)
    s = s.replace('"gsc:"', 'window.TSB_CONFIG.storagePrefix').replace('"gsc:', 'window.TSB_CONFIG.storagePrefix+"')
    for k in ["gsc-tour-done", "gsc-gx-clip"]:
        s = rep(s, '"%s"' % k, 'window.TSB_CONFIG.storagePrefix+"%s"' % k[4:], label=k)
    s = rep(s, 'var ks="gsc-setopen-"', 'var ks=window.TSB_CONFIG.storagePrefix+"setopen-"', label="setopen")
    s = rep(s, "a.slice(4)", "a.slice(window.TSB_CONFIG.storagePrefix.length)", label="prefix slice")
    # brand name
    s = rep(s, 'function gxBrand(){', 'function gxShort(){return(window.TSB_CONFIG||{}).shortName||gxBrand()}\nfunction gxBrand(){return(window.TSB_CONFIG||{}).name||document.title||"Sheep Records"}\nfunction gxBrandOld(){', label="gxBrand")
    s = rep(s, 'src:"./logo-cover.png",alt:"",className:"gx-hlogo"', 'src:"./logo-header.png",alt:"",className:"gx-hlogo"', label="header logo")
    s = rep(s, '"Gehret Sheep Co"]', 'gxBrand()]', label="header name")
    s = rep(s, 'fn=herd?"Gehret Sheep Co - Herd.xlsx":`Gehret Sheep Co - ${n}.xlsx`', 'fn=herd?gxBrand()+" - Herd.xlsx":`${gxBrand()} - ${n}.xlsx`', label="xlsx")
    s = rep(s, 'children:["Gehret Sheep Co \\u2014 ",e]', 'children:[gxBrand()+" \\u2014 ",e]', label="print title")
    s = rep(s, 'children:"Gehret Sheep Co \\u2014 Herd Records"', 'children:gxBrand()+" \\u2014 Herd Records"', label="herd print")
    s = rep(s, '"Anything you add is sent to Gehret Sheep Co for approval.', '"Anything you add is sent to "+gxBrand()+" for approval.', label="showman note")
    s = rep(s, 'gxBtn("Use Gehret colors"', 'gxBtn("Use app colors"', label="colors btn")
    s = rep(s, 'owner:"Gehret"', 'owner:gxShort()', label="owner")
    s = rep(s, 'name:"Gehret"}', 'name:gxShort()}', count=None)
    s = rep(s, 'fontWeight:700}},"Gehret")', 'fontWeight:700}},gxShort())', label="sire mark")
    s = rep(s, 'note:"Bucks Gehret owns or raised.', 'note:"Bucks you own or raised.', label="bucks note")
    s = rep(s, '(marked Gehret)', '(marked with your farm name)', label="bucks note 2")
    s = s.replace("shared by Gehret, Petry and Wallen", "shared extensions")
    # Settings: the one "Remove examples" button (every Settings tab ends with the App Tour card)
    s = rep(s, "gxE(GxTourCard,{})", "gxE(GxTourCard,{}),gxE(TsbExCard,{})", label="tour card")
    s = rep(s, "function GxTourCard(){", (
        'function TsbExCard(){var st=ge.useState(0),force=st[1],on=!!(window.tsbExamplesPresent&&window.tsbExamplesPresent());'
        'return gxE(Gn,null,gxE(mn,null,"Examples"),'
        'gxNote(on?"The app starts with a few test entries (Test Lamb, Test Ewe, Test Show and so on) so every tab has something to look at. Remove examples takes out only those; anything you\'ve added stays.":"The example entries have been removed."),'
        'on?gxE(tt,{onClick:function(){Promise.resolve(window.tsbRemoveExamples&&window.tsbRemoveExamples()).then(function(){force(function(n){return n+1})})}},"Remove examples"):null)}\n'
        'function GxTourCard(){'), label="tour fn")
    s = rep(s, '[/^app tour/,"help"]];', '[/^app tour/,"help"],[/^examples/,"help"]];', label="examples in Help")
    left = [m.start() for m in re.finditer("Gehret Sheep Co", s)]
    if left: die("Gehret Sheep Co still in bundle at %s" % left[:5])
    return recolor(s, pal)


def build_sync(s, cfg):
    i = s.index("  var FIREBASE_CONFIG = {"); j = s.index("};", i) + 2
    s = s[:i] + "  var CFG = window.TSB_CONFIG || {};\n  var FIREBASE_CONFIG = CFG.firebase;" + s[j:]
    s = re.sub(r'var SYNC_EMAIL = "[^"]*";', "var SYNC_EMAIL = CFG.syncEmail;", s)
    s = rep(s, 'var LOCAL_PREFIX = "gsc:";', "var LOCAL_PREFIX = CFG.storagePrefix;")
    s = rep(s, 'var META_PREFIX = "gsc:__syncmeta:";', 'var META_PREFIX = CFG.storagePrefix + "__syncmeta:";')
    s = rep(s, 'localStorage.getItem("gsc:__sm")', 'localStorage.getItem(CFG.storagePrefix + "__sm")')
    s = s.replace('"gsc:autoReload"', 'CFG.storagePrefix + "autoReload"')
    s = s.replace('"gsc_sync"', 'CFG.collection + "_sync"')
    s = s.replace("Gehret Sheep Co</div>", "' + (CFG.name || 'Records') + '</div>")
    s = s.replace("// Gehret Sheep Co — cross-device sync", "// The Sheep Binder — cross-device sync (settings come from config.js)")
    # examples removed on another device -> clean this one too
    s = rep(s, "        if (sawChange) applyRemote(changedKeys);",
            "        if (changedKeys.indexOf(\"sheepwrld:examples\") >= 0 && window.tsbExamplesRemote) window.tsbExamplesRemote();\n"
            "        if (sawChange) applyRemote(changedKeys);")
    if re.search(r"Gehret Sheep|gehret-sheep|iangehret|gsc_sync|\"gsc:", s.replace("iangehret@gmail.com\"", "")) and False: pass
    s = rep(s, "'background:#4F7942;color:#fff;font-size:15px;font-weight:600;cursor:pointer;\">Unlock</button>'",
            "'background:' + (CFG.accent || '#C9A227') + ';color:#111;font-size:15px;font-weight:700;cursor:pointer;\">Unlock</button>'", label="unlock")
    if re.search(r"Gehret Sheep|gehret-sheep|gsc_sync|\"gsc:|SYNC_EMAIL = \"", s): die("sync.js still has Gehret settings")
    return s


def build_showman(s, cfg):
    s = rep(s, 'var LS = "gsc:";', 'var CFG = window.TSB_CONFIG || {};\n  var LS = CFG.storagePrefix;')
    s = s.replace('"gsc:__smIdleMs"', 'LS + "__smIdleMs"')
    s = s.replace('"gsc_sm"', 'CFG.collection + "_sm"')
    s = s.replace('" entered by Gehret Sheep Co"', '" entered by " + (CFG.name || "the owner")')
    s = s.replace('"This phone has Gehret Sheep Co records on it.', '"This phone has " + (CFG.name || "farm") + " records on it.')
    s = s.replace("// Gehret Sheep Co — showman codes", "// The Sheep Binder — showman codes")
    if re.search(r"Gehret Sheep|\"gsc:|\"gsc_sm\"", s): die("showman.js still has Gehret settings: %s" % re.findall(r"(?i).{40}gehret.{40}", s)[:3])
    return s


def build_index(s, cfg, pal):
    nm = cfg["name"].replace("&", "&amp;")
    s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % nm, s)
    s = rep(s, '<meta name="apple-mobile-web-app-title" content="Gehret Sheep Co" />', '<meta name="apple-mobile-web-app-title" content="%s" />' % nm)
    s = rep(s, 'alt="Gehret Sheep Co."', 'alt="%s"' % nm)
    s = s.replace('"gsc:cover:day"', 'window.TSB_CONFIG.storagePrefix + "cover:day"')
    s = rep(s, '  <script src="./firebase-vendor.js"></script>',
            '  <script src="./config.js"></script>\n  <script src="./examples.js"></script>\n  <script src="./firebase-vendor.js"></script>')
    if re.search(r"(?i)gehret|\"gsc:", s): die("index.html still has Gehret text")
    return recolor(s, pal)


def build_sw(s, cfg):
    pre = re.sub(r"[^a-z0-9]", "", cfg["storagePrefix"].lower()) + "-app-"
    s = re.sub(r'const CACHE_NAME = "gsc-app-v\d+";', 'const CACHE_NAME = "%sv%d";' % (pre, int(cfg.get("version", 1))), s)
    s = rep(s, 'k.indexOf("gsc-app-") === 0', 'k.indexOf("%s") === 0' % pre)
    s = rep(s, '  "./sync.js",', '  "./config.js",\n  "./examples.js",\n  "./sync.js",')
    s = rep(s, '  "./logo-pdf.png",', '  "./logo-pdf.png",\n  "./logo-header.png",')
    return s


def rules(cfg):
    c, e = cfg["collection"], cfg["syncEmail"]
    return """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // The passcode login (the hidden sync account).
    function isOwner() {
      return request.auth != null && request.auth.token.email == '%(e)s';
    }

    // All records: only phones unlocked with the passcode.
    match /%(c)s_sync/{key} {
      allow read, write: if isOwner();
    }

    // Showman codes: each code is its own document, named by a scrambled form of the code.
    match /%(c)s_sm/{code} {
      allow get: if request.auth != null;
      allow list, create, update, delete: if isOwner();
      match /years/{year} {
        allow get, list: if request.auth != null;
        allow create, update, delete: if isOwner();
      }
      match /inbox/{entry} {
        allow create: if request.auth != null
          && get(/databases/$(database)/documents/%(c)s_sm/$(code)).data.active == true
          && request.resource.data.keys().hasOnly(['op', 'ts', 'by'])
          && request.resource.data.op is string
          && request.resource.data.op.size() < 20000;
        allow get, delete: if isOwner();
      }
    }

    match /{path=**}/inbox/{entry} {
      allow read, delete: if isOwner();
    }
  }
}
""" % {"c": c, "e": e}


def config_js(cfg):
    keep = {k: cfg[k] for k in ["name", "shortName", "storagePrefix", "collection", "syncEmail", "firebase", "years", "examplesYear", "examples"] if k in cfg}
    keep["accent"] = cfg.get("_accent")
    return ("// The Sheep Binder — app settings. One file per farm.\n"
            "// storagePrefix must be different for every app hosted on the same web address.\n"
            "window.TSB_CONFIG = " + json.dumps(keep, indent=2, ensure_ascii=False) + ";\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True); ap.add_argument("--intake", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.intake))
    for k in ["name", "storagePrefix", "collection", "syncEmail", "firebase", "years"]:
        if not cfg.get(k): die("intake is missing " + k)
    if not cfg["storagePrefix"].endswith(":"): die("storagePrefix must end with ':'")
    cfg.setdefault("shortName", cfg["name"]); cfg.setdefault("examples", True)
    pal = dict(DEFAULT_PALETTE); pal.update(cfg.get("palette") or {})
    cfg["_accent"] = pal["accent"]
    if os.path.exists(a.out): shutil.rmtree(a.out)
    os.makedirs(a.out)
    for f in sorted(os.listdir(a.src)):
        if f in SKIP or f.startswith("."): continue
        shutil.copy2(os.path.join(a.src, f), os.path.join(a.out, f))
    O = lambda f: os.path.join(a.out, f)
    def edit(f, fn, *args):
        s = open(O(f), encoding="utf-8").read(); open(O(f), "w", encoding="utf-8").write(fn(s, *args))
    edit("bundle.js", build_bundle, cfg, pal)
    edit("sync.js", build_sync, cfg)
    edit("showman.js", build_showman, cfg)
    edit("index.html", build_index, cfg, pal)
    edit("sw.js", build_sw, cfg)
    for f in ["pdfpacket.js", "salepdf.js"]:
        s = open(O(f), encoding="utf-8").read()
        s = s.replace('name || "Gehret Sheep Co.pdf"', 'name || ((document.title || "Records") + ".pdf")')
        s = s.replace('"Gehret Sheep Co - "', '(document.title || "Records") + " - "')
        s = s.replace("Gehret Sheep Co", "The Sheep Binder")
        open(O(f), "w", encoding="utf-8").write(s)
    m = json.load(open(O("manifest.json")))
    m.update({"name": cfg["name"], "short_name": cfg.get("homeScreenName") or cfg["shortName"][:12], "background_color": pal["dark"], "theme_color": pal["dark"]})
    json.dump(m, open(O("manifest.json"), "w"), indent=2)
    open(O("config.js"), "w").write(config_js(cfg))
    shutil.copy2(os.path.join(TEMPLATE, "examples.js"), O("examples.js"))
    open(O("firestore.rules"), "w").write(rules(cfg))
    import logos
    logos.make(cfg, pal, a.out, os.path.dirname(os.path.abspath(a.intake)))
    # final check: no Gehret name or real records left anywhere a user could see
    bad = []
    for f in os.listdir(a.out):
        if f.endswith((".js", ".html", ".json", ".rules", ".txt", ".md")):
            t = open(O(f), encoding="utf-8", errors="ignore").read()
            for w in ["Gehret Sheep Co", "gehret-sheep-co", "Ellen Getz", "Mo Betty", "Paige Gehret"] + (["iangehret@gmail.com"] if cfg["syncEmail"] != "iangehret@gmail.com" else []):
                if w in t: bad.append((f, w))
    if bad: die("leftovers: %s" % bad)
    print("built", cfg["name"], "->", a.out)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    main()
