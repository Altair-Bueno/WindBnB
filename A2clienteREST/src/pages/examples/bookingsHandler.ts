import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
import config from "../../config";

export async function get(context: APIContext) {
  const c = new Configuration(config.reservas);
  const api = new BookingApi(c);
  const response = await api.getBookings();

  console.log(response);

  return {
    body: JSON.stringify(response),
  };
}
