import { z } from "zod";

export const gerarChavesSchema = z.object({
  primo1: z.int().min(2),
  primo2: z.int().min(2),
  expoente: z.int().min(2).optional(),
}).refine(({ primo1, primo2 }) => Number.isSafeInteger(primo1 * primo2), {
  path: ["primo2"],
});

const chaveSchema = z.object({
  expoente: z.int().positive(),
  n: z.int().min(2),
});

export const criptografarSchema = chaveSchema.extend({
  mensagem: z.string().refine((mensagem) => !/[^A-Z ]/.test(mensagem)),
});

export const descriptografarSchema = chaveSchema.extend({
  texto: z.array(z.int().nonnegative()),
});
