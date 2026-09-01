from textnode import *
from source_copy import source_copy, generate_page, generate_pages_recursive

def main():
    source_copy("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")

if __name__ == "__main__":
    main()