from course import *
from extension_finish import modules,hub
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
    from learner_preview import page as layout
    return layout(title,'<p><a href="index.html#lessons">← Course outline</a></p>'+body)

def render():
    chapters.sort(key=lambda c:c['n'])
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
