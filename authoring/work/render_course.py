from course import *
from extension_finish import modules,hub
STYLE='''
:root{--ink:#192a3a;--muted:#536574;--blue:#145b88;--line:#d4dfe7;--paper:#fff;--bg:#edf2f6;--accent:#0d736a}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--blue);text-underline-offset:3px}a:hover{color:var(--accent)}.top{background:#132b40;color:white;padding:18px 32px;display:flex;justify-content:space-between;gap:20px;align-items:center}.top a{color:white;text-decoration:none}.brand{font-weight:750;letter-spacing:.02em}.top small{color:#c0d1df}.layout{display:grid;grid-template-columns:280px minmax(0,1fr);max-width:1440px;margin:auto}.sidebar{padding:28px 20px;position:sticky;top:0;max-height:100vh;overflow:auto}.sidebar a{display:block;padding:7px 12px;font-size:14px;text-decoration:none;border-left:2px solid transparent}.sidebar a.active{border-color:var(--accent);background:#dceae9;font-weight:700}.sidebar .group{font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin:22px 12px 6px;color:var(--muted)}main{background:var(--paper);padding:44px 58px;min-width:0;min-height:100vh}h1{font-size:clamp(30px,4vw,48px);line-height:1.12;letter-spacing:-.035em;margin:12px 0 22px}h2{font-size:27px;line-height:1.25;margin-top:46px}h3{font-size:20px;line-height:1.4;margin:0 0 15px}p{margin:14px 0}.eyebrow{font-size:13px;font-weight:750;letter-spacing:.13em;text-transform:uppercase;color:var(--accent)}.lead{font-size:20px;color:var(--muted);max-width:770px}.meta{display:flex;gap:12px;flex-wrap:wrap;margin:25px 0}.tag{background:#eef3f7;border:1px solid var(--line);padding:5px 12px;font-size:14px}.note{border-left:4px solid var(--accent);padding:16px 20px;background:#edf6f5;margin:25px 0}.step{margin:32px 0;padding-top:28px;border-top:1px solid var(--line)}.command{margin:18px 0;background:#142a3a;color:#e5f0f6;border-radius:4px;overflow:hidden}.terminal-label{padding:9px 16px;background:#233e51;color:#c1dee8;font:12px/1.5 system-ui;letter-spacing:.04em}pre{margin:0;padding:18px;overflow:auto;font:14px/1.7 Consolas,monospace;tab-size:2}code{font-family:Consolas,monospace}table{width:100%;border-collapse:collapse;margin:22px 0;font-size:15px}th,td{text-align:left;padding:12px;border-bottom:1px solid var(--line);vertical-align:top}th{background:#eef3f7}.tablewrap{overflow:auto}.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:24px}.card{display:block;text-decoration:none;border:1px solid var(--line);padding:20px;color:var(--ink)}.card:hover{border-color:var(--accent)}.card strong{display:block;font-size:20px;margin:8px 0}.card span{font-size:14px;color:var(--muted)}.footer{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}.next{display:flex;justify-content:space-between;gap:20px;margin-top:32px}li{margin:8px 0}.button{display:inline-block;background:var(--blue);color:white;padding:10px 18px;text-decoration:none;margin:8px 8px 8px 0}.button:hover{color:white;background:var(--accent)}details{border:1px solid var(--line);padding:16px;margin:16px 0}summary{cursor:pointer;font-weight:700}svg{max-width:100%;height:auto}@media(max-width:850px){.layout{display:block}.sidebar{position:static;max-height:240px;padding:10px 20px;border-bottom:1px solid var(--line)}main{padding:28px 22px}.cards{grid-template-columns:1fr}.top{padding:16px 22px}.top small{display:none}}@media print{.top,.sidebar,.next,.button{display:none}.layout{display:block}main{padding:0}body{background:white;font-size:11pt}h1{font-size:26pt}h2{break-after:avoid}.step{break-inside:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;color:black;background:#eee;font-size:9pt}.command{color:black;background:#eee}.terminal-label{background:#ddd;color:black}a{color:inherit}.card{break-inside:avoid}}
'''
def nav(current):
    s='<a href="index.html">Course overview</a><a href="lab-handbook.html">Lab handbook</a><a href="mentor.html">Mentor guide</a><a href="templates.html">Evidence templates</a><a href="glossary.html">Glossary &amp; troubleshooting</a>'
    last=None
    for c in chapters:
        if c['phase']!=last:s+='<div class="group">'+c['phase']+'</div>';last=c['phase']
        s+='<a '+('class="active" ' if current==c['n'] else '')+'href="week-%02d.html">%02d · %s</a>'%(c['n'],c['n'],html.escape(c['title']))
    s+='<div class="group">Security platform extensions</div><a href="extensions.html">Schedule, case &amp; assessment</a>'
    for m in modules:s+='<a href="'+m['slug']+'.html">'+m['title']+'</a>'
    return s
def page(title,body,current=None):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A six-month hands-on cybersecurity course: operating systems, networks, identity, detection, response, and cloud."><title>'+html.escape(title)+' · Security Foundations Lab</title><link rel="stylesheet" href="style.css"></head><body><header class="top"><a class="brand" href="index.html">SECURITY FOUNDATIONS / LAB</a><small>Build it. Explain it. Test it. Recover it.</small></header><div class="layout"><nav class="sidebar" aria-label="Course navigation">'+nav(current)+'</nav><main>'+body+'<footer class="footer">Course edition 1.1 · September 2026 · Instructor-led lab material. Commands require the named guest and prerequisites. Documentation checked during authoring; VM execution remains a learner/mentor validation step.</footer></main></div></body></html>'
def render():
    chapters.sort(key=lambda c:c['n'])
    (OUT/'style.css').write_text(STYLE,encoding='utf-8')
    for c in chapters:
        body='<div class="eyebrow">Week %02d / %s</div><h1>%s</h1>'%(c['n'],c['phase'],c['title'])
        body+='<div class="meta"><span class="tag">6 hours core</span><span class="tag">+ 0–6 hours practice</span><span class="tag">Prerequisite: '+('Week %02d'%(c['n']-1) if c['n']>1 else 'Start here')+'</span></div>'
        body+=p(c['concept'])+note('<strong>Power-on plan:</strong> '+c['run'])
        if c['n'] in (11,12,13,14,16):body+=p('For dashboard access and file transfers, use the complete <a href="lab-handbook.html">temporary management procedure in the lab handbook</a>, including the explicit host key path and cleanup checks.')
        body+=p('<strong>Your week:</strong> Session A (2 h): read, prepare, begin the first steps. Session B (2 h): finish the build and tests. Session C (2 h): troubleshoot, write evidence, and complete mentor review. These are planning estimates; use extra hours for repeats. If a gate fails, carry it forward before dependent labs.')
        if c['n']>=14:body+=note('<strong>Expanded track:</strong> See the <a href="extensions.html">six security-platform labs and schedule</a> for Elastic, Splunk, and Security Onion. Budget these hours separately from the core; complete their comparison report for the final review.')
        body+=''.join(c['steps'])
        body+='<h2>Pass this week</h2>'+ul(*c['proof'])+'<h3>Explain without the guide</h3>'+ul(*c['questions'])
        body+='<h3>If something fails</h3>'+p(c['fix'])+'<h3>Optional practice · 0–6 extra hours</h3>'+p(c['stretch'])
        if c['links']:body+=refs(*c['links'])
        body+='<div class="next"><a href="'+('week-%02d.html'%(c['n']-1) if c['n']>1 else 'index.html')+'">← Previous</a>'
        if c['n']<len(chapters):body+='<a href="week-%02d.html">Next week →</a>'%(c['n']+1)
        body+='</div>'
        (OUT/('week-%02d.html'%c['n'])).write_text(page(c['title'],body,c['n']),encoding='utf-8')
    body='<div class="eyebrow">26-week practical course</div><h1>Learn security by building<br>the systems it protects.</h1><p class="lead">A guided path from your first Linux VM to an investigated incident and a secured cloud workload. Start with the lab handbook, then complete the weeks in order.</p><div class="meta"><span class="tag">6 months</span><span class="tag">6–12 hours / week</span><span class="tag">16 GB laptop path</span><span class="tag">English</span></div><a class="button" href="lab-handbook.html">Read the lab handbook</a><a class="button" href="week-01.html">Begin Week 01</a>'
    body+=note('<strong>Outcome:</strong> Build, configure, test, troubleshoot, and explain a small security environment across operating systems, networks, identity, applications, monitoring, recovery, and cloud. This is a foundation for junior security work—not a promise of mastery, certification, or employment.')
    body+='<h2>Your learning rhythm</h2>'+p('The core path is 156 planned hours: 26 weeks × 6 hours. At 9 hours weekly you have 234 hours; at 12, 312. The additional time is for repetition, deeper investigation, and optional exercises. Installation time varies. Keep the order and extend a difficult week when needed; do not substitute screenshots of commands for understanding.')
    body+='<h2>New: Elastic, Splunk &amp; Security Onion</h2>'+p('Six guided extensions add 36 planned hours of pipeline engineering, search, detection testing, packet investigation, and platform comparison. Includes a downloadable synthetic case and a staged 16 GB laptop plan. <a href="extensions.html">Open the extension track and choose a schedule →</a>')
    body+='<h2>The course</h2><div class="cards">'
    for c in chapters:body+='<a class="card" href="week-%02d.html"><span>WEEK %02d · %s</span><strong>%s</strong><span>%s</span></a>'%(c['n'],c['n'],c['phase'].upper(),c['title'],c['proof'][0])
    body+='</div><h2>For the instructor</h2>'+p('Use the <a href="mentor.html">mentor guide</a> to assess explanations, select controlled faults, and decide whether to advance. The learner instructions are intentionally explicit; mentor reviews should gradually remove that scaffolding. Later publication can retain this static HTML structure without requiring a learning-management system.')
    body+=p('<a href="course-offline.zip">Download the complete offline HTML course</a> · <a href="templates.html">Evidence templates</a>. Download and extract the ZIP, then open index.html. Reading/navigation work offline; software downloads, external references, and cloud labs require internet.')
    (OUT/'index.html').write_text(page('Course overview',body),encoding='utf-8')
    for name,title,body in extra_pages():
        body+=note('<strong>Expanded course:</strong> The <a href="extensions.html">security-platform track</a> contains the added VM profiles, six-module schedule, mentor rubric, answer key, and comparison-report template. Its separate review network is for benign file investigation only; follow each module’s power-on and access plan.')
        (OUT/(name+'.html')).write_text(page(title,body),encoding='utf-8')
    (OUT/'extensions.html').write_text(page('Security platform extensions',hub()),encoding='utf-8')
    for i,m in enumerate(modules):
        body='<div class="eyebrow">Security platform extensions / Module '+str(i+1)+'</div><h1>'+m['title']+'</h1>'
        body+=p('<strong>Prerequisites:</strong> '+m['prereq'])+p('<strong>Time:</strong> Three two-hour sessions: build, test, review. Extend the estimate if installation or a failed gate needs more time.')
        body+=note('<strong>Power-on plan:</strong> '+m['run'])+p(m['intro'])+''.join(m['steps'])
        body+='<h2>Pass this module</h2>'+ul(*m['proof'])+'<h3>Explain without the guide</h3>'+ul(*m['questions'])+'<h3>If something fails</h3>'+p(m['fix'])+refs(*m['links'])
        body+='<div class="next"><a href="extensions.html">← Track overview</a>'
        if i+1<len(modules):body+='<a href="'+modules[i+1]['slug']+'.html">Next module →</a>'
        body+='</div>'
        (OUT/(m['slug']+'.html')).write_text(page(m['title'],body),encoding='utf-8')
    from learner_preview import render_preview
    render_preview(OUT,chapters)
    site=ROOT/'work'/'site'/'dist';site.mkdir(parents=True,exist_ok=True)
    import shutil
    for f in OUT.iterdir():
        if f.is_file() and f.suffix in ('.html','.css','.txt'):shutil.copy2(f,site/f.name)
from support_pages import extra_pages
if __name__=='__main__':render()
