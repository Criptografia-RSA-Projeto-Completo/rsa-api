import type { RequestHandler } from "express";
import { criptografarSchema, descriptografarSchema, gerarChavesSchema } from "./rsa.schemas.js";
import * as rsaService from "./rsa.service.js";

export const gerarChaves: RequestHandler = async (request, response) => {
  const dados = gerarChavesSchema.parse(request.body);
  response.set("Cache-Control", "no-store").status(201).json(await rsaService.gerarChaves(dados));
};

export const criptografar: RequestHandler = async (request, response) => {
  const dados = criptografarSchema.parse(request.body);
  response.set("Cache-Control", "no-store").json(await rsaService.criptografar(dados));
};

export const descriptografar: RequestHandler = async (request, response) => {
  const dados = descriptografarSchema.parse(request.body);
  response.set("Cache-Control", "no-store").json(await rsaService.descriptografar(dados));
};
