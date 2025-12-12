#!/usr/bin/env python3
"""
Test Script for File Tools
Demonstrates file management capabilities.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.file_tools import FileTools


def main():
    print("=" * 70)
    print("🧪 File Tools Comprehensive Test")
    print("=" * 70)
    
    try:
        # Test 1: Get initial workspace info
        print("\n📍 Step 1: Workspace Information")
        info = FileTools.get_workspace_info()
        print(f"   Workspace Path: {info['workspace_path']}")
        print(f"   Files Present: {info['file_count']}")
        
        # Test 2: Save a Flask application file
        print("\n📍 Step 2: Saving Flask Application")
        app_code = '''"""
arXiv CS Daily - Flask Application
Main entry point for the web application.
"""

from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    """Home page with category navigation."""
    categories = ['cs.AI', 'cs.CV', 'cs.NLP', 'cs.LG']
    return render_template('index.html', categories=categories)

@app.route('/paper/<paper_id>')
def paper_detail(paper_id):
    """Detailed view of a specific paper."""
    return render_template('paper_detail.html', paper_id=paper_id)

@app.route('/api/papers/<category>')
def get_papers(category):
    """API endpoint to fetch papers by category."""
    # TODO: Fetch from arXiv API
    return jsonify({"category": category, "papers": []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
        FileTools.save_code("app.py", app_code)
        
        # Test 3: Save HTML templates
        print("\n📍 Step 3: Saving HTML Templates")
        
        base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}arXiv CS Daily{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <nav class="navbar">
            <h1>arXiv CS Daily</h1>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="#about">About</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2025 arXiv CS Daily. All rights reserved.</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
'''
        FileTools.save_code("templates/base.html", base_template)
        
        index_template = '''{% extends "base.html" %}

{% block content %}
<section class="hero">
    <h2>Daily Computer Science Papers from arXiv</h2>
    <p>Stay updated with the latest research</p>
</section>

<aside class="categories">
    <h3>Categories</h3>
    <ul>
        {% for category in categories %}
        <li><a href="#category-{{ category }}">{{ category }}</a></li>
        {% endfor %}
    </ul>
</aside>

<section class="papers">
    {% for category in categories %}
    <div id="category-{{ category }}" class="category-group">
        <h3>{{ category }}</h3>
        <div class="paper-list">
            <!-- Papers will be loaded here -->
        </div>
    </div>
    {% endfor %}
</section>
{% endblock %}
'''
        FileTools.save_code("templates/index.html", index_template)
        
        # Test 4: Save CSS stylesheet
        print("\n📍 Step 4: Saving CSS Stylesheet")
        css_code = '''/* arXiv CS Daily - Main Stylesheet */

:root {
    --primary-color: #2c3e50;
    --accent-color: #3498db;
    --text-color: #333;
    --bg-color: #ecf0f1;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--text-color);
    background-color: var(--bg-color);
}

header {
    background-color: var(--primary-color);
    color: white;
    padding: 1rem 0;
}

.navbar {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--accent-color);
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 2rem;
    padding: 0 2rem;
}

.hero {
    grid-column: 1 / -1;
    text-align: center;
    margin-bottom: 2rem;
}

.categories {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    height: fit-content;
}

.categories ul {
    list-style: none;
    margin-top: 1rem;
}

.categories li {
    margin: 0.5rem 0;
}

.categories a {
    color: var(--accent-color);
    text-decoration: none;
}

.papers {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
}

.category-group {
    margin-bottom: 2rem;
}

footer {
    background-color: var(--primary-color);
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 4rem;
}
'''
        FileTools.save_code("static/css/style.css", css_code)
        
        # Test 5: Save JavaScript file
        print("\n📍 Step 5: Saving JavaScript File")
        js_code = '''// arXiv CS Daily - JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    console.log('arXiv CS Daily loaded');
    loadPapers();
});

async function loadPapers() {
    const categories = ['cs.AI', 'cs.CV', 'cs.NLP', 'cs.LG'];
    
    for (const category of categories) {
        try {
            const response = await fetch(`/api/papers/${category}`);
            const data = await response.json();
            displayPapers(category, data.papers);
        } catch (error) {
            console.error(`Error loading papers for ${category}:`, error);
        }
    }
}

function displayPapers(category, papers) {
    const container = document.getElementById(`category-${category}`);
    if (!container) return;
    
    const paperList = container.querySelector('.paper-list');
    
    papers.forEach(paper => {
        const paperElement = createPaperElement(paper);
        paperList.appendChild(paperElement);
    });
}

function createPaperElement(paper) {
    const div = document.createElement('div');
    div.className = 'paper-item';
    div.innerHTML = `
        <h4><a href="/paper/${paper.id}">${paper.title}</a></h4>
        <p class="authors">${paper.authors}</p>
        <p class="summary">${paper.summary}</p>
        <div class="paper-actions">
            <a href="${paper.pdf_url}" target="_blank">View PDF</a>
            <button onclick="citePaper('${paper.id}')">Cite</button>
        </div>
    `;
    return div;
}

function citePaper(paperId) {
    console.log(`Citing paper: ${paperId}`);
    alert('Citation format will be shown here');
}
'''
        FileTools.save_code("static/js/script.js", js_code)
        
        # Test 6: Save configuration file
        print("\n📍 Step 6: Saving Configuration File")
        config_code = '''"""
Configuration for arXiv CS Daily Application
"""

import os
from datetime import datetime

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = FLASK_ENV == 'development'

# Database Configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///arxiv_papers.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# arXiv API Configuration
ARXIV_BASE_URL = 'http://export.arxiv.org/api/query'
ARXIV_CATEGORIES = ['cs.AI', 'cs.CV', 'cs.NLP', 'cs.LG']
PAPERS_PER_CATEGORY = 10

# Caching Configuration
CACHE_TIMEOUT = 3600  # 1 hour
LAST_UPDATE = datetime.now()
'''
        FileTools.save_code("arxiv_config.py", config_code)
        
        # Test 7: Save requirements.txt
        print("\n📍 Step 7: Saving Requirements File")
        requirements = '''flask==3.0.0
requests==2.31.0
sqlalchemy==2.0.0
arxiv==2.0.0
python-dotenv==1.0.0
gunicorn==21.0.0
'''
        FileTools.save_code("requirements.txt", requirements)
        
        # Test 8: List all saved files
        print("\n📍 Step 8: Listing All Saved Files")
        files = FileTools.list_files()
        print(f"   Total files: {len(files)}")
        print("\n   Files in workspace:")
        for file in sorted(files):
            file_size = Path(FileTools.WORKSPACE_DIR / file).stat().st_size
            print(f"      - {file:40s} ({file_size:6d} bytes)")
        
        # Test 9: Verify file contents
        print("\n📍 Step 9: Verifying Saved Content")
        app_content = FileTools.read_code("app.py")
        print(f"   app.py: {len(app_content)} characters, contains 'Flask': {('Flask' in app_content)}")
        
        # Test 10: Get final workspace info
        print("\n📍 Step 10: Final Workspace Status")
        final_info = FileTools.get_workspace_info()
        print(f"   Total files: {final_info['file_count']}")
        print(f"   Workspace ready for generation: ✓")
        
        print("\n" + "=" * 70)
        print("✅ File Tools Test PASSED!")
        print("=" * 70)
        print(f"\n📂 Generated project files are located at:")
        print(f"   {final_info['workspace_path']}")
        
    except Exception as e:
        print(f"\n❌ Test FAILED!")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
