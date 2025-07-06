import re
import sys
import os

def parse_junk(code):
    lines = code.strip().split('\n')
    parsedLines = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('hungry'):
            i += 1
            continue

        if line.startswith('order'):
            varval = line[len('order '):]
            if '=' not in varval:
                raise SyntaxError(f"Missing '=' in order statement: {line}")

            name = varval.split('=')[0].strip()
            value = varval.split('=')[1].strip()

            if value.startswith('eat'):
                expr = value[len('eat '):].strip()
                parsedLines.append({
                    'type': 'eat',
                    'name': name,
                    'expression': expr
                })
            else:
                parsedLines.append({
                    'type': 'order',
                    'name': name,
                    'value': value
                })

        elif line.startswith('whisper '):
            rest = line[len('whisper '):].strip()
            parsedLines.append({
                'type': 'print',
                'message': rest
            })

        elif line.startswith('reheat: '):
            func_name = line[len('reheat: '):].strip()
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != 'done':
                body.append(lines[i].strip())
                i += 1
            parsedLines.append({
                'type': 'function',
                'name': func_name,
                'body': body
            })

        elif line.startswith('barf(') and line.endswith(')'):
            msg = line[len('barf('):-1].strip()
            if msg.startswith('"') and msg.endswith('"'):
                parsedLines.append({
                    'type': 'barf',
                    'message': msg[1:-1]
                })

        elif line.startswith('open your mouth and say '):
            var_name = line[len('open your mouth and say '):].strip()
            if not var_name.isidentifier():
                raise SyntaxError(f"Invalid variable name: {var_name}")
            parsedLines.append({
                'type': 'input',
                'name': var_name,
            })

        elif line.startswith('if you like ') and ':' in line:
            condition = line[len('if you like '):].split(':')[0].strip()
            if_body = []
            else_body = []
            i += 1
            else_found = False
            while i < len(lines):
                current_line = lines[i].strip()
                if current_line == 'done':
                    break
                elif current_line == 'else:':
                    else_found = True
                else:
                    if else_found:
                        else_body.append(current_line)
                    else:
                        if_body.append(current_line)
                i += 1
            parsedLines.append({
                'type': 'if',
                'condition': condition,
                'if_body': if_body,
                'else_body': else_body
            })

        elif line.startswith('until thirsty ') and ':' in line:
            condition_part = line[len('until thirsty '):].split(':')[0].strip()
            loop_body = []
            i += 1
            while i < len(lines) and lines[i].strip() != 'done':
                loop_body.append(lines[i].strip())
                i += 1
            parsedLines.append({
                'type': 'loop',
                'condition': condition_part,
                'body': loop_body
            })

        else:
            raise SyntaxError(f"message must be written in double quotes: {line}")

        i += 1
    return parsedLines

def resolve(token, variables):
    if token.isdigit():
        return int(token)
    elif token in variables:
        return variables[token]
    else:
        raise ValueError(f"Unknown variable or value: {token}")

def evaluate_expression(expr, variables):
    tokens = re.findall(r'\w+|[+\-*/]', expr)
    if not tokens:
        raise SyntaxError(f"Empty expression: {expr}")

    total = resolve(tokens[0], variables)
    i = 1
    while i < len(tokens) - 1:
        op = tokens[i]
        next_val = resolve(tokens[i + 1], variables)
        if op == '+': total += next_val
        elif op == '-': total -= next_val
        elif op == '*': total *= next_val
        elif op == '/':
            if next_val == 0:
                raise ZeroDivisionError("Division by zero in expression.")
            total /= next_val
        else:
            raise ValueError(f"Unknown operator: {op}")
        i += 2
    return total

def execute(parsedLines, variables, functions):
    for types in parsedLines:
        if types['type'] == 'order':
            val = types['value']
            if val.startswith('deliver(') and val.endswith(')'):
                func_called = val[len('deliver('):-1].strip()
                if func_called in functions:
                    body_lines = parse_junk('\n'.join(functions[func_called]))
                    execute(body_lines, variables, functions)
                    if variables:
                        last_var = list(variables.keys())[-1]
                        variables[types['name']] = variables[last_var]
                    else:
                        raise ValueError(f"Function {func_called} did not return a value.")
                else:
                    raise NameError(f"Function {func_called} not defined.")
            elif val.isdigit():
                variables[types['name']] = int(val)
            else:
                variables[types['name']] = val

        elif types['type'] == 'eat':
            result = evaluate_expression(types['expression'], variables)
            variables[types['name']] = result

        elif types['type'] == 'print':
            msg = types['message']
            if '+' in msg:
                parts = [p.strip() for p in msg.split('+')]
                result = ''
                for part in parts:
                    if part.startswith('"') and part.endswith('"'):
                        result += part[1:-1]
                    elif part in variables:
                        result += str(variables[part])
                    else:
                        raise ValueError(f"Unknown part in whisper: {part}")
                print(result)
            elif msg.startswith('"') and msg.endswith('"'):
                print(msg[1:-1])
            elif msg in variables:
                print(variables[msg])
            else:
                raise ValueError(f"Unknown message to whisper: {msg}")

        elif types['type'] == 'input':
            user_inp = input(f"{types['name']}: ")
            if user_inp.isdigit():
                variables[types['name']] = int(user_inp)
            else:
                variables[types['name']] = user_inp

        elif types['type'] == 'barf':
            raise RuntimeError(f"barfed: {types['message']}")

        elif types['type'] == 'if':
            cond = types['condition']
            if ' more than ' in cond:
                a, b = cond.split(' more than ')
                op = '>'
            elif ' less than ' in cond:
                a, b = cond.split(' less than ')
                op = '<'
            elif ' equal to ' in cond:
                a, b = cond.split(' equal to ')
                op = '=='
            else:
                raise SyntaxError(f"Invalid condition: {cond}")

            a_val = resolve(a.strip(), variables)
            b_val = resolve(b.strip(), variables)

            condition_true = (
                (op == '>' and a_val > b_val) or
                (op == '<' and a_val < b_val) or
                (op == '==' and a_val == b_val)
            )

            body_to_run = types['if_body'] if condition_true else types['else_body']
            sublines = parse_junk('\n'.join(body_to_run))
            execute(sublines, variables, functions)

        elif types['type'] == 'loop':
            cond = types['condition']
            if '<' in cond:
                a, b = cond.split('<')
                op = '<'
            elif '>' in cond:
                a, b = cond.split('>')
                op = '>'
            elif '==' in cond:
                a, b = cond.split('==')
                op = '=='
            else:
                raise SyntaxError(f"Unknown loop condition: {cond}")

            a = a.strip()
            b = b.strip()

            def condition_met():
                a_val = resolve(a, variables)
                b_val = resolve(b, variables)
                return (
                    (op == '<' and a_val < b_val) or
                    (op == '>' and a_val > b_val) or
                    (op == '==' and a_val == b_val)
                )

            while condition_met():
                sublines = parse_junk('\n'.join(types['body']))
                execute(sublines, variables, functions)

def run_junk(code):
    parsedLines = parse_junk(code)
    variables = {}
    functions = {t['name']: t['body'] for t in parsedLines if t['type'] == 'function'}
    execute(parsedLines, variables, functions)

def run_junk_code(code: str) -> str:
    from io import StringIO
    import sys

    original_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        run_junk(code)
    except Exception as e:
        print(f"Error: {e}")

    sys.stdout = original_stdout
    return mystdout.getvalue()
