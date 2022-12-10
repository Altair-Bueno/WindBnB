// I love ts...
import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
import AppConfig from "../../config";
import cookies from "../../cookies";
import { object, date, string } from "yup";

export const URI = "/bookings/newHandler";

function getUserId(context: APIContext) {
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;
  return string().required("User isn't logged in").validate(userId);
}

const postScheme = object({
  houseId: string().required(),
  startDate: date().required(),
  endDate: date().required(),
});

/**
 * Creates a new booking
 */
export async function post(context: APIContext) {
  try {
    const userId = await getUserId(context);
    const payload = await context.request
      .json()
      .then((x) => postScheme.validate(x));

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

const putScheme = object({
  paypalOrderId: string().required(),
  bookingId: string().required(),
});

export async function put(context: APIContext) {
  try {
    const payload = await context.request.json();
    const userId = await getUserId(context);
    const { paypalOrderId, bookingId } = await putScheme.validate(payload);

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
