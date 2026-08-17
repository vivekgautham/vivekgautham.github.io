#!/usr/bin/env python3
"""
Zero-Dependency Local Preview Server for Vivek's Jekyll Site.
Usage: python3 preview.py [port]
Default URL: http://localhost:4000
"""

import http.server
import socketserver
import re
import html
from pathlib import Path
from datetime import datetime

PORT = 4000
BASE_DIR = Path(__file__).resolve().parent

def parse_frontmatter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                fm_text = parts[1]
                data = {}
                for line in fm_text.strip().splitlines():
                    if ':' in line:
                        k, v = line.split(':', 1)
                        k = k.strip()
                        v = v.strip()
                        if v.startswith('[') and v.endswith(']'):
                            items = [x.strip(' "\'') for x in v[1:-1].split(',') if x.strip()]
                            data[k] = items
                        else:
                            data[k] = v.strip(' "\'')
                return data, parts[2].strip()
            except Exception:
                pass
    return {}, content

def markdown_to_html(md_text):
    def code_repl(match):
        lang = (match.group(1) or 'code').strip()
        code = html.escape(match.group(2).strip('\n'))
        return f'<div class="language-{lang} highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{code}</code></pre></div></div>'
    
    md_text = re.sub(r'```([a-zA-Z0-9_\+#\s]*)\n(.*?)```', code_repl, md_text, flags=re.DOTALL)
    md_text = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_text)
    md_text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', md_text)
    md_text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md_text)
    md_text = re.sub(r'_(.+?)_', r'<em>\1</em>', md_text)
    md_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', md_text)
    md_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', md_text)
    md_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md_text)
    
    lines = md_text.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        if re.match(r'^\s*[-*]\s+(.+)$', line):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            item_text = re.sub(r'^\s*[-*]\s+', '', line)
            new_lines.append(f'  <li>{item_text}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    
    paragraphs = '\n'.join(new_lines).split('\n\n')
    processed_p = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<') and (p.startswith('<h') or p.startswith('<ul') or p.startswith('<div') or p.startswith('<blockquote') or p.startswith('<img')):
            processed_p.append(p)
        else:
            processed_p.append(f'<p>{p.replace("\n", "<br>")}</p>')
            
    return '\n'.join(processed_p)

def load_posts():
    posts_dir = BASE_DIR / '_posts'
    posts = []
    if not posts_dir.exists():
        return posts
    
    for f in sorted(posts_dir.glob('*.md'), reverse=True):
        fname = f.name
        m = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$', fname)
        if not m:
            continue
        year, month, day, slug = m.groups()
        raw = f.read_text(encoding='utf-8')
        fm, body = parse_frontmatter(raw)
        
        title = fm.get('title', slug.replace('-', ' ').title())
        date_str = f"{year}-{month}-{day}"
        url = f"/blog/{year}/{month}/{day}/{slug}"
        
        post_obj = {
            'title': title,
            'date': date_str,
            'date_formatted': datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y"),
            'url': url,
            'tags': fm.get('tags', []),
            'categories': fm.get('categories', []),
            'content': body,
            'html_content': markdown_to_html(body),
        }
        posts.append(post_obj)
    return posts

def render_layout(layout_name, content, page_meta):
    layout_file = BASE_DIR / '_layouts' / f"{layout_name}.html"
    if not layout_file.exists():
        return content
    
    layout_content = layout_file.read_text(encoding='utf-8')
    fm, layout_template = parse_frontmatter(layout_content)
    
    rendered = layout_template
    page_title = page_meta.get('title', 'Vivek Soundararaj')
    rendered = rendered.replace("{{ page.title }}", page_title)
    rendered = rendered.replace("{{ page.date | date: \"%B %d, %Y\" }}", page_meta.get('date_formatted', ''))
    rendered = rendered.replace("{{ page.date | date_to_string }}", page_meta.get('date_formatted', ''))
    rendered = rendered.replace("{{ site.name }}", "Vivek Soundararaj")
    rendered = rendered.replace("{{ site.title }}", "Vivek Soundararaj · Systems & Algorithms")
    rendered = rendered.replace("{{ site.description }}", "Notes on modern C++, algorithms, data structures, and systems engineering.")
    rendered = rendered.replace("{{ '/css/main.css' | relative_url }}", "/css/main.css")
    rendered = rendered.replace("{{ 'now' | date: \"%Y\" }}", "2026")
    
    words = len(content.split())
    read_time = max(1, words // 200)
    rendered = rendered.replace("{{ read_time }}", str(read_time))
    
    rendered = rendered.replace("{{ content }}", content)
    
    # Strip any unresolved liquid conditional tags for cleaner local HTML
    rendered = re.sub(r'\{%\s*if\s+page\.url\s+contains\s+\'/blog\'\s*%\}\s*active\s*\{%\s*endif\s*%\}', 'active' if page_meta.get('url', '') == '/blog' else '', rendered)
    rendered = re.sub(r'\{%\s*if\s+page\.url\s*==\s*\'/\'\s*or\s+page\.url\s*==\s*\'\'\s*%\}\s*active\s*\{%\s*endif\s*%\}', 'active' if page_meta.get('url', '') == '/' else '', rendered)
    rendered = re.sub(r'\{%\s*if.*?%\}(.*?)\{%\s*endif\s*%\}', r'\1', rendered, flags=re.DOTALL)
    rendered = re.sub(r'\{%.*?%\}', '', rendered)
    rendered = re.sub(r'\{\{.*?\}\}', '', rendered)
    
    parent_layout = fm.get('layout')
    if parent_layout and parent_layout != layout_name:
        return render_layout(parent_layout, rendered, page_meta)
    
    return rendered

class JekyllPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_path = self.path.split('?')[0].rstrip('/')
        if not url_path:
            url_path = '/'
            
        posts = load_posts()
        
        # Static files (CSS, JS, images)
        if self.path.startswith('/css/') or self.path.endswith('.css') or self.path.endswith('.js') or self.path.endswith('.png') or self.path.endswith('.jpg'):
            rel_path = self.path.lstrip('/').split('?')[0]
            local_file = BASE_DIR / rel_path
            if local_file.exists():
                return super().do_GET()
                
        # Home Page
        if url_path == '/':
            index_file = BASE_DIR / 'index.html'
            raw = index_file.read_text(encoding='utf-8')
            fm, body = parse_frontmatter(raw)
            
            feed_html = ""
            for post in posts:
                tags_list = post.get('tags') or post.get('categories') or []
                if isinstance(tags_list, str):
                    tags_list = [tags_list]
                tags_html = "".join([f'<span class="tag-badge">#{t}</span>' for t in tags_list[:2]])
                tags_block = f'<span class="meta-separator">•</span><div class="post-tags">{tags_html}</div>' if tags_list else ''
                words = len(post['content'].split())
                rt = max(1, words // 200)
                excerpt = " ".join(re.sub(r'<[^>]+>', '', post['html_content']).split()[:32]) + "..."
                
                feed_html += f"""
                <article class="post-card">
                  <header class="post-card-header">
                    <h3 class="post-title"><a href="{post['url']}">{post['title']}</a></h3>
                    <div class="post-meta">
                      <span class="post-date">{post['date_formatted']}</span>
                      <span class="meta-separator">•</span>
                      <span>{rt} min read</span>
                      {tags_block}
                    </div>
                  </header>
                  <p class="post-excerpt">{excerpt}</p>
                  <div class="post-card-footer">
                    <a href="{post['url']}" class="read-more-link">
                      <span>Read full article</span>
                      <span class="arrow">&rarr;</span>
                    </a>
                  </div>
                </article>
                """
                
            content = body
            # Replace loop in index.html
            content = re.sub(r'\{%\s*for post in site\.posts\s*%\}.*?\{%\s*endfor\s*%\}', feed_html, content, flags=re.DOTALL)
            
            full_html = render_layout('default', content, {'title': fm.get('title', 'Vivek Soundararaj'), 'url': '/'})
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(full_html.encode('utf-8'))
            return
            
        # Journal / Blog list
        if url_path == '/blog':
            blog_file = BASE_DIR / 'blog' / 'index.html'
            raw = blog_file.read_text(encoding='utf-8')
            fm, body = parse_frontmatter(raw)
            
            feed_html = ""
            for post in posts:
                tags_list = post.get('tags') or post.get('categories') or []
                if isinstance(tags_list, str):
                    tags_list = [tags_list]
                tags_html = "".join([f'<span class="tag-badge">#{t}</span>' for t in tags_list])
                tags_block = f'<span class="meta-separator">•</span><div class="post-tags">{tags_html}</div>' if tags_list else ''
                words = len(post['content'].split())
                rt = max(1, words // 200)
                excerpt = " ".join(re.sub(r'<[^>]+>', '', post['html_content']).split()[:34]) + "..."
                
                feed_html += f"""
                <article class="post-card">
                  <header class="post-card-header">
                    <h3 class="post-title"><a href="{post['url']}">{post['title']}</a></h3>
                    <div class="post-meta">
                      <span class="post-date">{post['date_formatted']}</span>
                      <span class="meta-separator">•</span>
                      <span>{rt} min read</span>
                      {tags_block}
                    </div>
                  </header>
                  <p class="post-excerpt">{excerpt}</p>
                  <div class="post-card-footer">
                    <a href="{post['url']}" class="read-more-link">
                      <span>Read full article</span>
                      <span class="arrow">&rarr;</span>
                    </a>
                  </div>
                </article>
                """
                
            content = body
            content = re.sub(r'\{%\s*for post in site\.posts\s*%\}.*?\{%\s*endfor\s*%\}', feed_html, content, flags=re.DOTALL)
            full_html = render_layout('default', content, {'title': 'Journal & Writing · Vivek Soundararaj', 'url': '/blog'})
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(full_html.encode('utf-8'))
            return
            
        # Single Post: /blog/YYYY/MM/DD/slug
        for i, post in enumerate(posts):
            if url_path == post['url']:
                prev_post = posts[i+1] if i+1 < len(posts) else None
                next_post = posts[i-1] if i > 0 else None
                
                post_html = post['html_content']
                tags_chips = "".join([f'<span class="tag-badge">#{t}</span>' for t in (post['tags'] or post['categories'])])
                words = len(post['content'].split())
                rt = max(1, words // 200)
                
                nav_html = '<nav class="post-navigation">'
                if prev_post:
                    nav_html += f'<a href="{prev_post["url"]}" class="post-nav-card prev"><span class="post-nav-label">← Previous Article</span><span class="post-nav-title">{prev_post["title"]}</span></a>'
                else:
                    nav_html += '<div></div>'
                if next_post:
                    nav_html += f'<a href="{next_post["url"]}" class="post-nav-card next"><span class="post-nav-label">Next Article →</span><span class="post-nav-title">{next_post["title"]}</span></a>'
                nav_html += '</nav>'
                
                article_inner = f"""
                <article class="article-container">
                  <header class="article-header">
                    <a href="/blog" class="back-link">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                      Back to Journal
                    </a>
                    <h1 class="article-title">{post['title']}</h1>
                    <div class="article-meta">
                      <div class="meta-item">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                        <span>{post['date_formatted']}</span>
                      </div>
                      <span class="meta-dot">·</span>
                      <div class="meta-item">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        <span>{rt} min read</span>
                      </div>
                      <span class="meta-dot">·</span>
                      <div class="post-tags">{tags_chips}</div>
                    </div>
                  </header>
                  <div class="prose">{post_html}</div>
                  {nav_html}
                </article>
                """
                
                full_html = render_layout('default', article_inner, {'title': post['title'] + ' · Vivek Soundararaj', 'date_formatted': post['date_formatted'], 'url': post['url']})
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(full_html.encode('utf-8'))
                return
                
        # 404
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>404 Not Found</h1><p><a href='/'>Go Home</a></p>")

if __name__ == '__main__':
    import sys
    start_port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    port = start_port
    max_tries = 10
    httpd = None

    for i in range(max_tries):
        try:
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(("", port), JekyllPreviewHandler)
            break
        except OSError as e:
            if e.errno == 48:
                port += 1
            else:
                raise

    if httpd is None:
        print(f"Error: Could not bind to any port in range {start_port}-{start_port + max_tries - 1}.")
        sys.exit(1)

    with httpd:
        print(f"=====================================================")
        print(f"✨ Local Preview running at: http://localhost:{port}")
        print(f"Press Ctrl+C to stop the preview server.")
        print(f"=====================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nPreview server stopped.")
