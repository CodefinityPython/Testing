from lib.python_checkers.code_checker import CodeChecker


import io
import tokenize


class CodeBlockChecker(CodeChecker):
    def __init__(self, solution: str, user_code: str, hints=None):
        super().__init__(solution, user_code)
        self.hints = self.clear_hints(hints)

    @staticmethod
    def clear_hints(hints):
        cleared_hints_list = []
        for line in hints:
            hint = line.strip()
            if hint and hint[0] != '#':  # перевірка на не пустий рядок та перший символ не "#"
                cleared_hints_list.append(hint)
        return cleared_hints_list

    def len_test(self):
        if len(self.user_lines) != len(self.solution_lines):
            return ['Your code does not meet the task requirements.\n' \
                   f'Solution lines length: {len(self.solution_lines)}\n' \
                   f'Your code lines length: {len(self.user_lines)}']

    def is_different(self):
        messages = []
        if not self.len_test():
            for i in range(len(self.user_text)):
                if '___' in self.user_text[i]:
                    messages.append(f"Fill in all '___' gaps in code. An error was found in the line '{self.hints[i]}'")

                elif self.user_text[i] != self.solution_text[i]:
                    messages.append(f"Line {i}: Expected '{self.solution_lines[i]}', but got '{self.hints[i]}'")

            if messages:
                return messages
        else:
            return self.len_test()


class ErrorChecker:
    def __init__(self, code):
        self.code = code

    def remove_comments(self):
        lines = io.StringIO(self.code).readlines()
        in_comment = False
        cleaned_lines = []

        for line in lines:
            if in_comment:
                if line.strip().endswith("'''") or line.strip().endswith('"""'):
                    in_comment = False
                continue

            if "'''" in line or '"""' in line:
                in_comment = True
                if not (line.strip().endswith("'''") or line.strip().endswith('"""')):
                    continue

            tokens = tokenize.generate_tokens(io.StringIO(line).readline)
            cleaned_line = ""

            for token in tokens:
                token_type = token[0]
                token_value = token[1]

                if token_type == tokenize.COMMENT:
                    break
                else:
                    cleaned_line += token_value

            cleaned_lines.append(cleaned_line)

        return ErrorChecker('\n'.join(cleaned_lines))

    def get_errors(self):
        try:
            compiled = compile(self.code, '<string>', 'exec')
            return
        except SyntaxError as e:
            error_message = f"Syntax Error: {e}"
            lines = self.code.split('\n')
            error_line_number = e.lineno
            if error_line_number <= len(lines):
                error_line = lines[error_line_number - 1]
                error_message += f"\nError in line: '{error_line}'"
            return [error_message]
        except Exception as e:
            return [f"Execution Error: {e}"]




