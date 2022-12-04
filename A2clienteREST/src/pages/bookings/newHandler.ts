// I love ts...
import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
import AppConfig from "../../config";
import cookies from "../../cookies";
import { CreateOrderRequestBody } from "@paypal/paypal-js";

export const URI = "/bookings/newHandler";

/**
 * Creates a new booking
 */
export async function post(context: APIContext) {
  const payload = await context.request.json();
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;

  if (!userId) {
    return { body: JSON.stringify({ error: "User is not logged in" }) };
  }

  const config = new Configuration(AppConfig.reservas);
  const api = new BookingApi(config);

  try {
    const response = await api.newBooking({
      newBooking: {
        userId,
        houseId: payload.houseId,
        startDate: new Date(Date.parse(payload.startDate)),
        endDate: new Date(Date.parse(payload.endDate)),
      },
    });
    const body: CreateOrderRequestBody = {
      purchase_units: response.purchaseUnits,
    };
    return {
      body: JSON.stringify(body),
    };
  } catch (e: any) {
    const error = await e.response.json().then((x: any) => x.detail);
    return { body: JSON.stringify({ error }) };
  }
}

export async function put(context: APIContext) {
  const { paypalTransactionId, bookingId } = await context.request.json();
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;

  if (!userId) {
    return { body: JSON.stringify({ error: "User is not logged in" }) };
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
  } catch (e: any) {
    const error = await e.response.json().then((x: any) => x.detail);
    return { body: JSON.stringify({ error }) };
  }
}
