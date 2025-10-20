import streamlit as st
import streamlit.components.v1 as components
import os

# ------------------------------------------------------------------
# 🧭 Streamlit Page Configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI Course Notes",
    layout="wide",
    page_icon="📘",
)

# ------------------------------------------------------------------
# 🎨 Custom CSS Styling (Light Theme)
# ------------------------------------------------------------------
custom_css = """
<style>
body {
    background-color: #f9fafc;
    color: #1a1a1a;
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.7;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}
h1, h2, h3 {
    color: #004aad;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 4px;
}
p, li {
    font-size: 1.05rem;
}
ul {
    margin-left: 1.5rem;
}
b {
    color: #00509e;
}
.mjx-display {
    margin: 2.5em 0;
}
code {
    background: #f3f3f3;
    padding: 3px 6px;
    border-radius: 5px;
}
</style>
"""

# ------------------------------------------------------------------
# 🧭 Sidebar Navigation
# ------------------------------------------------------------------
st.sidebar.title("📄 Lecture Navigation")

# Path where your HTML files are stored
PAGES_DIR = "weekly_outputs"

# Get all HTML files in the folder
html_pages = [f for f in os.listdir(PAGES_DIR) if f.endswith(".html")]
html_pages.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))

if not html_pages:
    st.error("No HTML files found in the 'pages' folder.")
    st.stop()

# Create page names without .html
page_names = [os.path.splitext(f)[0] for f in html_pages]

# Sidebar selector
selected_page = st.sidebar.radio("Go to:", page_names)

# ------------------------------------------------------------------
# 📄 Load and Display the Selected HTML Page
# ------------------------------------------------------------------
html_file_path = os.path.join(PAGES_DIR, f"{selected_page}.html")

with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Combine CSS with the HTML content
components.html(custom_css + html_content, height=1000, scrolling=True)

# ------------------------------------------------------------------
# 🧠 Optional Footer
# ------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ using Streamlit")
