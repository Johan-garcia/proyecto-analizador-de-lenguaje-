class LexicalAnalyzer:
    def __init__(self):
        # Palabras clave del lenguaje
        self.keywords = {
            "False", "class", "finally", "is", "return",
            "None", "continue", "for", "lambda", "try",
            "True", "def", "from", "nonlocal", "while",
            "and", "del", "global", "not", "with",
            "as", "elif", "if", "or", "yield",
            "assert", "else", "import", "pass",
            "break", "except", "in", "raise", "print"
        }
        # Operadores y sus tokens
        self.operators = {
            "=": "tk_asig", "==": "tk_igual", "!=": "tk_distinto",
            "<": "tk_menor", "<=": "tk_menor_igual", ">": "tk_mayor", ">=": "tk_mayor_igual",
            "+": "tk_suma", "-": "tk_resta", "*": "tk_mult", "/": "tk_div", "%": "tk_mod",
            "(": "tk_par_izq", ")": "tk_par_der", "{": "tk_llave_izq", "}": "tk_llave_der",
            "[": "tk_corchete_izq", "]": "tk_corchete_der", ".": "tk_punto", ",": "tk_coma",
            ":": "tk_dos_puntos", ";": "tk_punto_coma", "~": "tk_neg", "^": "tk_pot",
            "&": "tk_and", "|": "tk_or"
        }
        # Pila para manejar la indentación
        self.indent_stack = [0]
        self.expected_indent = False

    def is_identifier_char(self, char):
        # Verifica si el carácter es válido en un identificador
        return char.isalnum() or char == "_"

    def analyze(self, input_code):
        tokens = []
        state = "start"
        current_token = ""
        line = 0
        column = 1
        idx = 0
        current_indent = 0

        while idx < len(input_code):
            char = input_code[idx]

            # Estado inicial
            if state == "start":
                if char == " " or char == "\t":
                    # Calcula la indentación en función del tipo de espacio
                    current_indent += 1 if char == " " else 4
                    idx += 1
                    column += 1
                elif char == "\n":
                    # Resetea la indentación al comenzar una nueva línea
                    current_indent = 0
                    line += 1
                    column = 1
                    idx += 1
                else:
                    # Manejo de la indentación
                    if self.expected_indent and current_indent <= self.indent_stack[-1]:
                        print(f">>> Error de indentación(linea:{line},posicion:{column})")
                        return None
                    self.expected_indent = False

                    if current_indent > self.indent_stack[-1]:
                        self.indent_stack.append(current_indent)
                        tokens.append(f"<INDENT,{line},{column}>")
                    elif current_indent < self.indent_stack[-1]:
                        while current_indent < self.indent_stack[-1]:
                            self.indent_stack.pop()
                            tokens.append(f"<DEDENT,{line},{column}>")
                        if current_indent != self.indent_stack[-1]:
                            print(f">>> Error de indentación(linea:{line},posicion:{column})")
                            return None
                    current_indent = 0
                    state = "processing"
                    continue

            # Procesamiento de caracteres
            if state == "processing":
                if char.isspace():
                    if char == "\n":
                        line += 1
                        column = 0
                        state = "start"
                    column += 1
                elif char.isalpha() or char == "_":
                    current_token += char
                    state = "identifier"
                elif char.isdigit():
                    current_token += char
                    state = "number"
                elif char in self.operators:
                    if current_token:
                        if current_token in self.keywords:
                            tokens.append(
                                f"<{current_token},{line},{column-len(current_token)}>")
                        else:
                            tokens.append(
                                f"<id,{current_token},{line},{column-len(current_token)}>")
                        current_token = ""
                    current_token += char
                    state = "operator"
                elif char in "\"'":
                    current_token += char
                    state = "string"
                    string_start_line = line
                    string_start_col = column
                elif char == "#":
                    state = "comment"
                else:
                    print(f">>> Error léxico(linea:{line},posicion:{column})")
                    return None
                idx += 1

            # Procesamiento de identificadores
            elif state == "identifier":
                if self.is_identifier_char(char):
                    current_token += char
                    idx += 1
                    column += 1
                else:
                    if current_token in self.keywords:
                        tokens.append(
                            f"<{current_token},{line},{column-len(current_token)}>")
                        if current_token in {"for", "if", "while", "def", "class", "elif", "else"}:
                            self.expected_indent = True
                    else:
                        tokens.append(
                            f"<id,{current_token},{line},{column-len(current_token)}>")
                    current_token = ""
                    state = "processing"

            # Procesamiento de números enteros
            elif state == "number":
                if char.isdigit():
                    current_token += char
                    idx += 1
                    column += 1
                elif char == ".":
                    current_token += char
                    state = "float"
                    idx += 1
                    column += 1
                else:
                    tokens.append(
                        f"<tk_entero,{current_token},{line},{column-len(current_token)}>")
                    current_token = ""
                    state = "processing"

            # Procesamiento de números flotantes
            elif state == "float":
                if char.isdigit():
                    current_token += char
                    idx += 1
                    column += 1
                elif char.isalpha():
                    print(f">>> Error léxico(linea:{line},posicion:{column})")
                    return None
                else:
                    tokens.append(
                        f"<tk_flotante,{current_token},{line},{column-len(current_token)}>")
                    current_token = ""
                    state = "processing"

            # Procesamiento de operadores
            elif state == "operator":
                if current_token + char in self.operators:
                    current_token += char
                    idx += 1
                    column += 1
                else:
                    tokens.append(
                        f"<{self.operators[current_token]},{line},{column-len(current_token)}>")
                    current_token = ""
                    state = "processing"

            # Procesamiento de cadenas de texto
            elif state == "string":
                current_token += char
                if char == current_token[0]:
                    tokens.append(
                        f"<tk_cadena,{current_token},{string_start_line},{string_start_col}>")
                    current_token = ""
                    state = "processing"
                idx += 1
                column += 1

            # Procesamiento de comentarios
            elif state == "comment":
                if char == "\n":
                    line += 1
                    column = 1
                    state = "start"
                idx += 1

        # Manejo de tokens finales y posibles errores
        if state == "identifier":
            if current_token in self.keywords:
                tokens.append(
                    f"<{current_token},{line},{column-len(current_token)}>")
            else:
                tokens.append(
                    f"<id,{current_token},{line},{column-len(current_token)}>")
        elif state == "number":
            tokens.append(
                f"<tk_entero,{current_token},{line},{column-len(current_token)}>")
        elif state == "float":
            if current_token[-1] == ".":
                print(f">>> Error léxico(linea:{line},posicion:{column})")
                return None
            tokens.append(
                f"<tk_flotante,{current_token},{line},{column-len(current_token)}>")
        elif state == "operator":
            tokens.append(
                f"<{self.operators[current_token]},{line},{column-len(current_token)}>")

        # Manejo de la indentación final
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(f"<DEDENT,{line},{column}>")

        return "\n".join(tokens)


# Lectura del archivo de entrada
with open('codigo_fuente.py', 'r') as file:
    input_code = file.read()

# Creación del archivo de salida
analyzer = LexicalAnalyzer()
output = analyzer.analyze(input_code)

if output:  # Si no hay errores, guarda el análisis en el archivo
    with open('output.txt', 'w') as output_file:
        output_file.write(output)

    

