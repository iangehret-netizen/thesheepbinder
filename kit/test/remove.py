import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
from walk import serve, open_app, ls_dump, PORT
from playwright.sync_api import sync_playwright

OUT, SHOTS = sys.argv[1], sys.argv[2]
import walk; walk.OUT = OUT
serve()
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx, pg, errs = open_app(b, "try{localStorage.setItem('tsb:tour-done','1')}catch(e){}")
    # the user adds their own lamb, and a weigh-in on an example lamb
    pg.evaluate("""()=>{const k='tsb:sheepwrld:showbarn:2026';const d=JSON.parse(localStorage.getItem(k));
      d.sheep.push({id:'u1',name:'My Own Lamb',sex:'Wether',lEar:'26777',showman:'Test Showman 1'});
      d.weights['ex-s1'].push({id:'uw1',date:'2026-07-10',weight:131});
      d.weights['u1']=[{id:'uw2',date:'2026-07-10',weight:99}];
      localStorage.setItem(k,JSON.stringify(d));
      const h=JSON.parse(localStorage.getItem('tsb:sheepwrld:herd'));h.herdSheep.push({id:'u2',name:'My Ewe',sex:'Ewe'});localStorage.setItem('tsb:sheepwrld:herd',JSON.stringify(h));}""")
    pg.reload(); pg.wait_for_timeout(1500)
    if pg.locator("#gsc-cover-open").is_visible(): pg.click("#gsc-cover-open"); pg.wait_for_timeout(600)
    pg.click('.gx-tabs button[data-tab="years"]'); pg.wait_for_timeout(800)
    pg.locator("button", has_text=re.compile(r"^\s*Help")).first.click(); pg.wait_for_timeout(500)
    btn = pg.get_by_role("button", name="Remove examples")
    print("button visible:", btn.count(), btn.first.is_visible() if btn.count() else None)
    btn.first.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(SHOTS, "r1-settings-before.png"))
    pg.once("dialog", lambda d: (print("confirm:", d.message.splitlines()[0]), d.accept()))
    btn.first.click(); pg.wait_for_timeout(2500)
    if pg.locator("#gsc-cover-open").is_visible(): pg.click("#gsc-cover-open"); pg.wait_for_timeout(600)
    d = ls_dump(pg, "tsb:")
    left = {k: re.findall(r'"(ex-[\w-]+)"', v) for k, v in d.items() if "ex-" in v}
    print("flag:", d.get("sheepwrld:examples"))
    print("example ids left:", {k: sorted(set(v)) for k, v in left.items()})
    sb = json.loads(d["sheepwrld:showbarn:2026"])
    print("2026 sheep:", [s["name"] for s in sb["sheep"]], "weights:", {k: [w["id"] for w in v] for k, v in sb["weights"].items()})
    print("exhibitors:", sb["exhibitors"], "shows:", sb["shows"], "results:", sb["showResults"])
    print("herd ewes:", [s["name"] for s in json.loads(d["sheepwrld:herd"])["herdSheep"]])
    print("other farm keys:", [k for k in d if "of:" in k or "otherfarms" in k], d.get("sheepwrld:otherfarms"))
    # reload twice: examples must not come back
    for i in range(2):
        pg.reload(); pg.wait_for_timeout(1200)
    d2 = ls_dump(pg, "tsb:")
    print("after reload, any new ex-:", sum(v.count('"ex-') for v in d2.values()), "vs", sum(v.count('"ex-') for v in d.values()))
    if pg.locator("#gsc-cover-open").is_visible(): pg.click("#gsc-cover-open"); pg.wait_for_timeout(600)
    pg.click('.gx-tabs button[data-tab="years"]'); pg.wait_for_timeout(700)
    pg.locator("button", has_text=re.compile(r"^\s*Help")).first.click(); pg.wait_for_timeout(500)
    pg.get_by_text("The example entries have been removed.").first.scroll_into_view_if_needed()
    pg.screenshot(path=os.path.join(SHOTS, "r2-settings-after.png"))
    pg.click('.gx-tabs button[data-tab="roster"]'); pg.wait_for_timeout(700)
    pg.screenshot(path=os.path.join(SHOTS, "r3-roster-after.png"))
    print("errors:", errs[:8])
    b.close()
