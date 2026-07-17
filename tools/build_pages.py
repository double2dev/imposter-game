import os
import datetime
import json

BASE_URL = "https://impostergamewords.com"
TEMPLATE_APP = "template.html"
TEMPLATE_ARTICLE = "article_template.html"
DIST_DIR = "html"

def load_data():
    app_pages = []
    if os.path.exists("apps"):
        for file in os.listdir("apps"):
            if file.endswith(".json"):
                with open(os.path.join("apps", file), "r", encoding="utf-8") as f:
                    app_pages.append(json.load(f))
                    
    article_pages = []
    if os.path.exists("articles"):
        for file in os.listdir("articles"):
            if file.endswith(".json"):
                with open(os.path.join("articles", file), "r", encoding="utf-8") as f:
                    article_pages.append(json.load(f))
                    
    # Sort them by filename to keep deterministic builds, though optional
    app_pages.sort(key=lambda x: x['filename'])
    article_pages.sort(key=lambda x: x['filename'])
    return app_pages, article_pages

def build():
    app_pages, article_pages = load_data()
    
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    # Read Templates
    try:
        with open(TEMPLATE_APP, "r", encoding="utf-8") as f:
            app_template = f.read()
        
        # 【新增】读取西班牙语模版
        with open("template_es.html", "r", encoding="utf-8") as f:
            es_template = f.read()
            
        with open(TEMPLATE_ARTICLE, "r", encoding="utf-8") as f:
            article_template = f.read()
    except FileNotFoundError:
        print("Templates not found. Make sure template.html, template_es.html and article_template.html exist.")
        return

    generated_files = []

    # 1. Build App Pages
    print("Building App Pages...")
    for page in app_pages:
        current_template = es_template if page.get("template_id") == "es" else app_template
        content = current_template.replace("{{title}}", page["title"]) \
                              .replace("{{description}}", page["description"]) \
                              .replace("{{h1}}", page["h1"]) \
                              .replace("{{article_intro}}", page["article_intro"])
        
        # Canonical Logic
        if page['filename'] == 'index.html':
            canonical_url = BASE_URL + "/"
        else:
            canonical_url = f"{BASE_URL}/{page['filename'].replace('.html', '')}"
        content = content.replace("{{canonical}}", canonical_url)
        
        # JS Logic
        js = f"window.defaultCategory = '{page['category']}';" if page.get("category") != "standard" else ""
        content = content.replace("__CUSTOM_SCRIPT__", js) # 确保模板里是 {{custom_script}}
        
        # Footer Badge Logic - Only show on homepage
        if page['filename'] == 'index.html':
            footer_badge = """
            <div class="mt-4 flex flex-col md:flex-row justify-center items-center gap-4 md:gap-6">
                <a href='https://www.saashub.com/imposter-game-word-generator?utm_source=badge&utm_campaign=badge&utm_content=imposter-game-word-generator&badge_variant=color&badge_kind=approved' target='_blank'><img src="https://cdn-b.saashub.com/img/badges/approved-color.png?v=1" alt="Imposter Game Word Generator badge" style="max-width: 150px;"/></a>
                <div style="font-size: 0.85rem;">
                    <a 
                        href="https://www.trustpilot.com/review/impostergamewords.com" 
                        target="_blank" 
                        rel="nofollow noopener" 
                        style="display: inline-flex; align-items: center; gap: 6px; color: #64748b; border: 1px solid #00b67a; border-radius: 12px; padding: 8px 16px; text-decoration: none;"
                    >
                        <span>Review us on</span>
                        <strong style="color: #00b67a; font-weight: 700; display: inline-flex; align-items: center;">★ Trustpilot</strong>
                    </a>
                </div>
            </div>"""
        else:
            footer_badge = ""
        content = content.replace("{{footer_badge}}", footer_badge)
        
        # SEO Article Logic - Only show on homepage
        if page['filename'] == 'index.html':
            seo_article = """
        <!-- Always Visible SEO Article -->
        <article id="seo-article"
            class="bg-slate-900/50 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl">
            <h2 class="text-2xl font-bold text-cyber-primary mb-6 border-b border-white/10 pb-4">The Ultimate Imposter
                Game Word List & Guide</h2>

            <div class="space-y-6 text-slate-300 leading-relaxed">

                <p>
                    Need an <strong class="text-white">Imposter game unblocked</strong> for school or work?
                    ImposterGameWords.com is a lightweight, browser-based tool that works on any device without
                    downloads. It's the perfect way to kill time during breaks or recess, offering a safe and accessible
                    way to play your favorite social deduction game anywhere, anytime.
                </p>

                <div>
                    <h3 class="text-xl font-bold text-cyber-primary mb-3">How to play Imposter Game</h3>
                    <ol class="list-decimal list-inside space-y-2 marker:text-cyber-secondary">
                        <li><strong class="text-white">Setup:</strong> Select your player count and choose a category.
                            Hand the device to the first player.</li>
                        <li><strong class="text-white">Reveal & Pass:</strong> Each player taps to see their secret
                            word. Civilians get the same word; the Imposter gets "IMPOSTER".</li>
                        <li><strong class="text-white">Discuss & Vote:</strong> Ask questions to find the liar! If
                            you're the Imposter, try to guess the word to win.</li>
                    </ol>
                </div>

                <p class="pt-4 border-t border-white/10 text-sm text-center text-slate-400">
                    Start playing now at <a href="https://impostergamewords.com"
                        class="text-cyber-secondary hover:text-white transition-colors">ImposterGameWords.com</a> and
                    become the master of deception!
                </p>
            </div>
        </article>
"""
        elif page.get("template_id") == "es" and page['filename'] == 'imposter-game-espanol.html':
            seo_article = """
        <article id="seo-article"
            class="bg-slate-900/50 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl animate-fade-in">
            <h2 class="text-2xl font-bold text-cyber-primary mb-6 border-b border-white/10 pb-4">Guía Completa de Quién es el Espía en Español</h2>

            <div class="space-y-6 text-slate-300 leading-relaxed">
                <p>
                    Esta edición en español está enfocada en utilidad real: reglas claras, ritmo de mesa y ejemplos que funcionan
                    en conversaciones naturales. No es una traducción literal de otra URL: está escrita para reuniones familiares,
                    clases y grupos de amigos hispanohablantes.
                </p>

                <div>
                    <h3 class="text-xl font-bold text-cyber-primary mb-3">Cómo sacar mejores partidas</h3>
                    <ol class="list-decimal list-inside space-y-2 marker:text-cyber-secondary">
                        <li><strong class="text-white">Antes de empezar:</strong> define si la ronda será casual, aula o competitiva.</li>
                        <li><strong class="text-white">Durante pistas:</strong> usa frases cortas y evita sinónimos demasiado obvios.</li>
                        <li><strong class="text-white">En votación:</strong> pide una razón breve por persona para reducir votos aleatorios.</li>
                    </ol>
                </div>

                <div>
                    <h3 class="text-xl font-bold text-cyber-primary mb-3">FAQ rápida</h3>
                    <ul class="space-y-2 text-sm">
                        <li><strong class="text-white">¿Sirve para clase?</strong> Sí, con turnos fijos y palabras acordes a edad.</li>
                        <li><strong class="text-white">¿Cuántos jugadores?</strong> De 6 a 9 suele dar la mejor discusión.</li>
                        <li><strong class="text-white">¿Qué aporta esta página?</strong> Estrategias y ejemplos propios para contexto hispanohablante.</li>
                    </ul>
                </div>
            </div>
        </article>
"""
        else:
            seo_article = ""

        content = content.replace("{{seo_article}}", seo_article)
        
        # Featured Articles Logic
        if page['filename'] == 'index.html':
            # Homepage: Fixed 3 articles
            featured_articles_html = """<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Featured Deep Guide 1 -->
                <a href="/imposter-game-host-guide-teachers-teams"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">Imposter Host Guide for Teachers & Team Leads</h3>
                    <p class="text-sm text-slate-400">Run better sessions with concrete facilitation formats, fairness rules, and debrief playbooks.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Featured Deep Guide 2 -->
                <a href="/how-to-create-balanced-imposter-word-pairs"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">How to Create Balanced Imposter Word Pairs</h3>
                    <p class="text-sm text-slate-400">Use a repeatable framework to design fair but challenging word pairs that improve game quality.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Article 1: How to Win -->
                <a href="/10-tips-to-win-as-imposter"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">How
                        to Win Imposter Word Game: 10 Pro Strategies</h3>
                    <p class="text-sm text-slate-400">Stop getting caught! The ultimate strategy guide with pro tips on
                        how to lie, bluff, and win.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Article 2: Zoom Games -->
                <a href="/best-zoom-word-games-no-app"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">Best
                        Zoom Word Games for Teams</h3>
                    <p class="text-sm text-slate-400">Host a virtual game night easily. No app download required, works
                        in browser.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Article 3: Hardest Words -->
                <a href="/50-hardest-imposter-game-words"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">50+
                        Hardest Imposter Game Words</h3>
                    <p class="text-sm text-slate-400">Expert level only. Extremely similar word pairs that make it
                        nearly impossible to bluff.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Article 4: How to Play -->
                <a href="/how-to-play-imposter-game"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">How to Play Imposter Game Guide</h3>
                    <p class="text-sm text-slate-400">Complete rules, winning strategies, and pro tips for both Civilians and Imposters in 2026.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Article 5: Words List -->
                <a href="/best-imposter-game-words-list"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">Ultimate Imposter Words List 2025</h3>
                    <p class="text-sm text-slate-400">500+ hard, funny, and spicy ideas categorized for couples, kids, and experts.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>

                <!-- Article 6: Strategic Questions -->
                <a href="/best-questions-to-ask-in-imposter-game"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">Best Strategic Trap Questions</h3>
                    <p class="text-sm text-slate-400">Want to catch the liar instantly? Use these smart, trap-setting questions in your next game.</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>
            </div>
            
            <!-- View All Button -->
            <div class="mt-8 text-center">
                <a href="/resources"
                    class="inline-block px-8 py-3 bg-transparent border-2 border-cyber-primary text-cyber-primary font-bold rounded-xl hover:bg-cyber-primary hover:text-cyber-bg transition-all hover:shadow-[0_0_20px_rgba(57,255,20,0.3)] transform hover:scale-105">
                    View All Guides & Word Lists →
                </a>
            </div>"""
        else:
            # Other game pages: Random 3 articles from data_articles.py
            import random
            priority_filenames = {
                'imposter-game-host-guide-teachers-teams.html',
                'how-to-create-balanced-imposter-word-pairs.html'
            }
            priority_articles = [a for a in article_pages if a['filename'] in priority_filenames]
            remaining_articles = [a for a in article_pages if a['filename'] not in priority_filenames]
            random_articles = priority_articles + random.sample(remaining_articles, max(0, min(3, len(article_pages)) - len(priority_articles)))
            
            articles_html_parts = []
            for article in random_articles:
                # Truncate description to ~100 chars
                desc = article['description']
                if len(desc) > 100:
                    desc = desc[:97] + "..."
                
                article_html = f"""<a href="/{article['filename'].replace('.html', '')}"
                    class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
                    <h3 class="text-lg font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">{article['title'].replace(' | ', '<br class="hidden md:block">').split('|')[0].strip()}</h3>
                    <p class="text-sm text-slate-400">{desc}</p>
                    <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read
                        More &rarr;</span>
                </a>"""
                articles_html_parts.append(article_html)
            
            featured_articles_html = f"""<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {chr(10).join(articles_html_parts)}
            </div>"""
        
        content = content.replace("{{featured_articles}}", featured_articles_html)
        
        with open(os.path.join(DIST_DIR, page["filename"]), "w", encoding="utf-8") as f:
            f.write(content)
        generated_files.append(page["filename"])

    # 2. Build Article Pages (包括 About/Contact/Privacy)
    print("Building Article Pages...")
    for page in article_pages:
        content = article_template.replace("{{title}}", page["title"]) \
                                  .replace("{{description}}", page["description"]) \
                                  .replace("{{h1}}", page["h1"]) \
                                  .replace("{{article_content}}", page["article_content"])
        
        # Canonical Logic
        canonical_url = f"{BASE_URL}/{page['filename'].replace('.html', '')}"
        content = content.replace("{{canonical}}", canonical_url)
        
        with open(os.path.join(DIST_DIR, page["filename"]), "w", encoding="utf-8") as f:
            f.write(content)
        generated_files.append(page["filename"])

    # 3. Build Resources Page
    build_resources_page(article_template, article_pages)
    generated_files.append("resources.html")

    # 4. Copy Assets
    assets = ["styles.css", "app.js", "manifest.json", "robots.txt", "_headers", "logo.png", "favicon.ico", "ads.txt", "404.html", "llms.txt", "llms-full.txt"]
    for asset in assets:
        if os.path.exists(asset):
            mode = "rb" if asset.endswith((".png", ".ico")) else "r"
            with open(asset, mode, encoding=None if mode=="rb" else "utf-8") as src:
                data = src.read()
            with open(os.path.join(DIST_DIR, asset), "wb" if mode=="rb" else "w", encoding=None if mode=="rb" else "utf-8") as dst:
                dst.write(data)
    
    # 5. Sitemap
    generate_sitemap(generated_files)
    print("Build Complete!")

def build_resources_page(template, articles):
    # 手动添加 Christmas (置顶推荐)
    list_html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6">'

    list_html += """
        <a href="/imposter-game-host-guide-teachers-teams" class="block p-6 bg-cyber-glass border border-cyber-primary/40 rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1 relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-cyber-primary text-cyber-bg text-[10px] font-bold px-2 py-1 rounded-bl-lg">FEATURED</div>
            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">Imposter Host Guide for Teachers & Team Leads</h3>
            <p class="text-sm text-slate-400">Facilitation systems, fairness rules, and debrief methods for classrooms and team sessions.</p>
            <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read More &rarr;</span>
        </a>

        <a href="/how-to-create-balanced-imposter-word-pairs" class="block p-6 bg-cyber-glass border border-cyber-primary/40 rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1 relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-cyber-primary text-cyber-bg text-[10px] font-bold px-2 py-1 rounded-bl-lg">FEATURED</div>
            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">How to Create Balanced Imposter Word Pairs</h3>
            <p class="text-sm text-slate-400">A practical framework to design clear, fair, and challenging pairs across different play modes.</p>
            <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read More &rarr;</span>
        </a>
    """

    for page in articles:
        # 排除 Trust Pages 和已置顶推荐，避免在 Resources 列表重复出现
        if page['filename'] in [
            'about-us.html',
            'contact-us.html',
            'privacy-policy.html',
            'imposter-game-host-guide-teachers-teams.html',
            'how-to-create-balanced-imposter-word-pairs.html'
        ]:
            continue

        clean_link = page['filename'].replace('.html', '')
        list_html += f"""
        <a href="/{clean_link}" class="block p-6 bg-cyber-glass border border-cyber-glassBorder rounded-xl hover:border-cyber-primary group transition-all hover:-translate-y-1">
            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-cyber-primary transition-colors">{page['title'].split('|')[0]}</h3>
            <p class="text-sm text-slate-400">{page['description']}</p>
            <span class="inline-block mt-4 text-xs font-bold text-cyber-secondary uppercase tracking-wider">Read More &rarr;</span>
        </a>
        """
    list_html += """
        <a href="/christmas-imposter-game-words" class="block p-6 bg-slate-800/50 border border-white/5 rounded-xl hover:border-white/10 group transition-all opacity-60 hover:opacity-100">
            <div class="absolute top-0 right-0 bg-slate-700 text-slate-400 text-[10px] font-bold px-2 py-1 rounded-bl-lg">PAST</div>
            <h3 class="text-xl font-bold text-slate-500 mb-2 group-hover:text-red-400 transition-colors">🎄 Christmas Edition</h3>
            <p class="text-sm text-gray-500">Archived holiday words from 2025.</p>
            <span class="inline-block mt-4 text-xs font-bold text-slate-600 uppercase tracking-wider">View Archive &rarr;</span>
        </a>
    """
    list_html += '</div>'

    content = template.replace("{{title}}", "Imposter Game Resources | Word Lists & Guides") \
                      .replace("{{description}}", "Browse our collection of Imposter Game word lists.") \
                      .replace("{{h1}}", 'GAME <span class="text-cyber-primary">RESOURCES</span>') \
                      .replace("{{article_content}}", list_html) \
                      .replace("{{canonical}}", f"{BASE_URL}/resources")
    
    with open(os.path.join(DIST_DIR, "resources.html"), "w", encoding="utf-8") as f:
        f.write(content)

def generate_sitemap(files):
    content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    today = datetime.date.today().isoformat()
    for f in files:
        if f == "index.html":
            url = BASE_URL + "/"
        else:
            url = f"{BASE_URL}/{f.replace('.html', '')}"
        content += f"  <url><loc>{url}</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>\n"
    content += '</urlset>'
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    build()