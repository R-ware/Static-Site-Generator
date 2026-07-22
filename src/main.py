from textnode import *

def main():
    test_node = TextNode("this is a test", TextType.text_inline, "http://example.com")
    print(test_node)

if __name__ == "__main__":
    main()