// I love ts...
import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
import { getAccessToken } from "../../utils/auth0";
import { z } from "zod";

export const URI = "/bookings/newHandler";

const postScheme = z.object({
  houseId: z.coerce.string(),
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
});

/**
 * Creates a new booking
 */
export async function post(context: APIContext) {
  try {
    const payload = await context.request
      .json()
      .then((x) => postScheme.parse(x));

    const config = new Configuration({
      basePath: import.meta.env.RESERVAS_BASE_PATH,
      accessToken: () => getAccessToken(context),
    });
    const api = new BookingApi(config);

    const body = await api
      .newBookingRaw({ newBooking: payload })
      .then((x) => x.raw.text());
    return { body };
  } catch (e: any) {
    throw new Error(e);
  }
}

const putScheme = z.object({
  paypalOrderId: z.coerce.string(),
  bookingId: z.coerce.string(),
});

export async function put(context: APIContext) {
  try {
    const payload = await context.request.json();
    const { paypalOrderId, bookingId } = putScheme.parse(payload);

    const config = new Configuration({
      basePath: import.meta.env.RESERVAS_BASE_PATH,
      accessToken: () => getAccessToken(context),
    });
    const api = new BookingApi(config);

    const response = await api.captureBookingPayment({
      bookingId,
      orderId: paypalOrderId,
    });
    return {
      body: JSON.stringify(response),
    };
  } catch (e: any) {
    throw new Error(e);
  }
}
