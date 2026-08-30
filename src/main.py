from textnode import *
from source_copy import source_copy, generate_page

def main():
    source_copy("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()