// The Sheep Binder — example entries.
//
// The first time the app opens on a phone or computer, this fills every tab with a few
// test entries (Test Lamb, Test Ewe, Test Show...) so each step of the App Tour has
// something to show. Every example's id starts with "ex-". Settings → Examples →
// "Remove examples" takes out only those entries; anything the user added stays,
// even when it's attached to an example animal (that animal is then kept too).
// Once removed, examples never come back on their own (the choice syncs to every device).
(function () {
  "use strict";
  var CFG = window.TSB_CONFIG || {};
  var P = CFG.storagePrefix || "tsb:";
  var FLAG = "sheepwrld:examples";
  var Y = String(CFG.examplesYear || (CFG.years || []).filter(function (y) { return y !== "All Time"; })[0] || new Date().getFullYear());
  var PY = String(+Y - 1);
  function D(md) { return Y + "-" + md; }
  function DP(md) { return PY + "-" + md; }

  function lsGet(k) { try { return localStorage.getItem(P + k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(P + k, v); } catch (e) {} }

  // ------------------------------------------------------------------ data
  function W(id, md, w) { return { id: id, date: D(md), weight: w }; }
  function build() {
    var show = {
      exhibitors: [
        { id: "ex-x1", name: "Test Showman 1", age: "14", county: "Test", numSheep: "2", targetShow: "Test County Fair", targetShowDate: D("07-20"), osf: false },
        { id: "ex-x2", name: "Test Showman 2", age: "11", county: "Test", numSheep: "1", targetShow: "Test County Fair", targetShowDate: D("07-20"), osf: false }
      ],
      sheep: [
        { id: "ex-s1", name: "Test Lamb 1", sex: "Wether", lEar: Y.slice(2) + "001", rEar: "", birthdate: DP("12-15"), breed: "Cross", sire: "Test Sire 1", dam: "Test Ewe 1", breeder: "Test Farm", price: "$600", showman: "Test Showman 1", county: "Test", notes: "Example lamb", inBarn: true, targetWeight: "135", targetDate: D("07-20") },
        { id: "ex-s2", name: "Test Lamb 2", sex: "Ewe Lamb", lEar: Y.slice(2) + "002", rEar: "", birthdate: DP("12-20"), breed: "Southdown", sire: "Test Sire 2", dam: "Test Ewe 2", breeder: "Test Farm", price: "$450", showman: "Test Showman 1", county: "Test", notes: "Example lamb", inBarn: true, targetWeight: "125", targetDate: D("07-20") },
        { id: "ex-s3", name: "Test Lamb 3", sex: "Wether", lEar: Y.slice(2) + "003", rEar: "", birthdate: D("01-04"), breed: "Cross", sire: "Test Sire 1", dam: "Test Ewe 3", breeder: "Test Farm", price: "$500", showman: "Test Showman 2", county: "Test", notes: "Example lamb", inBarn: true, targetWeight: "130", targetDate: D("07-20") }
      ],
      weights: {
        "ex-s1": [W("ex-w11", "03-07", 62), W("ex-w12", "04-04", 80), W("ex-w13", "05-02", 97), W("ex-w14", "06-06", 115), W("ex-w15", "07-04", 129)],
        "ex-s2": [W("ex-w21", "03-07", 55), W("ex-w22", "04-04", 70), W("ex-w23", "05-02", 84), W("ex-w24", "06-06", 101), W("ex-w25", "07-04", 113)],
        "ex-s3": [W("ex-w31", "03-07", 58), W("ex-w32", "04-04", 75), W("ex-w33", "05-02", 91), W("ex-w34", "06-06", 108), W("ex-w35", "07-04", 121)]
      },
      records: {
        "ex-s1": [
          { id: "ex-hr11", date: D("03-01"), type: "Vaccination", product: "Test Vaccine (CD&T)", doseGiven: "2", doseUnit: "mL", withdrawalDays: "21", notes: "Example" },
          { id: "ex-hr12", date: D("04-15"), type: "Dewormer", product: "Test Dewormer", doseGiven: "3", doseUnit: "mL", withdrawalDays: "14", notes: "Example" }
        ],
        "ex-s2": [
          { id: "ex-hr21", date: D("03-01"), type: "Vaccination", product: "Test Vaccine (CD&T)", doseGiven: "2", doseUnit: "mL", withdrawalDays: "21", notes: "Example" }
        ],
        "ex-s3": [
          { id: "ex-hr31", date: D("03-01"), type: "Vaccination", product: "Test Vaccine (CD&T)", doseGiven: "2", doseUnit: "mL", withdrawalDays: "21", notes: "Example" }
        ]
      },
      feedLog: {
        "ex-s1": [
          { id: "ex-f11", date: D("03-07"), lines: [{ id: "ex-f11a", type: "Feed", product: "Test Show Feed", lbs: "1", oz: "8", amt: "" }, { id: "ex-f11b", type: "Hay", product: "Test Hay", lbs: "", oz: "", amt: "2" }] },
          { id: "ex-f12", date: D("05-02"), lines: [{ id: "ex-f12a", type: "Feed", product: "Test Show Feed", lbs: "2", oz: "4", amt: "" }, { id: "ex-f12b", type: "Supplement", product: "Test Supplement", lbs: "", oz: "4", amt: "" }, { id: "ex-f12c", type: "Hay", product: "Test Hay", lbs: "", oz: "", amt: "2" }] }
        ],
        "ex-s2": [
          { id: "ex-f21", date: D("03-07"), lines: [{ id: "ex-f21a", type: "Feed", product: "Test Show Feed", lbs: "1", oz: "4", amt: "" }, { id: "ex-f21b", type: "Hay", product: "Test Hay", lbs: "", oz: "", amt: "2" }] }
        ],
        "ex-s3": [
          { id: "ex-f31", date: D("03-07"), lines: [{ id: "ex-f31a", type: "Feed", product: "Test Show Feed", lbs: "1", oz: "6", amt: "" }, { id: "ex-f31b", type: "Drench", product: "Test Drench", lbs: "", oz: "", amt: "20" }] }
        ]
      },
      customFeeds: [],
      shows: [
        { id: "ex-sw1", name: "Test Spring Show", city: "Test City", state: "OH", date: D("05-16"), judge: "Test Judge", attendees: ["ex-s1", "ex-s2"], notes: "Example show" },
        { id: "ex-sw2", name: "Test County Fair", city: "Test City", state: "OH", date: D("07-20"), judge: "Test Judge", attendees: ["ex-s1", "ex-s2", "ex-s3"], notes: "Example show" }
      ],
      showResults: [
        { id: "ex-r1", showName: "Test Spring Show", exhibitor: "Test Showman 1", sheepId: "ex-s1", showedAs: "Market Lamb — Crossbred", placing: "1st in class" },
        { id: "ex-r2", showName: "Test Spring Show", exhibitor: "Test Showman 1", sheepId: "ex-s2", showedAs: "Southdown Ewe", placing: "3rd in class" },
        { id: "ex-r3", showName: "Test County Fair", exhibitor: "Test Showman 2", sheepId: "ex-s3", showedAs: "Market Lamb — Crossbred", placing: "Reserve Champion" }
      ]
    };

    function E(id, n, tag, bd, br, sire, dam, extra) {
      var o = { id: id, name: n, nickname: "", sex: "Ewe", lEar: tag, rEar: "", birthdate: bd, breed: br, sire: sire, dam: dam, breeder: "Test Farm", born: "2x", reared: "2x", notes: "Example ewe", active: true };
      for (var k in extra || {}) o[k] = extra[k];
      return o;
    }
    var herd = {
      herdSheep: [
        E("ex-h1", "Test Ewe 1", "21001", "2021-01-10", "Cross", "Test Sire 1", "Test Dam A"),
        E("ex-h2", "Test Ewe 2", "22002", "2022-01-14", "Southdown", "Test Sire 2", "Test Dam B"),
        E("ex-h3", "Test Ewe 3", "23003", "2023-01-20", "Cross", "Test Sire 1", "Test Ewe 1")
      ],
      breeding: [
        { id: "ex-b1", ewe: "Test Ewe 1", eweTag: "21001", breedingDate: PY + "-07-20", via: "A.I.", buck: "Test Buck 1", expectedLambing: PY + "-12-14", ultrasound: PY + "-08-30 (2)", actualLambing: PY + "-12-15", carriedToTerm: "2", bornAlive: "2", males: "1", females: "1", notes: "Example" },
        { id: "ex-b2", ewe: "Test Ewe 2", eweTag: "22002", breedingDate: PY + "-07-25", via: "Natural", buck: "Test Buck 2", expectedLambing: PY + "-12-19", ultrasound: "", actualLambing: PY + "-12-20", carriedToTerm: "1", bornAlive: "1", males: "0", females: "1", notes: "Example" },
        { id: "ex-b3", ewe: "Test Ewe 3", eweTag: "23003", breedingDate: Y + "-07-22", via: "A.I.", buck: "Test Buck 1", expectedLambing: Y + "-12-16", ultrasound: "", actualLambing: "", carriedToTerm: "", bornAlive: "", males: "", females: "", notes: "Example — still due" }
      ],
      lambing: [
        { id: "ex-l1", tag: Y.slice(2) + "001", sex: "Male", sire: "Test Buck 1", dam: "Test Ewe 1", dob: PY + "-12-15", soldTo: "Test Buyer", price: "$600", showedBy: "Test Showman 1", notes: "Example lamb" },
        { id: "ex-l2", tag: Y.slice(2) + "004", sex: "Female", sire: "Test Buck 1", dam: "Test Ewe 1", dob: PY + "-12-15", soldTo: "", price: "", showedBy: "", notes: "Example lamb (twin)" },
        { id: "ex-l3", tag: Y.slice(2) + "002", sex: "Female", sire: "Test Buck 2", dam: "Test Ewe 2", dob: PY + "-12-20", soldTo: "Test Buyer", price: "$450", showedBy: "Test Showman 1", notes: "Example lamb" }
      ],
      soldEwes: [
        E("ex-h4", "Test Ewe 4", "19004", "2019-01-12", "Cross", "Test Sire 3", "Test Dam C", { active: false, soldDate: PY + "-09-01", notes: "Example sold ewe" })
      ],
      herdShowResults: [
        { id: "ex-hr1", lambId: "ex-l1", showName: "Test County Fair", showedAs: "Market Lamb — Crossbred", placing: "1st in class" },
        { id: "ex-hr2", lambId: "ex-l3", showName: "Test Spring Show", showedAs: "Southdown Ewe", placing: "3rd in class" }
      ]
    };
    var herdHealth = {
      "ex-h1": [{ id: "ex-hh1", date: D("02-10"), type: "Vaccination", product: "Test Vaccine (CD&T)", doseGiven: "2", doseUnit: "mL", withdrawalDays: "21", notes: "Example" }],
      "ex-h2": [{ id: "ex-hh2", date: D("02-10"), type: "Dewormer", product: "Test Dewormer", doseGiven: "6", doseUnit: "mL", withdrawalDays: "14", notes: "Example" }]
    };
    var bucks = [
      { id: "ex-k1", tag: "22101", name: "Test Buck 1", nickname: "", breed: "Cross", dob: "2022-01-05", sire: "Test Sire 1", dam: "Test Dam A", notes: "Example buck" },
      { id: "ex-k2", tag: "23102", name: "Test Buck 2", nickname: "", breed: "Southdown", dob: "2023-01-08", sire: "Test Sire 2", dam: "Test Dam B", notes: "Example buck" }
    ];
    function R(id, y, tag, sire, dam, sex, br, extra) {
      var o = { id: id, year: y, farmTag: tag, nickname: "", scrapieTag: "", sire: sire, dam: dam, sex: sex, breed: br, showmen: [], notes: "Example" };
      for (var k in extra || {}) o[k] = extra[k];
      return o;
    }
    // Herd View → Lamb Roster (and its Sales)
    var lambRoster = {
      years: [Y],
      roster: [
        R("ex-g1", Y, Y.slice(2) + "001", "Test Buck 1", "21001", "Wether", "Cross"),
        R("ex-g2", Y, Y.slice(2) + "004", "Test Buck 1", "21001", "Ewe", "Cross"),
        R("ex-g3", Y, Y.slice(2) + "002", "Test Buck 2", "22002", "Ewe", "Southdown")
      ],
      sales: [
        { id: "ex-hs1", name: "Test Online Sale", date: D("02-20"), platform: "Online", lots: [
          { id: "ex-hl1", lot: "1", tag: Y.slice(2) + "001", sex: "Wether", breed: "Cross", dob: PY + "-12-15", sire: "Test Buck 1", damTag: "21001", damSire: "Test Sire 1", comments: "Example lot", showmen: [], myPrice: "", finalPrice: "600", soldTo: "Test Buyer", fav: true },
          { id: "ex-hl2", lot: "2", tag: Y.slice(2) + "002", sex: "Ewe", breed: "Southdown", dob: PY + "-12-20", sire: "Test Buck 2", damTag: "22002", damSire: "Test Sire 2", comments: "Example lot", showmen: [], myPrice: "", finalPrice: "450", soldTo: "Test Buyer", fav: false }
        ] }
      ],
      ewes: [], results: [], notes: [], showmen: [], logo: ""
    };
    // Other Farms
    var farm = { id: "ex-f1", name: "Test Farm", colors: null };
    function L(id, lot, tag, sx, sire, dam, ds, dob, fp, c) { return { id: id, lot: lot, tag: tag, sex: sx, breed: "Southdown", dob: dob, sire: sire, damTag: dam, damSire: ds, comments: c || "Example lot", showmen: [], myPrice: "", finalPrice: fp, fav: lot === "1" }; }
    var farmData = {
      years: [Y, PY],
      roster: [
        R("ex-or1", Y, Y.slice(2) + "041", "Test Sire 4", "20012", "Wether", "Southdown"),
        R("ex-or2", Y, Y.slice(2) + "042", "Test Sire 4", "20012", "Ewe", "Southdown"),
        R("ex-or3", PY, PY.slice(2) + "031", "Test Sire 5", "21088", "Wether", "Southdown")
      ],
      sales: [
        { id: "ex-os1", name: "Test Farm Online Sale", date: PY + "-12-20", platform: "Online", lots: [
          L("ex-ol1", "1", Y.slice(2) + "041", "Wether", "Test Sire 4", "20012", "Test Sire 6", PY + "-10-15", "1250", "Example lot — big topped wether"),
          L("ex-ol2", "2", Y.slice(2) + "042", "Ewe", "Test Sire 4", "20012", "Test Sire 6", PY + "-10-15", "900"),
          L("ex-ol3", "3", Y.slice(2) + "050", "Wether", "Test Sire 5", "21088", "Test Sire 7", PY + "-10-20", "1100")
        ] }
      ],
      ewes: [
        { id: "ex-oe1", tag: "20012", name: "Test Ewe A", nickname: "", breed: "Southdown", sire: "Test Sire 6", dob: "2019-12-01", babies: [], notes: "Example" },
        { id: "ex-oe2", tag: "21088", name: "Test Ewe B", nickname: "", breed: "Southdown", sire: "Test Sire 7", dob: "2020-12-01", babies: [], notes: "Example" }
      ],
      bucks: [
        { id: "ex-ok1", tag: "", name: "Test Sire 4", nickname: "", breed: "Southdown", dob: "", sire: "Test Sire 8", dam: "", notes: "Example" },
        { id: "ex-ok2", tag: "", name: "Test Sire 5", nickname: "", breed: "Southdown", dob: "", sire: "Test Sire 9", dam: "", notes: "Example" }
      ],
      results: [
        { id: "ex-ores1", show: "Test Spring Show", date: D("05-16"), lamb: "", lambText: "Test Farm lamb " + Y.slice(2) + "041", showman: "Test Showman 3", showedAs: "Southdown Wether", placing: "Champion" },
        { id: "ex-ores2", show: "Test County Fair", date: D("07-20"), lamb: "", lambText: "Test Farm lamb " + Y.slice(2) + "042", showman: "Test Showman 4", showedAs: "Southdown Ewe", placing: "2nd in class" }
      ],
      notes: [
        { id: "ex-on1", date: D("01-15"), text: "Example note: visited Test Farm, liked lot 1." },
        { id: "ex-on2", date: D("02-02"), text: "Example note: ask about the Test Sire 4 ewe lambs." }
      ],
      showmen: [], logo: ""
    };
    var products = [
      { id: "ex-p1", name: "Test Dewormer", type: "Dewormer", rate: "1", per: "25", unit: "mL", withdrawalDays: "14", notes: "Example product" },
      { id: "ex-p2", name: "Test Vaccine (CD&T)", type: "Vaccination", rate: "", per: "", unit: "mL", withdrawalDays: "21", notes: "Example product" }
    ];
    var customSires = [
      { id: "ex-cs1", name: "Test Sire 1", lineage: "Test Sire A X Test Dam A", owner: "Test Farm", breeder: "", semen: "", listed: "", cat: "custom" },
      { id: "ex-cs2", name: "Test Sire 2", lineage: "Test Sire B X Test Dam B", owner: "Test Farm", breeder: "", semen: "", listed: "", cat: "custom" }
    ];
    var out = {};
    out["sheepwrld:showbarn:" + Y] = show;
    out["sheepwrld:herd"] = herd;
    out["sheepwrld:herdhealth"] = herdHealth;
    out["sheepwrld:bucks"] = bucks;
    out["sheepwrld:of:gehret"] = lambRoster;
    out["sheepwrld:otherfarms"] = [farm];
    out["sheepwrld:of:ex-f1"] = farmData;
    out["sheepwrld:healthproducts"] = products;
    out["sheepwrld:customsires"] = customSires;
    return out;
  }

  // ------------------------------------------------------------------ merge helpers
  function isEx(o) { return o && typeof o === "object" && !Array.isArray(o) && typeof o.id === "string" && o.id.indexOf("ex-") === 0; }
  function srcAllEx(o) { return o && Array.isArray(o._src) && o._src.length && !(o._ov && o._ov.length) && o._src.every(function (s) { return String(s).indexOf("ex-") === 0; }); }
  // Add example values into what's already stored (never replaces a user's records).
  function mergeIn(cur, add) {
    if (cur == null) return add;
    if (Array.isArray(cur) && Array.isArray(add)) {
      var have = {}; cur.forEach(function (x) { if (x && x.id != null) have[x.id] = 1; else if (typeof x === "string") have["s:" + x] = 1; });
      return cur.concat(add.filter(function (x) { return x && x.id != null ? !have[x.id] : !have["s:" + x]; }));
    }
    if (cur && add && typeof cur === "object" && typeof add === "object" && !Array.isArray(cur)) {
      var r = {}; for (var k in cur) r[k] = cur[k];
      for (var j in add) r[j] = mergeIn(cur[j], add[j]);
      return r;
    }
    return cur;
  }

  // ------------------------------------------------------------------ load on first open
  function load() {
    try {
      if (localStorage.getItem(P + "__sm")) return;           // showman phones never get examples
      if (CFG.examples === false) return;
      if (lsGet(FLAG)) return;                                  // already loaded or removed once
      var data = build();
      Object.keys(data).forEach(function (k) {
        var cur = null; try { cur = JSON.parse(lsGet(k) || "null"); } catch (e) {}
        lsSet(k, JSON.stringify(mergeIn(cur, data[k])));
      });
      // make sure the example year is in the year list
      var ys = null; try { ys = JSON.parse(lsGet("sheepwrld:years") || "null"); } catch (e) {}
      if (Array.isArray(ys) && ys.indexOf(Y) < 0) { ys.unshift(Y); lsSet("sheepwrld:years", JSON.stringify(ys)); }
      if (!lsGet("gx:ofcur")) lsSet("gx:ofcur", JSON.stringify("ex-f1"));
      lsSet(FLAG, JSON.stringify({ state: "loaded", year: Y, at: Date.now() }));
    } catch (e) { console.error("[examples] load", e); }
  }

  // ------------------------------------------------------------------ remove
  // Returns the pruned value. keep = ids of example records the user's own entries point to.
  function collectRefs(v, refs, inEx) {
    if (Array.isArray(v)) { v.forEach(function (x) { collectRefs(x, refs, inEx); }); return; }
    if (!v || typeof v !== "object") return;
    var ex = inEx || isEx(v) || srcAllEx(v);
    for (var k in v) {
      if (k === "id" || k === "_src" || k === "_ov") continue;
      var x = v[k];
      if (!ex) {
        if (typeof x === "string" && x.indexOf("ex-") === 0) refs[x] = 1;
        if (Array.isArray(x)) x.forEach(function (y) { if (typeof y === "string" && y.indexOf("ex-") === 0) refs[y] = 1; });
        // a map keyed by an example animal holding the user's own entries
        if (k.indexOf("ex-") === 0 && hasUser(x)) refs[k] = 1;
      }
      collectRefs(x, refs, ex);
    }
  }
  function hasUser(v) {
    if (Array.isArray(v)) return v.some(function (x) { return x && typeof x === "object" ? !(isEx(x) || srcAllEx(x)) || hasUser(x) : false; });
    if (v && typeof v === "object") { if (!isEx(v) && !srcAllEx(v) && v.id != null) return true; for (var k in v) if (hasUser(v[k])) return true; }
    return false;
  }
  function prune(v, keep) {
    if (Array.isArray(v)) {
      return v.filter(function (x) {
        if (typeof x === "string" && x.indexOf("ex-") === 0) return !!keep[x];
        if (isEx(x)) return !!keep[x.id];
        if (srcAllEx(x)) return false;
        return true;
      }).map(function (x) { return prune(x, keep); });
    }
    if (v && typeof v === "object") {
      var r = {};
      for (var k in v) {
        if (k.indexOf("ex-") === 0 && !keep[k]) { var pv = prune(v[k], keep); if (Array.isArray(pv) ? pv.length : (pv && typeof pv === "object" ? Object.keys(pv).length : pv != null)) r[k] = pv; continue; }
        r[k] = (k === "_src" || k === "_ov") ? v[k] : prune(v[k], keep);
      }
      if (isEx(r) && keep[r.id]) { /* kept example: leave as is */ }
      return r;
    }
    return v;
  }
  function allKeys() {
    var out = [];
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf(P + "sheepwrld:") === 0 && k.indexOf(P + "__") !== 0) out.push(k.slice(P.length));
    }
    return out;
  }
  function removeAll(silent, fromRemote) {
    var keys = allKeys().filter(function (k) { return k !== FLAG && k.indexOf("sheepwrld:seeded:") !== 0 && k.indexOf("sheepwrld:backup") !== 0; });
    var vals = {}; keys.forEach(function (k) { try { vals[k] = JSON.parse(lsGet(k)); } catch (e) {} });
    // which examples does the user's own data point at? keep those (repeat until nothing new)
    var keep = {}, n = -1;
    while (Object.keys(keep).length !== n) {
      n = Object.keys(keep).length;
      Object.keys(vals).forEach(function (k) { collectRefs(prune(vals[k], keep), keep, false); });
    }
    var writes = [], dels = [];
    Object.keys(vals).forEach(function (k) {
      var m = /^sheepwrld:of:(ex-.+)$/.exec(k);
      if (m && !keep[m[1]] && !hasUser(vals[k])) { dels.push(k); return; }
      var nv = prune(vals[k], keep);
      if (JSON.stringify(nv) !== JSON.stringify(vals[k])) writes.push([k, JSON.stringify(nv)]);
    });
    var cur = null; try { cur = JSON.parse(lsGet("gx:ofcur") || "null"); } catch (e) {}
    if (cur === "ex-f1" && !keep["ex-f1"]) { try { localStorage.removeItem(P + "gx:ofcur"); } catch (e) {} }
    var st = window.storage;
    var jobs = writes.map(function (w) { return st && st.set ? st.set(w[0], w[1]) : (lsSet(w[0], w[1]), null); })
      .concat(dels.map(function (k) { return st && st.delete ? st.delete(k) : (localStorage.removeItem(P + k), null); }));
    if (!fromRemote) {
      var flag = JSON.stringify({ state: "removed", at: Date.now() });
      jobs.push(st && st.set ? st.set(FLAG, flag) : (lsSet(FLAG, flag), null));
    }
    return Promise.all(jobs).then(function () { return { changed: writes.length + dels.length, kept: Object.keys(keep) }; });
  }

  window.tsbExamplesPresent = function () {
    try { var f = JSON.parse(lsGet(FLAG) || "null"); return !!(f && f.state === "loaded"); } catch (e) { return false; }
  };
  window.tsbRemoveExamples = function (silent) {
    if (!silent && !confirm("Remove all the example entries (Test Lamb, Test Ewe, Test Show and the rest)?\n\nAnything you've added yourself stays.")) return Promise.resolve(null);
    return removeAll(silent).then(function (r) {
      if (!silent) { try { sessionStorage.setItem(P + "exRemoved", "1"); } catch (e) {} setTimeout(function () { window.location.reload(); }, 300); }
      return r;
    });
  };
  // Another device removed them: clean this one up too (called by sync.js).
  window.tsbExamplesRemote = function () {
    try { var f = JSON.parse(lsGet(FLAG) || "null"); if (f && f.state === "removed") return removeAll(true, true); } catch (e) {}
    return Promise.resolve(null);
  };
  window.tsbExamplesBuild = build; // for testing

  load();
})();
