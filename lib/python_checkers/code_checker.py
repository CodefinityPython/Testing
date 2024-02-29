import re


class CodeChecker:
    def __init__(self, solution: str, user_code: str):
        self.solution = solution
        self.user_code = user_code
        self.solution_lines = self.clear(self.solution)
        self.user_lines = self.clear(self.user_code)
        self.solution_text = self.code_to_text(self.solution_lines)
        self.user_text = self.code_to_text(self.user_lines)

    @staticmethod
    def clear(code):
        code = code.split('\n')
        lines = [line for line in code if line != ""]
        return lines

    @staticmethod
    def code_to_text(code):
        text_lines = []
        for line in code:
            indent_match = re.match(r'^(\s+)', line)
            if indent_match:
                indent = indent_match.group(1)
            else:
                indent = ''
            stripped_line = re.sub(r'^\s+', '', line)
            text_lines.append(indent + stripped_line)
        return text_lines
