import json
from pathlib import Path
from html import escape as esc
from collections import Counter

ROOT = Path(__file__).parent
SITE = ROOT
meta = {p['name']: p for p in json.loads((ROOT / 'catalog' / 'meta-public.json').read_text())}
projects = json.loads((ROOT / 'catalog' / 'projects-curated.json').read_text())
categories = {'imaging': '영상의학·임상', 'research': '연구·학술', 'workflow': '문서·업무 자동화', 'public': '학회·공공의료', 'experiments': '실험·학습', 'web': '프로필·사이트'}
for p in projects:
    m = meta[p['name']]
    p.update(fork=m['fork'], upstream=m.get('parent'), updated=m['pushed_at'][:10], source=f"https://github.com/hwangsi/{p['name']}")
    p['categoryLabel'] = categories[p['category']]
    if p['name'] in ['researcher-kg', 'Abstract-searchme', 'CRO_lecture', 'ksr_repeat_imaging']:
        p['image'] = 'assets/' + {'Abstract-searchme':'abstract-searcher'}.get(p['name'], p['name']) + '.jpg'
(SITE / 'projects.json').write_text(json.dumps(projects, ensure_ascii=False, indent=2) + '\n')
counts = Counter(p['category'] for p in projects)
originals = sum(not p['fork'] for p in projects)

def link(url, label, cls=''):
    return f'<a class="{cls}" href="{esc(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>'

def code_art():
    return '<svg viewBox="0 0 200 115" fill="none" aria-hidden="true"><rect x="25" y="12" width="150" height="88" rx="4" stroke="currentColor" stroke-width="2"/><path d="M25 32h150M36 23h4m5 0h4m5 0h4M93 46l-17 15 17 15m23-30 17 15-17 15m-9-34-9 39M42 87h38m7 0h22" stroke="currentColor" stroke-width="2"/><circle cx="151" cy="76" r="17" fill="#14377d"/><path d="m143 76 5 5 11-12" stroke="white" stroke-width="2"/></svg>'

def feature(p):
    preview = f'<img class="{"demo" if p["name"] == "dicom-viewer" else ""}" src="{esc(p["image"])}" alt="{esc(p["title"])}의 실제 실행 화면" loading="lazy" width="700" height="400">' if p.get('image') else code_art()
    label = '실제 실행 화면' if p.get('image') else 'PI-RADS v2.1 · 단일 HTML'
    live = link(p['live'], '실행하기 ↗') if p.get('live') else link(p['source'] + '#readme', '사용 방법 ↗')
    return f'<article class="feature"><div class="preview">{preview}<span class="preview-label">{label}</span></div><div class="feature-content"><div class="kicker">{esc(p["categoryLabel"])} / {p["featured"]:02}</div><h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p><div class="feature-links">{live}{link(p["source"], "소스 보기 ↗")}</div></div></article>'

def card(p):
    kind = 'fork' if p['fork'] else 'original'
    badge = 'Fork' if p['fork'] else '직접 만든 프로젝트'
    live = link(p['live'], '실행 ↗') if p.get('live') else ''
    parent = f'<div class="upstream">원본: {link("https://github.com/" + p["upstream"], esc(p["upstream"]))}</div>' if p.get('upstream') else ''
    return f'''<article class="project" data-name="{esc(p['name'])}" data-category="{p['category']}" data-type="{kind}" data-updated="{p['updated']}">
<div class="project-top"><span class="project-category">{esc(p['categoryLabel'])}</span><span class="tag {kind}">{badge}</span></div>
<h3>{esc(p['title'])}</h3><p class="repo-name">{esc(p['name'])}</p><p class="desc">{esc(p['summary'])}</p>
<p class="tech">{esc(p['stack'])} · {esc(p['format'])}</p><div class="project-footer"><span class="link-group">{live}{link(p['source'], '저장소 ↗', 'repo-link')}</span><span class="updated">최근 push {p['updated']}</span></div>{parent}</article>'''

filters = '<button type="button" class="category" data-category="all" aria-pressed="true">전체<span class="count">25</span></button>' + ''.join(f'<button type="button" class="category" data-category="{key}" aria-pressed="false">{label}<span class="count">{counts[key]}</span></button>' for key, label in categories.items())
html = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sungil Hwang | 프로젝트 카탈로그</title>
<meta name="description" content="황성일의 영상의학·연구·업무 자동화 프로젝트. 공개 저장소를 분야별로 탐색하고 직접 실행해 보세요."><meta name="theme-color" content="#14377d"><link rel="canonical" href="https://hwangsi.github.io/"><meta property="og:title" content="Sungil Hwang — 프로젝트 카탈로그"><meta property="og:description" content="진료의 질문에서, 쓸 수 있는 도구로. 영상의학·연구·자동화 프로젝트 모음."><meta property="og:type" content="website"><meta property="og:url" content="https://hwangsi.github.io/"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script defer src="app.js"></script></head>
<body><a class="skip" href="#catalog">프로젝트 목록으로 건너뛰기</a><header><div class="wrap"><nav class="nav" aria-label="주 메뉴"><a href="./" class="brand">SUNGIL HWANG<span>PROJECT INDEX</span></a><div class="navlinks"><a href="#featured">대표 프로젝트</a><a href="#catalog">전체 목록</a><a href="https://github.com/hwangsi" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></nav>
<div class="hero"><div><p class="eyebrow">Medical imaging · Research · Automation</p><h1>진료의 질문에서,<br>쓸 수 있는 도구로.</h1><p class="intro">영상의학과 연구, 일상의 업무에서 시작한 아이디어를 코드로 옮깁니다. 직접 만든 도구와 살펴보고 있는 오픈소스 프로젝트를 모았습니다.</p><div class="hero-actions"><a class="button primary" href="#catalog">프로젝트 둘러보기 ↓</a><a class="button" href="#featured">대표작 6개 보기</a></div></div>
<aside class="profile" aria-label="프로필"><p class="name">Sungil Hwang, MD, PhD</p><p class="korean">황성일</p><div class="role">Radiologist · Professor<br>분당서울대학교병원 영상의학과<br>Seoul National University Bundang Hospital</div><div class="profile-links"><a href="https://orcid.org/0000-0001-7516-5369" target="_blank" rel="noopener noreferrer">ORCID ↗</a><a href="https://github.com/hwangsi" target="_blank" rel="noopener noreferrer">@hwangsi ↗</a></div><div class="stats"><div class="stat"><strong>25</strong><span>공개 저장소</span></div><div class="stat"><strong>6</strong><span>탐색 분야</span></div><div class="stat"><strong>16 / 9</strong><span>직접 만든 프로젝트 / Fork</span></div></div></aside></div></div></header>
<main><section class="section" id="featured" aria-labelledby="featured-title"><div class="wrap"><div class="section-head"><div><h2 id="featured-title"><span class="section-number">01</span>대표 프로젝트</h2><p>영상의학 도구에서 연구 시각화, 학회와 공공의료까지.</p></div><a href="#catalog" class="section-link">전체 목록 보기 ↓</a></div><div class="featured-grid">FEATURES</div></div></section>
<section class="section catalog-section" id="catalog" aria-labelledby="catalog-title"><div class="wrap"><div class="section-head"><div><h2 id="catalog-title"><span class="section-number">02</span>프로젝트 카탈로그</h2><p>분야·키워드로 찾아보고, 직접 만든 프로젝트와 Fork를 구분해 보세요.</p></div></div>
<noscript><p>JavaScript가 꺼져 있어 전체 목록을 표시합니다. 검색과 필터는 JavaScript를 켜면 사용할 수 있습니다.</p></noscript>
<div class="toolbar" role="search" aria-label="프로젝트 검색과 필터"><div class="search-row"><div class="search-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 5 5"/></svg><input id="search" type="search" aria-label="프로젝트 검색" placeholder="프로젝트 이름, 기능, 기술로 검색" autocomplete="off"></div><select id="origin" aria-label="프로젝트 유형"><option value="all">모든 프로젝트</option><option value="original">직접 만든 프로젝트</option><option value="fork">Fork만 보기</option></select><select id="sort" aria-label="정렬 방식"><option value="featured">대표 프로젝트 순</option><option value="recent">최근 push 순</option><option value="name">저장소 이름 순</option></select></div><div class="filter-row"><div class="categories" role="group" aria-label="분야 선택">FILTERS</div></div></div>
<div class="catalog-meta"><p id="result-count" role="status" aria-live="polite" aria-atomic="true">25개 프로젝트 / 전체 25개</p><button type="button" data-reset class="reset">필터 초기화</button></div><div class="catalog-grid" id="project-grid">CARDS</div>
<div id="empty" class="empty" hidden><h3>일치하는 프로젝트가 없습니다.</h3><p>검색어를 바꾸거나 분야·유형 필터를 초기화해 보세요.</p><button type="button" data-reset class="button primary" style="border-color:#cbd4e3">전체 목록으로 돌아가기</button></div>
<div class="about"><div><h3>이 목록을 읽는 방법</h3><p>‘직접 만든 프로젝트’는 GitHub에서 Fork로 표시되지 않은 저장소입니다. Fork에는 원본 개발자·저장소 링크를 함께 표시합니다. ‘실행’은 공개 웹앱으로, ‘저장소’는 코드와 설치 안내로 연결됩니다.</p></div><div><h3>공개 프로젝트 기록</h3><p>2026년 10월 29일의 공개 저장소와 README를 기준으로 정리했습니다. 최근 push 날짜는 개발·검증 완료일을 뜻하지 않습니다. 연구·임상 도구의 사용 범위와 주의사항은 각 저장소의 안내를 확인해 주세요.</p></div></div>
</div></section></main><footer><div class="wrap"><span>© 2026 Sungil Hwang · Project Index</span><span>SNUBH · Medical Imaging &amp; AI &nbsp; / &nbsp; <a href="https://github.com/hwangsi/hwangsi.github.io" target="_blank" rel="noopener noreferrer">사이트 소스</a></span></div></footer></body></html>'''
html = html.replace('FEATURES', ''.join(feature(p) for p in projects if p.get('featured'))).replace('FILTERS', filters).replace('CARDS', '\n'.join(map(card, projects)))
(SITE / 'index.html').write_text(html)
(SITE / 'assets' / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="7" fill="#14377d"/><path d="m14 13-8 7 8 7m12-14 8 7-8 7m-3-18-6 22" fill="none" stroke="white" stroke-width="2.6"/></svg>')

readme = '''# Sungil Hwang (황성일 · 黃聖壹)

**Radiologist · Professor**, Department of Radiology, Seoul National University Bundang Hospital (SNUBH)  
**Secretary General**, Korean Society of Radiology (KSR)  
**President**, SNUBH Vibe Lab for Established Clinicians

Building practical tools at the intersection of **medical imaging, research, AI, and clinical workflow**.

[ORCID: 0000-0001-7516-5369](https://orcid.org/0000-0001-7516-5369) · Seongnam, Korea

## [프로젝트 카탈로그 · Project Catalog ↗](https://hwangsi.github.io/)

**[분야별 검색과 필터로 전체 프로젝트 둘러보기 →](https://hwangsi.github.io/#catalog)**  
공개 저장소 25개 · 6개 분야 · 직접 만든 프로젝트와 Fork를 구분해 소개합니다.

## 대표 프로젝트 · Selected Projects

| 프로젝트 | 어떤 일을 하나요? | 이용하기 |
|---|---|---|
'''
for p in projects:
    if not p.get('featured'): continue
    use = f"[실행하기]({p['live']})" if p.get('live') else f"[사용 방법]({p['source']}#readme)"
    readme += f"| [**{p['title']}**]({p['source']}) | {p['summary']} | {use} |\n"
readme += '\n## 직접 만든 프로젝트 · Projects\n\n'
for cat, label in categories.items():
    group = [p for p in projects if p['category'] == cat and not p['fork']]
    if not group: continue
    readme += f'### {label}\n\n| 저장소 | 설명 | 형태 |\n|---|---|---|\n'
    for p in group:
        live = f" · [실행]({p['live']})" if p.get('live') else ''
        readme += f"| [{p['name']}]({p['source']}) | {p['summary']} | {p['format']}{live} |\n"
    readme += '\n'
readme += '<details>\n<summary><strong>살펴보고 있는 오픈소스 · Forks (9)</strong></summary>\n\n아래 저장소는 다른 개발자의 프로젝트를 Fork한 것입니다. 원본 저장소와 저작자를 함께 확인해 주세요.\n\n| Fork | 설명 | 원본 |\n|---|---|---|\n'
for p in projects:
    if not p['fork']: continue
    readme += f"| [{p['name']}]({p['source']}) | {p['summary']} | [{p['upstream']}](https://github.com/{p['upstream']}) |\n"
readme += '\n</details>\n\n---\n\n[전체 카탈로그](https://hwangsi.github.io/) · [Repositories](https://github.com/hwangsi?tab=repositories)  \n공개 저장소 기준: 2026-10-29. 각 도구의 설치 방법과 사용 범위는 해당 README를 확인해 주세요.\n'
(ROOT / 'catalog' / 'profile-README.md').write_text(readme)
print(f'Built {len(projects)} cards, {originals} original repositories, {len(projects)-originals} forks, 6 featured projects.')
