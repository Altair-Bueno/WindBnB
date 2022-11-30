// I love ts...
import type { APIContext } from "astro";
import {
  BookingApi,
  Configuration,
  NewBooking,
  ResponseError,
} from "../../api/A2reservasREST";
import AppConfig from "../../config";
import cookies from "../../cookies";

export const URI = "/bookings/newHandler";

/**
 * Creates a new booking
 */
export async function post(context: APIContext) {
  const referer = new URL(
    context.request.headers.get("referer") ?? context.url
  );

  const payload = await context.request.json();
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;

  if (!userId) {
    referer.searchParams.set("danger", "User isn't log in");
    return context.redirect(referer.toString());
  }

  const config = new Configuration(AppConfig.reservas);
  const api = new BookingApi(config);

  // TS is great...
  // At this point i'm not even mad at this code
  const newBooking = {
    houseId: payload.houseId,
    startDate: new Date(Date.parse(payload.startDate)),
    endDate: new Date(Date.parse(payload.endDate)),
    userId,
  };

  try {
    const response = await api.newBooking({ newBooking });
    return {
      body: JSON.stringify(response),
    };
  } catch (e) {
    const error = e as ResponseError;
    const msg = await error.response.json().then((x) => x.detail);
    referer.searchParams.set("danger", msg);
    return context.redirect(referer.toString());
  }
}

export async function put(context: APIContext) {
  const referer = new URL(
    context.request.headers.get("referer") ?? context.url
  );

  const { paypalTransactionId, bookingId } = (await context.request.json()) as {
    paypalTransactionId: string;
    bookingId: string;
  };
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;

  if (!userId) {
    referer.searchParams.set("danger", "User isn't log in");
    return context.redirect(referer.toString());
  }

  const config = new Configuration(AppConfig.reservas);
  const api = new BookingApi(config);

  try {
    const response = await api.updateBooking({
      bookingId,
      updateBooking: { paypalTransactionId, userId },
    });
    const params = new URLSearchParams();
    params.set("info", "Booked!");
    return context.redirect(`/houses/${response.houseId}?${params}`);
  } catch (e) {
    const error = e as ResponseError;
    const msg = await error.response.json().then((x) => x.detail);
    referer.searchParams.set("danger", msg);
    return context.redirect(referer.toString());
  }
}
