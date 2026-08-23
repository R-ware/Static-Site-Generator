block = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
code_parts = block.split("```")
stripped_code_parts = code_parts[1].lstrip("\n")
print(stripped_code_parts)