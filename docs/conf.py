import sys
import os

sys.path.insert(0, os.path.abspath("../"))

extensions = ["nbsphinx"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "restructuredtext",
    ".md": "markdown",
}
