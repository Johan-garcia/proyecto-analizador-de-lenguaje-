# proyecto-analizador-de-lenguaje-
Realizado por: Marco Duarte, Daniel Reyes, Johan Garcia, William Cordero


Este proyecto es un analizador léxico simple implementado en Python. El analizador procesa un fragmento de código fuente e identifica varios tipos de tokens como palabras clave, operadores, identificadores, números y más.

## Requisitos

- Python 3.x

## Instalación

Sigue estos pasos para descargar, instalar y ejecutar el proyecto en un sistema Linux.

### 1. Instalacion python

Para instalar python deberemos de ejecutar en la terminal:
```bash
sudo apt install python3-pip
```

### 2. Descargar y extraer el archivo ZIP

Primero, descarga el archivo ZIP del repositorio desde GitHub. Una vez descargado, extrae el contenido en un directorio de tu elección

### 3. Ejecucion del programa

-Para ejecutar el programa nos dirigimos a la carpeta en donde se extrajo el archivo .zip y en esta carpeta hacemos clic derecho y damos en la opcion "abrir en terminal" <br/> 
-para ejecutarlo solo necesitaremos poner esta linea de codigo: 

```bash
python3 AFD.py
```
### Funcionamiento del programa
-El programa contiene un ejemplo de analisis de codigo que es:

```bash
input_code = """
    cuadrado = lambda x, y: x + y
"""
```

-Resultado:

```bash
<def,2,1>
<id,hola,2,5>
<tk_par_izq,2,9>
<tk_par_der,2,10>
<tk_dos_puntos,2,11>
<INDENT,3,5>
<print,3,5>
<tk_par_izq,3,10>
<tk_entero,12,3,11>
<tk_par_der,3,13>
<DEDENT,4,1>

```

-Interpretación:

    <def,2,1>:
        Token: def
        Línea: 2
        Columna: 1
        Interpretación: Se encontró la palabra clave def en la línea 2, columna 1.

    <id,hola,2,5>:
        Token: id (identificador)
        Valor: hola
        Línea: 2
        Columna: 5
        Interpretación: Se encontró un identificador llamado hola en la línea 2, columna 5.

    <tk_par_izq,2,9>:
        Token: tk_par_izq (paréntesis izquierdo)
        Línea: 2
        Columna: 9
        Interpretación: Se encontró un paréntesis izquierdo ( en la línea 2, columna 9.

    <tk_par_der,2,10>:
        Token: tk_par_der (paréntesis derecho)
        Línea: 2
        Columna: 10
        Interpretación: Se encontró un paréntesis derecho ) en la línea 2, columna 10.

    <tk_dos_puntos,2,11>:
        Token: tk_dos_puntos (dos puntos)
        Línea: 2
        Columna: 11
        Interpretación: Se encontró un símbolo de dos puntos : en la línea 2, columna 11.

    <INDENT,3,5>:
        Token: INDENT (indentación)
        Línea: 3
        Columna: 5
        Interpretación: Se detectó un nivel de indentación (espacios en blanco al inicio de la línea) en la línea 3, columna 5. Esto indica que el bloque de código en la función hola ha comenzado.

    <print,3,5>:
        Token: print (función de impresión)
        Línea: 3cuadrado = lambda x, y: x + y
        Columna: 5
        Interpretación: Se encontró la palabra clave print en la línea 3, columna 5.

    <tk_par_izq,3,10>:
        Token: tk_par_izq (paréntesis izquierdo)
        Línea: 3
        Columna: 10
        Interpretación: Se encontró un paréntesis izquierdo ( en la línea 3, columna 10.

    <tk_entero,12,3,11>:
        Token: tk_entero (número entero)
        Valor: 12
        Línea: 3
        Columna: 11
        Interpretación: Se encontró un número entero 12 en la línea 3, columna 11.

    <tk_par_der,3,13>:
        Token: tk_par_der (paréntesis derecho)
        Línea: 3
        Columna: 13
        Interpretación: Se encontró un paréntesis derecho ) en la línea 3, columna 13.

    <DEDENT,4,1>:
        Token: DEDENT (fin de indentación)
        Línea: 4
        Columna: 1
        Interpretación: Se detectó una reducción en el nivel de indentación en la línea 4, indicando el fin del bloque de código.




