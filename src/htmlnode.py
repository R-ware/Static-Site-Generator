class HTMLNode:
    def __init__(self, tag: str, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else None
        self.props = props if props is not None else None

    def to_html(self) -> str:
        raise NotImplementedError("Not implemented.")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f" {props_str}"

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNode must have a value to convert to HTML.")
        if self.tag is None:
            return self.value
        elif self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"        
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"        

    def __repr__(self) -> str:
        return (
            f"LeafNode({self.tag!r}, value={self.value!r}, {self.props!r})"
        )

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML.")
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML.")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return (
            f"ParentNode({self.tag!r}, children={self.children!r}, {self.props!r})"
        )