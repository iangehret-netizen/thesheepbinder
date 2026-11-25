"""Walk every section/tab of a built Sheep Binder at phone size.
python3 walk.py <outdir> <shotsdir> [--remove]"""
import sys, os, re, json, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

OUT, SHOTS = (sys.argv[1:3] + ["/home/claude/tsb/out", "/tmp/shots"])[:2] if len(sys.argv) < 3 else sys.argv[1:3]
os.makedirs(SHOTS, exist_ok=True)
PORT = 8791


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def serve():
    h = functools.partial(Q, directory=OUT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()


def ls_dump(pg, pre):
    return pg.evaluate("""(pre)=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith(pre))o[k.slice(pre.length)]=localStorage.getItem(k)}return o}""", pre)


def open_app(b, init=None):
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, service_workers="block")
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.route("**/firebase-vendor.js", lambda r: r.fulfill(content_type="application/javascript", body=""))
    if init: pg.add_init_script(init)
    pg.goto("http://127.0.0.1:%d/index.html" % PORT); pg.wait_for_timeout(1500)
    if pg.locator("#gsc-cover-open").is_visible(): pg.click("#gsc-cover-open"); pg.wait_for_timeout(700)
    return ctx, pg, errs


def skip_tour(pg):
    for _ in range(3):
        b = pg.get_by_role("button", name=re.compile("^(Skip|Skip tour|Close|Done)$"))
        if b.count() and b.first.is_visible(): b.first.click(); pg.wait_for_timeout(400)


def walk(pg, tag):
    rep = []
    roots = pg.eval_on_selector_all(".gx-rootbar button[data-root]", "bs=>bs.map(b=>b.getAttribute('data-root'))")
    for r in roots:
        pg.click('.gx-rootbar button[data-root="%s"]' % r); pg.wait_for_timeout(700)
        tabs = pg.eval_on_selector_all(".gx-tabs button[data-tab]", "bs=>bs.map(b=>[b.getAttribute('data-tab'),b.textContent.trim()])")
        for t, lab in tabs:
            pg.click('.gx-tabs button[data-tab="%s"]' % t); pg.wait_for_timeout(600)
            txt = pg.inner_text(".gx-body") if pg.locator(".gx-body").count() else pg.inner_text("body")
            n = len(re.findall(r"\bTest\b|Example", txt))
            fn = "%s-%s-%s.png" % (tag, r, t)
            pg.screenshot(path=os.path.join(SHOTS, fn), full_page=False)
            rep.append((r, t, lab, n))
    return rep


if __name__ == "__main__":
    serve()
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx, pg, errs = open_app(b, "try{localStorage.setItem('tsb:tour-done','1')}catch(e){}")
        pg.screenshot(path=os.path.join(SHOTS, "00-first-open.png"))
        d = ls_dump(pg, "tsb:")
        print("keys:", sorted(d.keys()))
        print("flag:", d.get("sheepwrld:examples"))
        rep = walk(pg, "a")
        for r in rep: print("  %-12s %-14s %-22s examples-mentioned=%d" % r)
        print("errors:", errs[:10])
        b.close()
