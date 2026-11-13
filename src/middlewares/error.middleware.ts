import type { ErrorRequestHandler } from "express";
import { ZodError } from "zod";
import { AppError } from "../errors/AppError.js";

export const handleError: ErrorRequestHandler = (error: unknown, _request, response, next) => {
  if (response.headersSent) {
    next(error);
    return;
  }
  if (error instanceof AppError) {
    response.status(error.status).json({ erro: error.message });
    return;
  }
  if (error instanceof ZodError) {
    const detalhe = error.issues[0];
    const campo = detalhe?.path.join(".");
    response.status(400).json({
      erro: campo ? `Campo inválido: ${campo}.` : "Envie um objeto JSON válido.",
    });
    return;
  }
  if (error instanceof Error && "type" in error) {
    if (error.type === "entity.parse.failed") {
      response.status(400).json({ erro: "Envie um JSON válido." });
      return;
    }
    if (error.type === "entity.too.large") {
      response.status(413).json({ erro: "O corpo excede 16 KiB." });
      return;
    }
  }
  console.error(error);
  response.status(500).json({ erro: "Erro interno da API." });
};
