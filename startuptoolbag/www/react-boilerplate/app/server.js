import { Server, Model, Factory, Response } from "miragejs";
import faker from "faker";

export function makeServer({ environment = "development" } = {}) {
  let server = new Server({
    environment,

    routes() {
      this.post("/api/job", () => {
        return new Response(202, {}, {href: "/api/jobs/2130040", id: "2130040"})
        // fetch("/api/job", {method: "POST"})
      });
    },
  });

  return server;
}
