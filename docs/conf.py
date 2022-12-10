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
release = '0.0.1-pre'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxemoji.sphinxemoji',
    'sphinx.ext.intersphinx',
    'pallets_sphinx_themes',
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    "link": "var(--peach)",
    "link_hover": "var(--peach)" 
}

#html_sidebars = {
#    '**': {
#        'globaltoc.html', 'searchbox.html'
#    }
#}