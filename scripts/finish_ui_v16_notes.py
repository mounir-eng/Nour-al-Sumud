from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def once(text,old,new,label):
    n=text.count(old)
    if n!=1: raise RuntimeError(f'{label}: {n}')
    return text.replace(old,new,1)

js_path=ROOT/'static/pwa/app.js'
js=js_path.read_text('utf-8')
start=js.index('function profileFromForm()')
end=js.index('function progressPercent',start)
new_block="""async function passwordDigest(value){try{if(crypto&&crypto.subtle){const bytes=new TextEncoder().encode(value);const digest=await crypto.subtle.digest('SHA-256',bytes);return Array.from(new Uint8Array(digest)).map(x=>x.toString(16).padStart(2,'0')).join('')}}catch(e){}let h=2166136261;for(let i=0;i<value.length;i++){h^=value.charCodeAt(i);h=Math.imul(h,16777619)}return 'local-'+(h>>>0).toString(16)}
async function profileFromForm(secretHash){const subjects=[];if($('#physics').checked)subjects.push('physics');if($('#chemistry').checked)subjects.push('chemistry');return{id:(profile&&profile.id)||('local-'+Date.now()),name:$('#name').value.trim(),grade:+$('#grade').value,subjects,passwordHash:secretHash||(profile&&profile.passwordHash)||'',createdAt:(profile&&profile.createdAt)||new Date().toISOString(),mode:'local'}}
$('#profileForm').addEventListener('submit',async event=>{event.preventDefault();const password=$('#password').value,confirm=$('#confirmPassword').value,hasHash=!!(profile&&profile.passwordHash);if($('#name').value.trim().length<2)return toast('اكتب اسمًا من حرفين على الأقل');if(!$('#physics').checked&&!$('#chemistry').checked)return toast('اختر مادة واحدة على الأقل');if(!hasHash||password||confirm){if(password.length<6)return toast('اكتب كلمة مرور من 6 أحرف على الأقل');if(password!==confirm)return toast('كلمة المرور وتأكيدها غير متطابقين')}const secretHash=password?await passwordDigest(password):(profile&&profile.passwordHash)||'';const p=await profileFromForm(secretHash);profile=p;save(PROFILE_KEY,p);$('#password').value='';$('#confirmPassword').value='';showDashboard()});

"""
js=js[:start]+new_block+js[end:]
old_editor="function showProfileEditor(){profile=normalizeProfile(read(PROFILE_KEY,null));if(!profile)return;$('#name').value=profile.name||'';$('#grade').value=profile.grade||12;$('#physics').checked=profile.subjects.includes('physics');$('#chemistry').checked=profile.subjects.includes('chemistry');$('#pin').value=profile.pin||'';$('#dashboard').classList.add('hidden');$('#auth').classList.remove('hidden');$$('.dashboard-only').forEach(x=>x.classList.add('hidden'));scrollTo({top:0,behavior:'smooth'})}"
new_editor="function showProfileEditor(){profile=normalizeProfile(read(PROFILE_KEY,null));if(!profile)return;$('#name').value=profile.name||'';$('#grade').value=profile.grade||12;$('#physics').checked=profile.subjects.includes('physics');$('#chemistry').checked=profile.subjects.includes('chemistry');$('#password').value='';$('#confirmPassword').value='';$('#dashboard').classList.add('hidden');$('#auth').classList.remove('hidden');$$('.dashboard-only').forEach(x=>x.classList.add('hidden'));scrollTo({top:0,behavior:'smooth'})}"
js=once(js,old_editor,new_editor,'pwa editor')
js=js.replace("caches.open('samed-units-v13')","caches.open('samed-units-v16')")
if 'PIN' in js or "$('#pin')" in js: raise RuntimeError('old PIN remains in PWA JS')
js_path.write_text(js,'utf-8')

css_path=ROOT/'static/pwa/dashboard-v13.css'
css=css_path.read_text('utf-8')
marker='/* Account UX v16 */'
if marker not in css:
    css+='''\n/* Account UX v16 */\n.auth-roadmap{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;background:#f7faf9;border-bottom:1px solid var(--ui-line);padding:12px 25px}.auth-roadmap span{font-size:10px;font-weight:850;color:#5d726d;display:flex;align-items:center;gap:6px}.auth-roadmap b{width:23px;height:23px;border-radius:8px;background:#e4f4ee;color:#2c747d;display:grid;place-items:center}.auth-all-subjects{grid-column:1/-1;background:#fff7e4;border:1px solid #efdba5;color:#725a20;border-radius:11px;padding:9px 11px;font-size:10px}.auth-note{background:#edf8f4!important;border-color:#cae6dc!important;color:#3e6a60!important}@media(max-width:680px){.auth-roadmap{grid-template-columns:1fr;padding:11px 21px}}\n'''
css_path.write_text(css,'utf-8')

sw=ROOT/'static/pwa/service-worker.js'
s=sw.read_text('utf-8').replace('samed-core-v13','samed-core-v16').replace('samed-units-v13','samed-units-v16')
sw.write_text(s,'utf-8')
manifest=ROOT/'static/pwa/manifest.webmanifest'
m=manifest.read_text('utf-8').replace('2.0.0-ui13','2.0.0-ui16')
manifest.write_text(m,'utf-8')

# Remove obsolete raw-password fields from existing locally generated profiles only through UI migration behavior.
for p in [ROOT/'landing_component/index.html',ROOT/'dashboard_component/index.html',ROOT/'onboarding_component/index.html',ROOT/'app.py',ROOT/'streamlit_dashboard_v13.py',ROOT/'static/pwa/index.html',js_path,css_path,sw]:
    s=p.read_text('utf-8')
    if '\ufffd' in s: raise RuntimeError(f'replacement character: {p}')
print('UI_V16_REMAINING_NOTES_APPLIED')
