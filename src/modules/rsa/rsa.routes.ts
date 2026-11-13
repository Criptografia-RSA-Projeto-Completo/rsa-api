import { Router, type RequestHandler } from "express";
import { AppError } from "../../errors/AppError.js";
import { criptografar, descriptografar, gerarChaves } from "./rsa.controller.js";

export const rsaRouter = Router();
const methodNotAllowed: RequestHandler = (_request, response, next) => {
  response.set("Allow", "POST");
  next(new AppError(405, "Use POST."));
};

rsaRouter.route("/chaves").post(gerarChaves).all(methodNotAllowed);
rsaRouter.route("/criptografar").post(criptografar).all(methodNotAllowed);
rsaRouter.route("/descriptografar").post(descriptografar).all(methodNotAllowed);
