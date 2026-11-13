import { Router } from "express";
import { rsaRouter } from "./modules/rsa/rsa.routes.js";

export const router = Router();
router.use(rsaRouter);
