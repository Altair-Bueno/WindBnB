// I love ts...
import type { APIContext } from "astro";
import {
  BookingApi,
  Configuration,
  ResponseError,
} from "../../api/A2reservasREST";
import AppConfig from "../../config";
import cookies from "../../cookies";

export const URI = "/bookings/newHandler";

export const FormDataKeys = {
  houseId: "house_id",
  startDate: "start_date",
  endDate: "end_date",
};

/**
 * Creates a new booking
 */
export async function post(context: APIContext) {
  const referer = new URL(
    context.request.headers.get("referer") ?? context.url
  );

  const formData = await context.request.formData();
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
    houseId: formData.get(FormDataKeys.houseId)?.toString() ?? "",
    startDate: new Date(
      Date.parse(formData.get(FormDataKeys.startDate)?.toString() ?? "")
    ),
    endDate: new Date(
      Date.parse(formData.get(FormDataKeys.endDate)?.toString() ?? "")
    ),
    userId,
  };

  try {
    const response = await api.newBooking({ newBooking });
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
