from pathlib import Path
import zipfile,shutil
import build_case
from render_course import render,OUT,ROOT
render()
readme='''SECURITY FOUNDATIONS LAB — Edition 1.1 (September 2026)

START: Open index.html in a browser. No installation or server is required
to read the course. Keep all HTML files and style.css together.

26 core weeks plus six security-platform extensions • 6–12 hours/week
38 HTML pages, including Elastic/ELK, Splunk, and Security Onion labs.
Core: 156 planned hours. Extensions: 36 additional hours.
At 9 hours/week, use the 26-week expanded schedule in extensions.html.
At 6 hours/week, the expanded course takes 32 calendar weeks.
case-m01.zip contains synthetic events, PCAP, hashes, and an answer key.

Reading/navigation work offline. External documentation links, software
downloads, and cloud exercises need internet. The archive's download link
returns to this same package; keep course-offline.zip alongside extracted
files if you want that link to work offline too.

Begin with lab-handbook.html, then week-01.html. Instructor: mentor.html.

Baseline: 16 GB Windows 11 Pro laptop; staged VM power profiles.
Assumptions to confirm: administrator/BIOS access, weekly mentor review,
Azure cloud sandbox provided in Week 23. English is confirmed.

Validation: HTML entrypoints and local references checked; all 26 lessons
have prerequisites, steps, evidence, questions, troubleshooting, and optional
practice. Official technical references checked during authoring. Selected
configuration syntax and the log-summary exercise were checked separately.
No Hyper-V guests, Wazuh deployment, or Azure resources were executed for
this authoring task. Pilot the course and record actual versions/timings
before using it with a wider cohort.

REUSE: HTML/CSS can be edited directly and hosted on a static web server.
An optional authoring source archive accompanies the delivered course.
No accounts, grades, payment processing, or shared learner state are built in.
No OS installers or third-party binaries are redistributed.
A public/open-source content license has not been selected.
'''
(OUT/'START-HERE.txt').write_text(readme,encoding='utf-8')
archive=OUT.parent/'security-foundations-offline.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):
        if f.name=='index.html':
            offline=f.read_text(encoding='utf-8').replace('<a href="course-offline.zip">Download the complete offline HTML course</a>','<a href="START-HERE.txt">Offline usage instructions</a>')
            z.writestr(f.name,offline)
        elif f.suffix in ('.html','.css','.txt') or f.name=='case-m01.zip':z.write(f,f.name)
shutil.copy2(archive,OUT/'course-offline.zip')
site=ROOT/'work'/'site'/'dist'
for f in OUT.iterdir():
    if f.is_file():shutil.copy2(f,site/f.name)
src=OUT.parent/'security-foundations-authoring-source.zip'
with zipfile.ZipFile(src,'w',zipfile.ZIP_DEFLATED) as z:
    for name in ('course.py','support_pages.py','extensions.py','extension_finish.py','build_case.py','learner_preview.py','render_course.py','package_course.py','validate_course.py'):
        z.write(ROOT/'work'/name,'work/'+name)
    z.writestr('README.txt','Extract into an empty directory. Requires Python 3.10+ standard library. Run python work/package_course.py to regenerate outputs/security-foundations and work/site/dist. Edit course.py for lessons, support_pages.py for handbook/mentor/templates, render_course.py for layout. No deployment credentials or hosting identifiers are included. The generated static HTML is also editable directly.\n')
print(archive)
print(src)
