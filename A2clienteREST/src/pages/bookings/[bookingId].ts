import type { APIContext } from "astro";
import {
  BookingApi,
  Configuration,
  ResponseError,
} from "../../api/A2reservasREST";
import { getAccessToken } from "../../utils/auth0";
import AppConfig from "../../config";

export function getUri(bookingId: string) {
  return `/bookings/${bookingId}`;
}

/**
 * Cancel a Booking
 */
export async function post(context: APIContext) {
  const { bookingId } = context.params as { bookingId: string };

  const referer = new URL(
    context.request.headers.get("referer") ?? context.url
  );

  const config = new Configuration({
    basePath: AppConfig.reservas.basePath,
    accessToken: () => getAccessToken(context),
  });
  const api = new BookingApi(config);

  try {
    const response = await api.cancelBooking({
      bookingId: bookingId.toString(),
    });
    referer.searchParams.set("info", response.message);
  } catch (e) {
    const error = e as ResponseError;
    const msg = await error.response.json().then((x) => x.detail);
    referer.searchParams.set("danger", msg);
  }

  return context.redirect(referer.toString());
}
