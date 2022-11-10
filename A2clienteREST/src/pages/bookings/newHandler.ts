// I love ts...
import type { APIContext } from "astro";
import { BookingApi, Configuration } from "../../api/A2reservasREST";
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
  const formData = await context.request.formData();
  const userId = context.cookies.get(cookies.USER_ID_KEY).value;

  if (!userId) throw new Error("Missing userId cookie");

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
  const response = await api.newBooking({ newBooking });

  return context.redirect(`/houses/${response.houseId}`);
}
