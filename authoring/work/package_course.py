from pathlib import Path
import zipfile,shutil
import build_case
from render_course import render,OUT,ROOT
render()
readme=f"""SECURITY FOUNDATIONS LAB | Public pilot v0.4

Hands-on systems administration, networking, and security engineering.
Build Linux and Windows guests, trace network traffic, test access controls,
investigate alerts, and prove you can restore data.

Extract the complete ZIP. Open index.html in your browser and choose your setup.
Read the lab handbook and begin Week 1. Keep notes outside this folder.

The {len(list(OUT.glob('*.html')))} HTML pages work offline. Plan six hours per core week for 26 weeks.
Optional extensions add about 36 hours. Downloads and cloud exercises need internet.
Learning solo? Use the handbook's self-review checklist. Teaching? Open mentor.html.
The case archive includes an answer key. For assessment, give students only the evidence files.

Pilot status: the first Ubuntu guest was piloted. The full course and the VirtualBox
alternative have not been tested end to end.
"""
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
