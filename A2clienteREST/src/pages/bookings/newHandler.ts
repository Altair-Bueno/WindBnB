// I love ts...
import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
import AppConfig from "../../config";
import cookies from "../../cookies";
import { z } from "zod";

export const URI = "/bookings/newHandler";

function getUserId(context: APIContext) {
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;
  return z.coerce.string().parse(userId);
}

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
    const userId = await getUserId(context);
    const payload = await context.request
      .json()
      .then((x) => postScheme.parse(x));

    const config = new Configuration(AppConfig.reservas);
    const api = new BookingApi(config);

    const body = await api
      .newBookingRaw({
        newBooking: { ...payload, userId },
      })
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
    const userId = getUserId(context);
    const { paypalOrderId, bookingId } = putScheme.parse(payload);

    const config = new Configuration(AppConfig.reservas);
    const api = new BookingApi(config);

    const response = await api.updateBooking({
      bookingId,
      updateBooking: { paypalOrderId, userId },
    });
    return {
      body: JSON.stringify(response),
    };
  } catch (e: any) {
    throw new Error(e);
  }
}
