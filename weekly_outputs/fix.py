def render_math_in_html(html_content: str,i) -> str:
    """
    Modifies an HTML string to correctly render LaTeX by converting all delimiters
    to the more web-safe dollar-sign format ($...$ and $$...$$) and
    configuring MathJax to recognize them.
    """
    # 1. Clean up non-breaking spaces.
    processed_html = html_content.replace(' ', ' ')

    # 2. Convert INLINE math \\( ... \\) to the standard $ ... $
    processed_html = processed_html.replace('\\\\(', '$')
    processed_html = processed_html.replace('\\\\)', '$')

    # 3. Convert DISPLAY math \\[ ... \\] and its variants to $$ ... $$
    # This handles the inconsistent delimiters like \\] found in the source file.
    processed_html = processed_html.replace('\\[', '$$')
    processed_html = processed_html.replace('\\\]', '$$')
    processed_html = processed_html.replace('\\]', '$$') # For any remaining cases

    # 4. Create a full HTML document with the necessary MathJax configuration.
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>week{i}</title>

    <script>
      MathJax = {{
        tex: {{
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
          displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        }}
      }};
    </script>
    
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.6;
            margin: 0 auto;
            max-width: 800px;
            padding: 2em;
        }}
        .mjx-display {{
            margin: 2.5em 0;
        }}
    </style>
</head>
<body>
    {processed_html}
</body>
</html>
"""
    return html_template

for i in range(1,13):
    with open(f'week_{i}.html', 'r', encoding='utf-8') as f:
        original_html = f.read()

    new_html = render_math_in_html(original_html,i)

    with open(f'week_{i}.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

