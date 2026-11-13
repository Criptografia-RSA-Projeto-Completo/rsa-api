import json
from math_utils import mdcEstendido, ehPrimo, exponenciacaoModular
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

dicionario = {
    "A": 2,
    "B": 3,
    "C": 4,
    "D": 5,
    "E": 6,
    "F": 7,
    "G": 8,
    "H": 9,
    "I": 10,
    "J": 11,
    "K": 12,
    "L": 13,
    "M": 14,    
    "N": 15,
    "O": 16,
    "P": 17,
    "Q": 18,
    "R": 19,
    "S": 20,
    "T": 21,
    "U": 22,
    "V": 23,
    "W": 24,
    "X": 25,
    "Y": 26,
    "Z": 27,
    " ": 28
}

dicionario_invertido = {
    2: "A",
    3: "B",
    4: "C",
    5: "D",
    6: "E",
    7: "F",
    8: "G",
    9: "H",
    10: "I",
    11: "J",
    12: "K",
    13: "L",
    14: "M",
    15: "N",
    16: "O",
    17: "P",
    18: "Q",
    19: "R",
    20: "S",
    21: "T",
    22: "U",
    23: "V",
    24: "W",
    25: "X",
    26: "Y",
    27: "Z",
    28: " "
}

def gerarChaves(primo1, primo2, expoente=65537, *, diretorio=None, sem_arquivos=False):

    if primo1 == primo2:
         raise ValueError("Os valores informados são iguais. Os valores precisam ser números primos diferentes")

    if not ehPrimo(primo1) or not ehPrimo(primo2):
         raise ValueError(f"Um ou ambos os valores informados não são primos")

    n = primo1 * primo2
    phi = (primo1 - 1) * (primo2 - 1)

    if expoente <= 1 or expoente >= phi:
         raise ValueError(f"O expoente informado ({expoente}) não se encaixa na condição  1 < e < (p - 1) x (q - 1)")

    resultado = mdcEstendido(expoente, phi)
    
    if resultado["mdc"] == 1:
        d = resultado["coef1"]
        d = (d % phi + phi) % phi

        chaves = {
            "chavePublica": {"e": expoente, "n": n},
            "chavePrivada": {"d": d, "n": n},
        }
        if sem_arquivos:
            return chaves

        pasta = Path.cwd() if diretorio is None else Path(diretorio)
        with (pasta / "chaves.json").open("w") as arquivo:
            json.dump(chaves, arquivo, indent=4)

        return {"chavePublica": chaves["chavePublica"]}

    else:
         raise ValueError(f"O expoente informado ({expoente}) não é primo entre si de phi ({phi})")

def criptografar(palavra, e=None, n=None, *, sem_arquivos=False):
    if e is None or n is None:
        if sem_arquivos:
            raise ValueError("Informe -e e -n com --sem-arquivos")
        with (RAIZ / "chaves.json").open() as arquivo:
            chave = json.load(arquivo)["chavePublica"]
        if e is None:
            e = chave["e"]
        if n is None:
            n = chave["n"]

    if sem_arquivos and (e <= 0 or n <= 1):
        raise ValueError("O expoente deve ser positivo e o módulo deve ser maior que 1")

    texto_criptografado = []
    for caractere in palavra:
        if caractere not in dicionario:
            raise ValueError("A mensagem aceita apenas letras de A a Z e espaços")
        codigo = dicionario[caractere]
        if codigo >= n:
            raise ValueError("O módulo da chave é pequeno demais para a mensagem")
        texto_criptografado.append(exponenciacaoModular(codigo, e, n))

    if not sem_arquivos:
        with (RAIZ / "texto.json").open("w") as arquivo:
            json.dump({"textoCripto": {"texto": texto_criptografado}}, arquivo, indent=4)

    return {"texto": texto_criptografado}
            


def descriptografar(d=None, n=None, textoCripto=None, *, sem_arquivos=False):
    if sem_arquivos:
        if d is None or n is None or textoCripto is None:
            raise ValueError("Informe o texto criptografado, -d e -n com --sem-arquivos")
        if d <= 0 or n <= 1:
            raise ValueError("O expoente deve ser positivo e o módulo deve ser maior que 1")
        if any(not 0 <= numero < n for numero in textoCripto):
            raise ValueError("Cada número criptografado deve estar entre 0 e n - 1")

    if d is None or n is None:
        with (RAIZ / "chaves.json").open() as arquivo:
            dados_de_chaves = json.load(arquivo)

            if d is None:
                d = dados_de_chaves["chavePrivada"]["d"]

            if n is None:
                n = dados_de_chaves["chavePrivada"]["n"]

    if textoCripto is None:
        with (RAIZ / "texto.json").open() as arquivo:
            texto_Criptografado = json.load(arquivo)
            textoCripto = texto_Criptografado["textoCripto"]["texto"]

    listadescripto = []

    for numero in textoCripto:
        resultado = exponenciacaoModular(numero, d, n)
        listadescripto.append(resultado)

    texto = ""

    for i in listadescripto:
        if sem_arquivos and i not in dicionario_invertido:
            raise ValueError("O texto criptografado não corresponde à chave informada")
        texto = texto + dicionario_invertido[i]

    return {"texto": texto}
