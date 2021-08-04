import { Server, Model, Factory, Response } from "miragejs";
import faker from "faker";

function ri(max){
  return Math.floor(Math.random() * max);
}

export function makeServer({ environment = "development" } = {}) {
  let server = new Server({
    environment,
    routes() {
      this.post("/api/job", () => {
        const jn = ri(1000);
        return new Response(202, {}, {href: `/api/jobs/${jn}`, id: `${jn}`})
        // fetch("/api/job", {method: "POST"})
      });

      //http://restalk-patterns.org/long-running-operation-polling.html
      this.get("/api/job", () => {
        const jn = ri(1000);
        return new Response(200, {}, [{id: `${jn}`, input:jn, isPrime:'False'},
          {id: `${jn+1}`, input:jn, isPrime:'False'},
          {id: `${jn+2}`, input:jn, isPrime:'False'}])
        // fetch("/api/job", {method: "POST"})
      });

      // this.get("/api/*/output", () => {
      //   return new Response(200, {}, {href: `/api/jobs/${jn}`, id: `${jn}`})
      //   // fetch("/api/job", {method: "POST"})
      // });

    },
  });

  return server;
}
