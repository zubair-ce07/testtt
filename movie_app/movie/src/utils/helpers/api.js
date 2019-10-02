import axios from "axios";
import { requestTypes } from "../constants";

export function apiCaller({
  method = requestTypes.GET,
  url = "",
  params = {},
  data = {}
}) {
  return axios({
    method,
    url,
    params,
    data,
    headers: {
      "Content-Type": "application/json"
    },
    responseType: "json"
  });
}
