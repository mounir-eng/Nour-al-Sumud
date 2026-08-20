from __future__ import annotations
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PWA = ROOT / "static" / "pwa"
sys.path.insert(0, str(ROOT))


def one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)


# 1) Activate the remedial v12 content overlay.
content_path = ROOT / "foundation_content.py"
content = content_path.read_text("utf-8")
marker = "\n# FOUNDATION_SIMPLIFIED_V12\n"
if marker in content:
    content = content.split(marker, 1)[0].rstrip() + "\n"
content += marker + "from foundation_simplified_v12 import apply_simplification as _apply_foundation_simplification_v12\n_apply_foundation_simplification_v12(FOUNDATION_COURSES)\n"
content_path.write_text(content, "utf-8")

# 2) Streamlit: show one-sentence meaning, arrows, and inputs inside equations.
renderer_path = ROOT / "foundation_renderer.py"
r = renderer_path.read_text("utf-8")
if "# FOUNDATION_SIMPLE_INLINE_V12" not in r:
    css = r'''

# FOUNDATION_SIMPLE_INLINE_V12
_FOUNDATION_SIMPLE_CSS_V12 = r"""
<style>
.rv-simple-sentence{background:#eef9ff;border:2px solid #a9d8ee;border-radius:17px;padding:16px 18px;margin:0 0 10px;color:#173f59;font-size:22px!important;line-height:2!important;font-weight:850;direction:rtl;text-align:right;unicode-bidi:plaintext}
.rv-simple-sentence b{color:var(--rv-accent);font-size:18px}
.rv-vector-note{direction:ltr!important;unicode-bidi:isolate!important;text-align:center!important;background:#fff;border:2px solid var(--rv-accent);border-radius:15px;padding:13px 15px;margin:8px 0 12px;font:900 23px/1.8 Consolas,"Noto Sans Arabic",monospace;color:var(--rv-deep)}
.rv-symbolic-copy{background:#f7fafc;border:1px solid #dce7ed;border-radius:14px;padding:12px;margin-top:10px}.rv-symbolic-copy>small{display:block;font-size:16px;color:#617887;font-weight:850;margin-bottom:5px}
.rv-inline-guide{direction:rtl;text-align:right;background:#fff7e8;border:1px solid #f0d29a;border-radius:13px;padding:12px 14px;margin-bottom:10px;font-size:18px;line-height:1.9;color:#76551e}.rv-inline-guide b{display:block;color:#8f5e08;font-size:20px}
.rv-inline-next{direction:rtl;text-align:right;font-size:18px;font-weight:850;color:#425f72;margin:13px 2px 6px}
.rv-inline-token{direction:ltr!important;unicode-bidi:isolate!important;display:flex;align-items:center;justify-content:center;min-height:54px;white-space:nowrap;font:900 25px Consolas,"Courier New",monospace;color:var(--rv-deep)}
div[data-testid="stForm"]:has(.rv-inline-guide){background:#f8fbfd;border:2px solid #d5e4ec;border-radius:17px;padding:14px!important}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stHorizontalBlock"]{direction:ltr!important;align-items:center!important;gap:.35rem!important;overflow-x:auto;padding:3px 2px 7px}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"]{min-width:74px!important}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"] input{direction:ltr!important;text-align:center!important;font:900 22px Consolas,"Courier New",monospace!important;color:var(--rv-deep)!important;background:#fff!important;border:0!important;border-bottom:3px solid var(--rv-accent)!important;border-radius:8px 8px 3px 3px!important;padding:8px 5px!important;min-width:72px!important}
div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"] input:focus{box-shadow:0 0 0 3px var(--rv-soft)!important}
@media(max-width:820px){.rv-simple-sentence{font-size:20px!important}.rv-vector-note{font-size:19px!important}.rv-inline-guide,.rv-inline-next{font-size:17px!important}.rv-inline-token{font-size:21px!important;min-height:49px}div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"]{min-width:64px!important}div[data-testid="stForm"]:has(.rv-inline-guide) div[data-testid="stTextInput"] input{font-size:20px!important;min-width:62px!important}}
</style>
"""
'''
    r = one(r, "\n\ndef _esc(value: Any) -> str:", css + "\n\ndef _esc(value: Any) -> str:", "renderer css insertion")
    r = one(r, "    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)\n", "    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)\n    st.markdown(_FOUNDATION_SIMPLE_CSS_V12, unsafe_allow_html=True)\n", "renderer css call")
    r = one(
        r,
        "        st.markdown('<div class=\"rv-card\"><h3>الفكرة بهدوء</h3>' + ''.join(f'<p class=\"rv-paragraph\">{_mixed(p)}</p>' for p in lesson[\"explanation\"]) + '<div class=\"rv-points\">' + ''.join(f'<div class=\"rv-point\">✓ {_mixed(p)}</div>' for p in lesson[\"key_points\"]) + '</div></div>', unsafe_allow_html=True)\n",
        "        if lesson.get(\"simple_sentence\"):\n            st.markdown(f'<div class=\"rv-simple-sentence\"><b>الفكرة في جملة واحدة</b><br>{_mixed(lesson[\"simple_sentence\"])}</div>', unsafe_allow_html=True)\n        st.markdown('<div class=\"rv-card\"><h3>نفهمها كلمة كلمة</h3>' + ''.join(f'<p class=\"rv-paragraph\">{_mixed(p)}</p>' for p in lesson[\"explanation\"]) + '<div class=\"rv-points\">' + ''.join(f'<div class=\"rv-point\">✓ {_mixed(p)}</div>' for p in lesson[\"key_points\"]) + '</div></div>', unsafe_allow_html=True)\n",
        "simple sentence",
    )
    r = one(
        r,
        "        st.markdown(_visual(lesson[\"visual\"]), unsafe_allow_html=True)\n",
        "        st.markdown(_visual(lesson[\"visual\"]), unsafe_allow_html=True)\n        if lesson.get(\"direction_note\"):\n            st.markdown(f'<div class=\"rv-vector-note\">{_esc(lesson[\"direction_note\"])}</div>', unsafe_allow_html=True)\n",
        "direction arrows",
    )

    old = '''        st.markdown(f'<div class="rv-card"><div class="rv-example-head"><div><h3>مثال موجّه: {_mixed(ex["title"])}</h3><p class="rv-example-q">{_mixed(ex["question"])}</p></div><span>أنت تنفذ التعويض</span></div><div class="rv-givens">{givens}</div><div class="rv-plan">{plan}</div><div class="rv-substitution">{_esc(ex["substitution"])}</div></div>', unsafe_allow_html=True)

        ex_ok_key = f"{prefix}_{lesson['id']}_example_ok"
        ex_msg_key = f"{prefix}_{lesson['id']}_example_msg"
        attempts_key = f"{prefix}_{lesson['id']}_attempts"
        with st.form(f"{prefix}_{lesson['id']}_example_form"):
            field_values: list[tuple[dict[str, Any], str]] = []
            cols = st.columns(min(3, max(1, len(ex["fields"]))))
            for i, field in enumerate(ex["fields"]):
                with cols[i % len(cols)]:
                    value = st.text_input(
                        _plain_mixed(f"{field['label']} ({field.get('unit','')})").strip(),
                        key=f"{prefix}_{lesson['id']}_field_{field['key']}",
                        placeholder=field.get("placeholder", ""),
                    )
                    field_values.append((field, value))
            result_value = st.text_input(
                _plain_mixed(f"{ex['result']['label']} ({ex['result'].get('unit','')})").strip(),
                key=f"{prefix}_{lesson['id']}_result",
                placeholder=ex["result"].get("placeholder", ""),
            )
            submitted = st.form_submit_button("تحقق من التعويض والحساب", type="primary", use_container_width=True)
'''
    new = '''        st.markdown(f'<div class="rv-card"><div class="rv-example-head"><div><h3>مثال موجّه: {_mixed(ex["title"])}</h3><p class="rv-example-q">{_mixed(ex["question"])}</p></div><span>أنت تضع القيم داخل العلاقة</span></div><div class="rv-givens">{givens}</div><div class="rv-plan">{plan}</div><div class="rv-symbolic-copy"><small>1. العلاقة كاملة بالرموز</small><div class="rv-substitution">{_esc(lesson["formula"])}</div></div></div>', unsafe_allow_html=True)

        ex_ok_key = f"{prefix}_{lesson['id']}_example_ok"
        ex_msg_key = f"{prefix}_{lesson['id']}_example_msg"
        attempts_key = f"{prefix}_{lesson['id']}_attempts"
        with st.form(f"{prefix}_{lesson['id']}_example_form"):
            st.markdown(f'<div class="rv-inline-guide"><b>2. عوّض داخل العلاقة نفسها</b>{_mixed(ex.get("inline_help", "ضع كل عدد مكان رمزه في الفراغ."))}</div>', unsafe_allow_html=True)
            field_values: list[tuple[dict[str, Any], str]] = []
            field_by_key = {field["key"]: field for field in ex["fields"]}
            inline_parts = [part for part in re.split(r"(\\[\\[[A-Za-z0-9_]+\\]\\])", ex["inline_template"]) if part]
            inline_weights = [1.15 if part.startswith("[[") else max(0.75, min(3.2, len(part.strip()) / 4 or 0.75)) for part in inline_parts]
            inline_cols = st.columns(inline_weights)
            for i, part in enumerate(inline_parts):
                with inline_cols[i]:
                    match = re.fullmatch(r"\\[\\[([A-Za-z0-9_]+)\\]\\]", part)
                    if match:
                        field = field_by_key[match.group(1)]
                        value = st.text_input(
                            _plain_mixed(field["label"]),
                            key=f"{prefix}_{lesson['id']}_field_{field['key']}",
                            placeholder="…",
                            label_visibility="collapsed",
                        )
                        field_values.append((field, value))
                    else:
                        st.markdown(f'<div class="rv-inline-token">{_esc(part)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="rv-inline-next">3. نفّذ العملية ثم اكتب النتيجة في الفراغ الأخير</div>', unsafe_allow_html=True)
            result_value = ""
            result_parts = [part for part in re.split(r"(\\[\\[[A-Za-z0-9_]+\\]\\])", ex["result_template"]) if part]
            result_weights = [1.2 if part == "[[__result]]" else max(0.75, min(3.2, len(part.strip()) / 4 or 0.75)) for part in result_parts]
            result_cols = st.columns(result_weights)
            for i, part in enumerate(result_parts):
                with result_cols[i]:
                    if part == "[[__result]]":
                        result_value = st.text_input(
                            _plain_mixed(ex["result"]["label"]),
                            key=f"{prefix}_{lesson['id']}_result",
                            placeholder="…",
                            label_visibility="collapsed",
                        )
                    else:
                        st.markdown(f'<div class="rv-inline-token">{_esc(part)}</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("تحقق من التعويض والحساب", type="primary", use_container_width=True)
'''
    r = one(r, old, new, "streamlit inline equation form")
    r = r.replace("صحيح: اخترت القيم المناسبة ونفذت الحساب دون تغيير العلاقة.", "صحيح: وضعت القيم في أماكن رموزها داخل العلاقة، ثم حسبت الناتج.")
    renderer_path.write_text(r, "utf-8")

# 3) PWA: native inputs embedded in the equation line.
js_path = PWA / "foundation.js"
js = js_path.read_text("utf-8")
if "FOUNDATION_INLINE_V12" not in js:
    helper = r'''
/* FOUNDATION_INLINE_V12 */
function inlineEquation(template,example,T){
 const meta=Object.fromEntries(example.fields.map(f=>[f.key,f]));
 return String(template||'').split(/(\[\[[A-Za-z0-9_]+\]\])/g).filter(Boolean).map(part=>{
  const m=part.match(/^\[\[([A-Za-z0-9_]+)\]\]$/);if(!m)return `<span class="rv-inline-token">${esc(part)}</span>`;
  const key=m[1],info=key==='__result'?example.result:meta[key]||{};
  return `<input class="rv-inline-input" name="${esc(key)}" inputmode="decimal" autocomplete="off" value="${esc(T.values[key]||'')}" placeholder="…" aria-label="${esc(info.label||'فراغ في العلاقة')}">`;
 }).join('');
}
'''
    js = one(js, "function render(){", helper + "function render(){", "pwa helper")
    pattern = re.compile(r"\n const fields=L\.example\.fields\.map\(f=>.*?\.join\(''\);\n const solution=", re.S)
    match = pattern.search(js)
    if not match:
        raise RuntimeError("PWA fields declaration not found")
    js = js[:match.start()] + "\n const inlineSub=inlineEquation(L.example.inline_template,L.example,T);\n const inlineResult=inlineEquation(L.example.result_template,L.example,T);\n const solution=" + js[match.end():]
    js = one(js, '</div><section class="rv-card"><h3>الفكرة بهدوء</h3>', '</div>${L.simple_sentence?`<div class="rv-simple-sentence"><b>الفكرة في جملة واحدة</b><br>${mixed(L.simple_sentence)}</div>`:""}<section class="rv-card"><h3>نفهمها كلمة كلمة</h3>', "pwa simple sentence")
    js = one(js, '${visual(L.visual)}<section class="rv-formula">', '${visual(L.visual)}${L.direction_note?`<div class="rv-vector-note">${esc(L.direction_note)}</div>`:""}<section class="rv-formula">', "pwa arrows")
    start = '<div class="rv-plan">${plan}</div><div class="rv-substitution">'
    end = '<button class="rv-action" type="submit">تحقق من التعويض والحساب</button></form>'
    a = js.find(start)
    b = js.find(end, a)
    if a < 0 or b < 0:
        raise RuntimeError("PWA example form segment not found")
    b += len(end)
    replacement = '<div class="rv-plan">${plan}</div><div class="rv-symbolic-copy"><small>1. العلاقة كاملة بالرموز</small><div class="rv-substitution">${esc(L.formula)}</div></div><form id="exampleForm"><div class="rv-inline-guide"><b>2. عوّض داخل العلاقة نفسها</b>${mixed(L.example.inline_help||"ضع كل عدد مكان رمزه في الفراغ.")}</div><div class="rv-inline-equation">${inlineSub}</div><div class="rv-inline-next">3. نفّذ العملية ثم اكتب النتيجة في الفراغ الأخير</div><div class="rv-inline-equation result">${inlineResult}</div><button class="rv-action" type="submit">تحقق من التعويض والحساب</button></form>'
    js = js[:a] + replacement + js[b:]
    js = js.replace("صحيح: اخترت القيم المناسبة ونفذت الحساب دون تغيير العلاقة.", "صحيح: وضعت القيم في أماكن رموزها داخل العلاقة، ثم حسبت الناتج.")
    js_path.write_text(js, "utf-8")

# 4) Shared PWA styles for the new interaction.
css_path = PWA / "review.css"
css_text = css_path.read_text("utf-8")
if "FOUNDATION_ULTRA_SIMPLE_INLINE_V12" not in css_text:
    css_text += r'''

/* FOUNDATION_ULTRA_SIMPLE_INLINE_V12 */
.foundation-page .rv-simple-sentence{background:#eef9ff;border:2px solid #a9d8ee;border-radius:17px;padding:16px 18px;margin:0 0 10px;color:#173f59;font-size:22px!important;line-height:2!important;font-weight:850;direction:rtl;text-align:right;unicode-bidi:plaintext}
.foundation-page .rv-simple-sentence b{display:inline-block;color:var(--rv-accent);font-size:18px;margin-bottom:2px}
.foundation-page .rv-vector-note{direction:ltr!important;unicode-bidi:isolate!important;text-align:center!important;background:#fff;border:2px solid var(--rv-accent);border-radius:15px;padding:13px 15px;margin:8px 0 12px;font:900 23px/1.8 Consolas,"Noto Sans Arabic",monospace;color:var(--rv-deep);overflow-wrap:anywhere}
.foundation-page .rv-symbolic-copy{background:#f7fafc;border:1px solid #dce7ed;border-radius:14px;padding:12px;margin-top:10px}.foundation-page .rv-symbolic-copy>small{display:block;font-size:16px;color:#617887;font-weight:850;margin-bottom:5px}
.foundation-page .rv-inline-guide{direction:rtl;text-align:right;background:#fff7e8;border:1px solid #f0d29a;border-radius:13px;padding:12px 14px;margin:12px 0 10px;font-size:18px;line-height:1.9;color:#76551e}.foundation-page .rv-inline-guide b{display:block;color:#8f5e08;font-size:20px}
.foundation-page .rv-inline-next{direction:rtl;text-align:right;font-size:18px;font-weight:850;color:#425f72;margin:14px 2px 7px}
.foundation-page .rv-inline-equation{direction:ltr!important;unicode-bidi:isolate!important;display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:8px;background:var(--rv-soft);border:2px dashed var(--rv-accent);border-radius:15px;padding:15px 12px;min-height:78px}
.foundation-page .rv-inline-equation.result{background:#f7fafc;border-style:solid}
.foundation-page .rv-inline-token{direction:ltr!important;unicode-bidi:isolate!important;white-space:pre-wrap;font:900 25px/1.5 Consolas,"Courier New",monospace;color:var(--rv-deep)}
.foundation-page .rv-inline-input{width:86px;min-width:64px;direction:ltr!important;text-align:center!important;font:900 23px Consolas,"Courier New",monospace;color:var(--rv-deep);background:#fff;border:0;border-bottom:4px solid var(--rv-accent);border-radius:9px 9px 3px 3px;padding:9px 5px;outline:none;box-shadow:0 2px 8px rgba(20,58,80,.08)}
.foundation-page .rv-inline-input:focus{box-shadow:0 0 0 4px color-mix(in srgb,var(--rv-accent) 18%,transparent)}.foundation-page .rv-inline-input::placeholder{color:#9badb8}
@media(max-width:820px){.foundation-page .rv-simple-sentence{font-size:20px!important}.foundation-page .rv-vector-note{font-size:19px!important}.foundation-page .rv-inline-guide,.foundation-page .rv-inline-next{font-size:17px}.foundation-page .rv-inline-equation{gap:6px;padding:13px 8px}.foundation-page .rv-inline-token{font-size:21px}.foundation-page .rv-inline-input{width:69px;min-width:58px;font-size:20px;padding:8px 3px}}
'''
    css_path.write_text(css_text, "utf-8")

# 5) Regenerate course data after activating the overlay.
from foundation_content import PHYSICS_FOUNDATION, CHEMISTRY_FOUNDATION
for subject, course in (("physics", PHYSICS_FOUNDATION), ("chemistry", CHEMISTRY_FOUNDATION)):
    payload = "window.REVIEW_COURSE = " + json.dumps(course, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (PWA / f"unit-{subject}-foundation-data.js").write_text(payload, "utf-8")

# 6) Versions and documentation.
sw = PWA / "service-worker.js"
sw_text = sw.read_text("utf-8").replace("samed-core-v11", "samed-core-v12").replace("samed-units-v11", "samed-units-v12")
sw.write_text(sw_text, "utf-8")
app_path = ROOT / "app.py"
app_text = app_path.read_text("utf-8")
app_text = re.sub(r'DASHBOARD_UX_VERSION\s*=\s*"[^"]+"', 'DASHBOARD_UX_VERSION = "dashboard-ux-v10-ultra-simple-inline"', app_text, count=1)
app_path.write_text(app_text, "utf-8")
readme = ROOT / "README_AR.md"
readme_text = readme.read_text("utf-8")
if "## تبسيط علاجي إضافي v12" not in readme_text:
    readme_text += "\n\n## تبسيط علاجي إضافي v12\n\n- الفكرة الأساسية في جملة واحدة قبل الشرح.\n- استعمال الأسهم لتمثيل اتجاهات الكميات المتجهة في الفيزياء.\n- عرض العلاقة كاملة بالرموز أولًا.\n- تعويض الطالب مباشرة داخل فراغات مدمجة في سطر المعادلة، لا في خانات منفصلة.\n- عدم كشف القيم أو الحل قبل مشاركة الطالب.\n"
    readme.write_text(readme_text, "utf-8")

print("FOUNDATION_V12_APPLIED")
