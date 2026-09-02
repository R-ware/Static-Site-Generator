from textnode import *
from source_copy import source_copy, generate_page, generate_pages_recursive
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    source_copy("static/", "docs/")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

if __name__ == "__main__":
    main()