# rsa-api

API REST didática em TypeScript que executa o rsa-engine-deploy pelo argparse com a opção `--sem-arquivos`. A cópia do motor em `rsa-engine-deploy/` permite publicar os dois a partir deste repositório.

## Rodar localmente

Com Node.js 24 e Python 3 no PATH, execute na raiz do projeto:

```powershell
npm ci
npm run dev
```

A API escuta em `http://127.0.0.1:3000`. As variáveis `HOST`, `PORT` e `PYTHON` podem substituir os valores padrão. Para checar e executar a versão compilada, use `npm run typecheck`, `npm run build` e `npm start`.

## Rotas

Envie os corpos com `Content-Type: application/json`.

| Método e rota | Exemplo de corpo | Resposta |
| --- | --- | --- |
| `POST /chaves` | `{"primo1":61,"primo2":53,"expoente":17}` | `{"chavePublica":{"e":17,"n":3233},"chavePrivada":{"d":2753,"n":3233}}` |
| `POST /criptografar` | `{"mensagem":"A","expoente":17,"n":3233}` | `{"texto":[1752]}` |
| `POST /descriptografar` | `{"texto":[1752],"expoente":2753,"n":3233}` | `{"texto":"A"}` |

Em `/chaves`, o expoente é opcional e o motor usa 65537 por padrão. Nos outros comandos, envie o expoente e o módulo da chave correspondente. O cliente guarda o par de chaves e o texto cifrado para reutilizá-los. A implementação é para demonstração com letras maiúsculas de A a Z e espaços.

## Contêiner e Vercel

Para testar com Docker a partir da raiz:

```powershell
docker build -f Dockerfile.vercel -t rsa-api .
docker run --rm -p 127.0.0.1:3000:3000 rsa-api
```

Na Vercel, importe o repositório da API com a raiz no diretório que contém `Dockerfile.vercel`. Configure a variável de ambiente `PORT=3000` no projeto, inclusive em Preview. Depois crie um deploy de prévia e teste as três rotas. O contêiner escuta em `0.0.0.0` e inclui o Python e o motor.
