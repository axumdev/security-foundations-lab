from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,re,ast
from course import chapters
from extension_finish import modules

import argparse
cli=argparse.ArgumentParser()
cli.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]/'course')
cli.add_argument('--external',action='store_true')
args=cli.parse_args()
root=args.root
required={'index.html','lab-handbook.html','mentor.html','templates.html','glossary.html','virtualbox.html','extensions.html'}|{f'week-{i:02}.html' for i in range(1,27)}|{m['slug']+'.html' for m in modules}
missing=required-{p.name for p in root.glob('*.html')}
if missing:raise SystemExit(f'Incomplete course at {root}: missing {len(missing)} required pages')
class Parser(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.links=[];self.h1=0;self.lang=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='html':self.lang=d.get('lang')
        if tag=='h1':self.h1+=1
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if tag=='link' and 'href' in d:self.links.append(d['href'])
errors=[];urls=set();words=0
for f in root.glob('*.html'):
    txt=f.read_text(encoding='utf-8');pr=Parser();pr.feed(txt)
    if pr.h1!=1:errors.append(f'{f.name}: h1 count {pr.h1}')
    if pr.lang!='en':errors.append(f'{f.name}: language')
    for link in pr.links:
        if link.startswith('https://'):urls.add(link)
        elif not link.startswith('#') and not (root/unquote(link.split('#')[0])).exists():errors.append(f'{f.name}: missing {link}')
    main=txt.split('<main>',1)[-1].split('<footer',1)[0]
    words+=len(re.sub('<[^>]+>',' ',main).split())
assert sorted(c['n'] for c in chapters)==list(range(1,27))
for c in chapters:
    if not all(c[k] for k in ('concept','run','steps','proof','questions','fix','stretch','links')):errors.append(f"Week {c['n']} incomplete")
assert len(modules)==6
for m in modules:
    assert all(m[k] for k in ('prereq','run','steps','proof','questions','fix','links')),m['slug']
assert not errors,errors
print(json.dumps({'pages':len(list(root.glob('*.html'))),'weeks':len(chapters),'instruction_sections':sum(len(c['steps']) for c in chapters),'main_content_words':words,'unique_external_references':len(urls),'errors':errors},indent=2))
def check(url):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'},method='HEAD')
        with urllib.request.urlopen(req,timeout=15) as r:return {'url':url,'status':r.status,'final':r.url}
    except Exception as e:return {'url':url,'error':str(e)}
if __name__=='__main__' and args.external:
    with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(check,sorted(urls)))
    (Path.cwd()/'reference-check.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps([r for r in results if 'error' in r],indent=2))
