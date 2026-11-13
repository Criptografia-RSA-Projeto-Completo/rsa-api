import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import type { z } from "zod";
import { AppError } from "../../errors/AppError.js";
import type { criptografarSchema, descriptografarSchema, gerarChavesSchema } from "./rsa.schemas.js";

const exec = promisify(execFile);
const engine = fileURLToPath(new URL("../../../rsa-engine-deploy/src/main.py", import.meta.url));
const python = process.env.PYTHON ?? "python";

async function executar(comando: string, args: string[]): Promise<unknown> {
  let stdout: string;
  try {
    ({ stdout } = await exec(python, ["-B", "-X", "utf8", engine, comando, "--sem-arquivos", ...args], {
      encoding: "utf8",
      timeout: 5_000,
      windowsHide: true,
    }));
  } catch (error) {
    if (error instanceof Error && "killed" in error && error.killed) {
      throw new AppError(504, "O rsa-engine excedeu o tempo limite.");
    }
    if (error instanceof Error && "code" in error && error.code === 2 &&
        "stderr" in error && typeof error.stderr === "string") {
      const mensagem = error.stderr.match(/^.*?: error: (.+)$/m)?.[1];
      if (mensagem) throw new AppError(400, mensagem);
    }
    throw new AppError(502, "Falha ao executar o rsa-engine.");
  }

  try {
    return JSON.parse(stdout) as unknown;
  } catch {
    throw new AppError(502, "O rsa-engine devolveu uma resposta inválida.");
  }
}

export function gerarChaves({ primo1, primo2, expoente }: z.infer<typeof gerarChavesSchema>) {
  const args = [String(primo1), String(primo2)];
  if (expoente !== undefined) args.push("-e", String(expoente));
  return executar("gerarChaves", args);
}

export function criptografar({ mensagem, expoente, n }: z.infer<typeof criptografarSchema>) {
  return executar("criptografar", ["-e", String(expoente), "-n", String(n), "--", mensagem]);
}

export function descriptografar({ texto, expoente, n }: z.infer<typeof descriptografarSchema>) {
  return executar("descriptografar", ["-d", String(expoente), "-n", String(n), JSON.stringify(texto)]);
}
