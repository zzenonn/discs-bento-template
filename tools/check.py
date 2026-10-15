"""Bento deck check: validate(), per-slide screenshots, and overflow checks.

Two overflow checks run on every slide: bento.measure() (does the text fit its box
at its font size) and the rendered page (did the browser draw text past its box, or
clip a code block). Both must be clean.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

f = os.path.abspath(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
JS_REPORT = r"""(()=>{
 const st=[...document.querySelectorAll('.ed-stage .bento-slide')].pop(); if(!st) return {err:'no stage'};
 const R=st.getBoundingClientRect(), sc=R.width/1280;
 const doc=window.bento.doc, sid=st.getAttribute('data-slide-id'), s=doc.slides.find(x=>x.id===sid);
 const issues=[];
 // text overflow via bento.measure
 for(const e of s.elements){ if(e.type!=='text'||!e.html) continue;
   const m=window.bento.measure({html:e.html,w:e.w,h:e.h,fontSize:e.fontSize,lineHeight:e.lineHeight,fontFamily:e.fontFamily,fontWeight:e.fontWeight});
   if(m && m.fits===false) issues.push(`overflow ${e.id}: needs ${Math.round(m.height)} > ${e.h}`);
   if(e.x<0||e.y<0||e.x+e.w>1280||e.y+e.h>720) issues.push(`offcanvas ${e.id}`); }
 // text-on-text overlap (excluding intentional label-on-shape)
 const T=s.elements.filter(e=>e.type==='text'&&e.html);
 for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){const a=T[i],b=T[j];
   const m1=window.bento.measure({html:a.html,w:a.w,fontSize:a.fontSize,lineHeight:a.lineHeight,fontFamily:a.fontFamily,fontWeight:a.fontWeight});
   const m2=window.bento.measure({html:b.html,w:b.w,fontSize:b.fontSize,lineHeight:b.lineHeight,fontFamily:b.fontFamily,fontWeight:b.fontWeight});
   const ah=a.valign==='middle'?a.h:Math.min(a.h,m1.height), bh=b.valign==='middle'?b.h:Math.min(b.h,m2.height);
   const ay=a.valign==='middle'?a.y:a.y, by=b.y;
   if(a.x<b.x+b.w&&b.x<a.x+a.w&&ay<by+bh&&by<ay+ah) issues.push(`text overlap ${a.id} / ${b.id}`);}
 // what the browser actually drew: text running past its box, code clipped by its frame
 for(const el of st.querySelectorAll('[data-el-id]')){ const id=el.dataset.elId, b=el.getBoundingClientRect();
   const rg=document.createRange(); rg.selectNodeContents(el); const r=rg.getBoundingClientRect();
   if(r.height>0&&(r.bottom>b.bottom+2||r.right>b.right+2)) issues.push(`drawn past box ${id}: ${Math.round((r.bottom-b.bottom)/sc)}px down, ${Math.round((r.right-b.right)/sc)}px right`);
   for(const c of [el,...el.querySelectorAll('*')]){ if(c.clientHeight>0&&c.scrollHeight>c.clientHeight+2&&getComputedStyle(c).overflow!=='visible'){issues.push(`clipped ${id}: ${c.scrollHeight}>${c.clientHeight}`);break;} } }
 return {sid,issues:[...new Set(issues)]};})()"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1700, "height": 1100}, device_scale_factor=1)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
    pg.goto("file://" + f)
    pg.wait_for_function("window.bento && window.bento.doc && window.bento.doc.slides", timeout=30000)
    pg.wait_for_timeout(1500)
    print("title:", pg.evaluate("window.bento.doc.title"), "| slides:", pg.evaluate("window.bento.doc.slides.length"))
    v = json.loads(pg.evaluate("JSON.stringify(window.bento.validate())"))
    print("validate ok:", v.get("ok"), v.get("counts"))
    for fd in v.get("findings", []):
        if fd.get("severity") != "info":
            print("  ", fd.get("severity"), fd.get("code"), fd.get("slide"), fd.get("element"), fd.get("message", "")[:200])
    print("fonts loaded:", pg.evaluate("[...new Set([...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family+' '+f.weight))].join(', ')"))
    n = pg.locator(".ed-thumb").count()
    bad = 0
    for i in range(n):
        pg.locator(".ed-thumb").nth(i).click(); pg.wait_for_timeout(700)
        pg.mouse.click(1690, 1090)  # deselect
        r = pg.evaluate(JS_REPORT)
        stage = pg.locator(".ed-stage .bento-slide").last
        stage.screenshot(path=f"{out}/s{i+1:02d}.png", animations="disabled")
        if r.get("issues"):
            bad += 1; print(f"slide {i+1} {r['sid']}:", "; ".join(r["issues"]))
    print(f"checked {n} slides, {bad} with issues; page errors: {errs[:3]}")
    b.close()
