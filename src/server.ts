import type { AddressInfo } from "node:net";
import { app } from "./app.js";

const port = Number(process.env.PORT ?? 3000);
const host = process.env.HOST ?? "127.0.0.1";
const server = app.listen(port, host, () => {
  const address = server.address() as AddressInfo;
  console.log(`rsa-api em http://${host}:${address.port}`);
});
