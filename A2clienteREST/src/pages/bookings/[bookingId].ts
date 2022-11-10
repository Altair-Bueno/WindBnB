import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
import AppConfig from "../../config";

export function getUri(bookingId: string) {
  return `/bookings/${bookingId}`;
}

/**
 * Cancel a Booking
 */
export async function post(context: APIContext) {
  const { bookingId } = context.params;

  if (!bookingId) {
    throw new Error("Invalid booking id");
  }

  const config = new Configuration(AppConfig.reservas);
  const api = new BookingApi(config);

  const response = await api.cancelBooking({ bookingId: bookingId.toString() });

  return context.redirect("/bookings");
}
