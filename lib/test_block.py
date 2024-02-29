# Імпортуємо необхідні модулі та функції з інших файлів
from lib.python_checkers.ipynb import IpynbCode
from lib.python_checkers.text_comparison import CodeBlockChecker, ErrorChecker
from lib.messages import success, error


def test(solution_file_path: str, user_code_file_path: str, index: int):
    solution_file = IpynbCode(solution_file_path)
    user_code_file = IpynbCode(user_code_file_path)

    solution = ErrorChecker(solution_file.code)
    user_code = ErrorChecker(user_code_file.code)

    if not user_code.get_errors():
        solution = solution.remove_comments()
        user_code = user_code.remove_comments()

        code1 = '\n'.join(solution_file.code_blocks[:index+1])
        code2 = '\n'.join(solution_file.code_blocks[0:index-1] + user_code_file.code_blocks[index-1:index+1])
        code1 = ErrorChecker(code1).remove_comments()
        code2 = ErrorChecker(code2).remove_comments()

        test = CodeBlockChecker(code1.code, code2.code)

        if test.is_different():
            print(error(error_descriptions=test.is_different()))
        else:
            print(success())

    else:
        print(error(error_descriptions=user_code.get_errors()))




