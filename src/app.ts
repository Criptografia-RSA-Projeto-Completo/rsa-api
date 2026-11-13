import express from "express";
import { AppError } from "./errors/AppError.js";
import { handleError } from "./middlewares/error.middleware.js";
import { router } from "./routes.js";

export const app = express();

app.use(express.json({ limit: "16kb" }));
app.use(router);
app.use((_request, _response, next) => next(new AppError(404, "Rota inexistente.")));
app.use(handleError);
