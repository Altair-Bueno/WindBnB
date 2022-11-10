import type { APIContext } from "astro";
import {
  BookingApi,
  Configuration,
  NewBooking,
} from "../../api/A2reservasREST";
import AppConfig from "../../config";

export async function post(context: APIContext) {
  // TODO payload
  // haha ts funny
  const newBooking: NewBooking = context.params as unknown as NewBooking;

  const config = new Configuration(AppConfig.reservas);
  const api = new BookingApi(config);

  const response = await api.newBooking({ newBooking });

  //   TODO check if the redirect is good
  return context.redirect(`/house/${response.houseId}`);
}
