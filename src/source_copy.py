import os
import shutil
from delimiter import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode
from pathlib import Path

def source_copy(static, public):
    if os.path.exists(static) == False:
        raise Exception("Static Folder Does Not Exist!")
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    static_dir = os.listdir(static)
    for files in static_dir:
        static_path = os.path.join(static, files)
        public_path = os.path.join(public, files)
        if os.path.isfile(static_path):
            print(static_path," -> ", public_path)
            shutil.copy(static_path, public_path)
        else:
            source_copy(static_path, public_path)

def extract_title(markdown):
    lines = markdown.strip().split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line .startswith("# "):
            title_text = stripped_line.split("#", 1)[1].strip()
            split_title_text = title_text.split()
            joined_title_text = " ".join(split_title_text)
            return joined_title_text
    else:
        raise Exception("There is no h1 header")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as f:
        file_contents = f.read()
    with open(template_path) as f:
        template_contents = f.read()
    converted_file_contents = markdown_to_html_node(file_contents)
    html_contents = converted_file_contents.to_html()
    title = extract_title(file_contents)
    titled_template = template_contents.replace("{{ Title }}", title)
    content_template = titled_template.replace("{{ Content }}", html_contents)
    basepath_template = content_template.replace('href="/', f'href="{basepath}')
    src_template = basepath_template.replace('src="/', f'src="{basepath}')
    path = os.path.dirname(dest_path)
    if os.path.exists(path) == False:
            os.makedirs(path)
    with open(dest_path, mode="w") as f:
        f.write(src_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_dir = os.listdir(dir_path_content)
    for file in content_dir:
        content_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(content_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(content_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)