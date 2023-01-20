# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
sys.path.append('../src/chafa')

project = 'chafa.py'
copyright = '2022, Erica Ferrua Edwardsdóttir'
author = 'Erica Ferrua Edwardsdóttir'
release = '1.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxemoji.sphinxemoji',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx_toolbox.sidebar_links',
    'sphinx_toolbox.github',
    'sphinx.ext.autosummary',
    'sphinxcontrib.prettyspecialmethods'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    "link": "var(--links)",
    "link_hover": "var(--links)", 
    "body_text": "var(--fg)",
    "sidebar_link": "var(--fg)",

    "head_font_family": "Eczar",
    "font_family": "Signika Negative",
    "code_font_family": "JetBrains Mono",

    "description": "Version " + release
}

pygments_style = "dracula"

html_js_files = [
    'table.js'
]

github_username = "GuardKenzie"
github_repository = "chafa.py"

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}