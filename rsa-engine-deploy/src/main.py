
import argparse
import json
from rsa import RAIZ, gerarChaves, criptografar, descriptografar

parser = argparse.ArgumentParser(description="Criptografia RSA")
subparse = parser.add_subparsers(dest="comando", required=True, help="Subcomandos disponíveis")

# Gerar Chaves
parser_gerarChaves = subparse.add_parser("gerarChaves", help="Gera a chave pública e a chave privada")
parser_gerarChaves.add_argument("primo1", type=int, help="Primeiro primo")
parser_gerarChaves.add_argument("primo2", type=int, help="Segundo primo")
parser_gerarChaves.add_argument("-e", "--expoente", type=int, help="Expoente", default=argparse.SUPPRESS)
parser_gerarChaves.add_argument("--sem-arquivos", action="store_true", help="Devolve o par de chaves no JSON da saída")

def tratar_gerar_chaves(args):
    kwargs = {k: v for k, v in vars(args).items() if k not in ("comando", "func")}

    try:
        resultado = gerarChaves(**kwargs, diretorio=RAIZ)
        print(json.dumps(resultado))
    except ValueError as e:
        parser.error(str(e))

parser_gerarChaves.set_defaults(func=tratar_gerar_chaves)


# Criptografar
parser_criptografar = subparse.add_parser("criptografar", help="Criptografa uma sentença")
parser_criptografar.add_argument("msg", type=str, help="Mensagem")
parser_criptografar.add_argument("-e", "--expoente", type=int, help="Expoente")
parser_criptografar.add_argument("-n", type=int, help="n da Chave Pública")
parser_criptografar.add_argument("--sem-arquivos", action="store_true", help="Usa a chave informada e devolve o texto no JSON da saída")

def tratar_criptografar(args):
    try:
        resultado = criptografar(args.msg, e=args.expoente, n=args.n, sem_arquivos=args.sem_arquivos)
        print(json.dumps(resultado))
    except (ValueError, KeyError, OSError) as e:
        parser.error(str(e))

parser_criptografar.set_defaults(func=tratar_criptografar)


# Descriptografar
parser_descriptografar = subparse.add_parser("descriptografar", help="Descriptografa uma sentença")
parser_descriptografar.add_argument("msg", type=str, nargs="?", help="Lista de números criptografados em JSON")
parser_descriptografar.add_argument("-d", "--expoente", type=int, help="Expoente da Chave Privada")
parser_descriptografar.add_argument("-n", type=int, help="n da Chave Privada")
parser_descriptografar.add_argument("--sem-arquivos", action="store_true", help="Usa a chave e o texto informados")

def tratar_descriptografar(args):
    texto = None

    if args.msg is not None:
        try:
            texto = json.loads(args.msg)
        except json.JSONDecodeError:
            parser.error("O texto deve ser uma lista JSON de números")

        if not isinstance(texto, list) or any(type(i) is not int for i in texto):
            parser.error("O texto deve ser uma lista de números inteiros")

    try:
        resultado = descriptografar(args.expoente, args.n, texto, sem_arquivos=args.sem_arquivos)
        print(json.dumps(resultado, ensure_ascii=False))
    except (ValueError, KeyError, FileNotFoundError) as e:
        parser.error(str(e))

parser_descriptografar.set_defaults(func=tratar_descriptografar)


args = parser.parse_args()
args.func(args)
