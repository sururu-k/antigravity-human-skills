#!/usr/bin/env python3
import json
import base64
import os
import argparse

def get_b64(path):
    if path and os.path.exists(path):
        ext = os.path.splitext(path)[1].lower()
        mime = 'image/png' if ext == '.png' else 'image/jpeg'
        with open(path, 'rb') as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')
    return ""

def build_html(data):
    title = data.get("title", "プレゼンテーション")
    theme_color = data.get("theme_color", "#0072ba")
    slides_html = []

    for s in data.get("slides", []):
        stype = s.get("type", "split")
        
        if stype == "cover":
            img_src = get_b64(s.get("image", ""))
            img_tag = f'<img src="{img_src}">' if img_src else ''
            slides_html.append(f'''
      <section>
        <div class="cover-body">
          <div class="cover-content">
            <div>
              <div style="color: var(--corporate-blue); font-size: 18px; font-weight: bold; letter-spacing: 0.05em;">発表資料</div>
              <h1 class="cover-title">{s.get('title', '').replace(chr(10), '<br>')}</h1>
            </div>
            <div style="font-size: 22px; color: var(--text-main); font-weight: bold; border-top: 1px solid var(--border-gray); padding-top: 20px;">
              発表者：{s.get('author', '')}
            </div>
          </div>
          <div class="cover-media">
            {img_tag}
          </div>
        </div>
      </section>''')

        elif stype == "split":
            img_src = get_b64(s.get("image", ""))
            img_tag = f'<img src="{img_src}">' if img_src else ''
            items_html = ""
            for item in s.get("items", []):
                items_html += f'''
              <div class="content-heading">{item.get('heading', '')}</div>
              <div class="content-text">{item.get('text', '').replace(chr(10), '<br>')}</div>'''

            caption_html = f'<div class="simple-caption">{s.get("caption")}</div>' if s.get("caption") else ""
            slides_html.append(f'''
      <section>
        <div class="standard-header">
          <h2>{s.get('title', '')}</h2>
          <span class="header-meta">{s.get('meta', '')}</span>
        </div>
        <div class="slide-body">
          <div class="two-column">
            <div>{items_html}</div>
            <div>
              <div class="media-box">
                {img_tag}
              </div>
              {caption_html}
            </div>
          </div>
        </div>
      </section>''')

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/theme/white.min.css">
  <style>
    :root {{
      --corporate-blue: {theme_color};
      --text-main: #0f172a;
      --text-sub: #475569;
      --border-gray: #cbd5e1;
      --bg-white: #ffffff;
    }}
    body {{ background: #1e293b; margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", Meiryo, sans-serif; }}
    .reveal {{ background: var(--bg-white); }}
    .reveal .slides section {{ width: 100% !important; height: 100% !important; padding: 0 !important; display: flex !important; flex-direction: column !important; }}
    .standard-header {{ height: 100px; padding: 24px 60px 16px; border-bottom: 4px solid var(--corporate-blue); display: flex; justify-content: space-between; align-items: flex-end; background: #fff; }}
    .standard-header h2 {{ font-size: 34px !important; font-weight: bold !important; color: var(--text-main) !important; margin: 0 !important; }}
    .standard-header .header-meta {{ font-size: 17px; font-weight: bold; color: var(--corporate-blue); }}
    .slide-body {{ flex: 1; padding: 36px 60px 48px; background: #fff; }}
    .two-column {{ display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 40px; align-items: center; height: 440px; }}
    .content-heading {{ font-size: 24px; font-weight: bold; color: var(--text-main); margin-bottom: 10px; display: flex; align-items: center; }}
    .content-heading::before {{ content: "■"; color: var(--corporate-blue); margin-right: 12px; font-size: 18px; }}
    .content-text {{ font-size: 21px; line-height: 1.75; color: #1e293b; margin-bottom: 24px; padding-left: 30px; }}
    .media-box {{ width: 100%; height: 440px; border: 1px solid var(--border-gray); border-radius: 6px; overflow: hidden; background: #fff; }}
    .media-box img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .simple-caption {{ font-size: 13px; color: var(--text-sub); text-align: center; margin-top: 6px; }}
    .cover-body {{ height: 100%; padding: 60px; display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 50px; align-items: center; }}
    .cover-title {{ font-size: 42px !important; font-weight: bold !important; color: var(--text-main) !important; line-height: 1.35 !important; }}
    .cover-media {{ height: 480px; border: 1px solid var(--border-gray); border-radius: 6px; overflow: hidden; }}
    .cover-media img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">{''.join(slides_html)}</div>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.min.js"></script>
  <script>
    Reveal.initialize({{ width: 1280, height: 720, margin: 0, center: false, slideNumber: 'c/t', keyboard: true }});
  </script>
</body>
</html>'''
    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="slide.html")
    args = parser.parse_args()
    
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    out_html = build_html(cfg)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out_html)
    print(f"Generated clean standard slide at {args.output}")
