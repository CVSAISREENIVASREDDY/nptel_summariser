HTML_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Title</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {
            font-family: "Product Sans", Arial, sans-serif;
            line-height: 1.6;
            margin: 0 auto;
            padding: 2rem 1rem;
            max-width: 800px;
            font-size: clamp(1rem, 2.5vw, 1.3rem); /* Fluid font sizing */
            box-sizing: border-box;
        }
        h1 {
            text-align: center;
        }
        h2 {
            margin-top: 30px;
        }
        .chapter {
            text-align: justify;
        }
    </style>
</head>
<body>
"""

HTML_FOOT = """
</body>
</html>
"""