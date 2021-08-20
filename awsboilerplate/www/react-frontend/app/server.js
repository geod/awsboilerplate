import { Server, Model, Factory, Response } from "miragejs";
import faker from "faker";

function ri(max){
  return Math.floor(Math.random() * max);
}

//export function makeServer({ environment = "development" } = {}) {
//  let server = new Server({
//    environment,
//    routes() {
//      this.urlPrefix = "https://api.localhost"
//
//      this.get("/prod/hello", (schema, request) => {
//        return new Response(202, {}, {message: "Hello " + request.queryParams.to})
//      })
//
//      this.post("/prod/job", () => {
//        const jn = ri(1000);
//        return new Response(202, {}, {href: `/api/jobs/${jn}`, id: `${jn}`})
//      })
//
//      //http://restalk-patterns.org/long-running-operation-polling.html
//      this.get("/prod/job", () => {
//        const jn = ri(1000);
//        return new Response(200, {}, [{id: `${jn}`, input:jn, isPrime:'False'}])
//        // fetch("/api/job", {method: "POST"})
//      })
//    },
//  });
//
//  return server;
//}
