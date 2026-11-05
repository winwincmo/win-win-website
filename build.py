#!/usr/bin/env python3
"""Build the Win-Win static site from Markdown articles. python build.py"""
from pathlib import Path
from datetime import datetime, timezone
import json, re, html, shutil, os
import yaml, mistune
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT=Path(__file__).parent
OUT=ROOT/'dist'
site=json.loads((ROOT/'site.json').read_text())
# Automatically use the correct GitHub Pages URL when published from a repo.
site['url']=site['site_url'].rstrip('/')
repo=os.environ.get('GITHUB_REPOSITORY','')
if site['url'] == 'https://example.com' and '/' in repo:
    owner, name = repo.split('/',1)
    site['url'] = f'https://{owner.lower()}.github.io' + ('' if name.lower()==f'{owner.lower()}.github.io' else f'/{name}')
# Supports GitHub Pages project URLs (https://username.github.io/repository).
from urllib.parse import urlparse
site['base_path']=urlparse(site['url']).path.rstrip('/')
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
markdown=mistune.create_markdown(escape=True,plugins=['strikethrough','table'])

def article_from_file(f):
    raw=f.read_text(encoding='utf-8')
    match=re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$',raw,re.S)
    if not match: raise ValueError(f'Missing YAML frontmatter: {f}')
    meta=yaml.safe_load(match.group(1))
    if not meta.get('published',False):return None
    date=meta['date']
    if hasattr(date,'isoformat'):date=date.isoformat()
    slug=f.stem
    return dict(**{**meta,'date':date},slug=slug,url=f'/blog/{slug}/',date_display=datetime.strptime(date,'%Y-%m-%d').strftime('%B %-d, %Y'),body=markdown(match.group(2)),read_time=max(1,round(len(match.group(2).split())/220)))

articles=[x for f in (ROOT/'posts').glob('*.md') if (x:=article_from_file(f))]
articles.sort(key=lambda a:a['date'],reverse=True)
env=Environment(loader=FileSystemLoader(str(ROOT/'templates')),autoescape=select_autoescape(['html']))
def render(rel,template,**kwargs):
    target=OUT/rel
    target.parent.mkdir(parents=True,exist_ok=True)
    output=env.get_template(template).render(site=site,articles=articles,**kwargs)
    if site['base_path']:
        # Prefix root-relative links and assets so GitHub Pages project sites work.
        output=re.sub(r'((?:href|src)=")/(?!/)',lambda m:m.group(1)+site['base_path']+'/',output)
    target.write_text(output,encoding='utf-8')
render('index.html','home.html',latest=articles[:3])
render('blog/index.html','blog.html')
render('faq/index.html','faq.html')
render('approach/index.html','approach.html')
render('services/index.html','services.html')
for a in articles: render(f"blog/{a['slug']}/index.html",'article.html',article=a)
render('404.html','404.html')
# RSS: content summary, permalinks, with proper XML escaping.
from email.utils import format_datetime
from datetime import date
rss=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0"><channel>',f'<title>{html.escape(site["name"])} | Insights</title>',f'<link>{html.escape(site["url"] + "/blog/")}</link>','<description>Ideas for right-fit marketing and revenue growth.</description>']
for a in articles:
    dt=datetime.strptime(a['date'],'%Y-%m-%d').replace(tzinfo=timezone.utc)
    rss.extend(['<item>',f'<title>{html.escape(a["title"])}</title>',f'<link>{html.escape(site["url"]+a["url"])}</link>',f'<guid>{html.escape(site["url"]+a["url"])}</guid>',f'<pubDate>{format_datetime(dt)}</pubDate>',f'<description>{html.escape(a["excerpt"])}</description>','</item>'])
rss+=['</channel></rss>']
(OUT/'feed.xml').write_text('\n'.join(rss),encoding='utf-8')
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {site["url"]}/sitemap.xml\n')
links=['/','/approach/','/services/','/blog/','/faq/']+[a['url'] for a in articles]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{html.escape(site["url"]+u)}</loc></url>' for u in links)+'</urlset>')
print(f'Built {len(articles)} articles in {OUT}')
