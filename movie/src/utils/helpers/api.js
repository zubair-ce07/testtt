import axios from "axios";
import { requestTypes } from "../constants";

export async function apiCaller({
  method = requestTypes.GET,
  url = "",
  params = {},
  data = {}
}) {
  try {
    const { data: resp } = await axios({
      method,
      url,
      params,
      data,
      headers: {
        "Content-Type": "application/json"
      },
      responseType: "json"
    });
    return resp;
  } catch (error) {
    throw error;
  }
}
