<script lang="ts">
  import type {
    CreateOrderActions,
    CreateOrderData,
    OnApproveActions,
    OnApproveData,
    OnCancelledActions,
  } from "@paypal/paypal-js";
  import type { Vivienda } from "../api/A2viviendasREST";
  import PaypalButton from "./PaypalButton.svelte";
  import { URI } from "../pages/bookings/newHandler";

  export let vivienda: Vivienda;
  export let paypalClientId: string;

  let bookingId = "";

  let from: string;
  let to: string;

  let danger: string | undefined;
  let info: string | undefined;

  async function createOrder(
    data: CreateOrderData,
    actions: CreateOrderActions
  ) {
    danger = undefined;
    info = undefined;
    const response = await fetch(URI, {
      method: "POST",
      body: JSON.stringify({
        houseId: vivienda.id,
        startDate: from,
        endDate: to,
      }),
    });
    const payload = await response.json();
    if (response.ok) {
      bookingId = payload.purchase_units[0].invoice_id;
      return await actions.order.create(payload);
    } else {
      throw new Error(payload);
    }
  }
  async function onApprove(data: OnApproveData, actions: OnApproveActions) {
    const response = await fetch(URI, {
      method: "PUT",
      body: JSON.stringify({
        bookingId,
        paypalOrderId: data.orderID,
      }),
    });
    const orderData = await response.json();
    if (response.ok) {
      info = "Booked sucessfully!";
    } else {
      throw new Error("Failed to verify order");
    }
  }
  async function onCancel(
    data: Record<string, any>,
    actions: OnCancelledActions
  ) {}
  async function onError(error: Record<string, any>) {
    console.log(error);
    if (!from || !to) {
      danger = "Missing from and/or to fields";
    } else {
      danger = "The house isn't available for that period";
    }
  }
</script>

<form>
  {#if danger}
    <div class="alert alert-danger" role="alert">
      {danger}
    </div>
  {/if}
  {#if info}
    <div class="alert alert-info" role="alert">
      {info}
    </div>
  {/if}
  <div class="mb-3">
    <label for="fromDateInput" class="form-label">From:</label>
    <input
      type="date"
      class="form-control"
      id="fromDateInput"
      aria-describedby="from date input"
      bind:value={from}
    />
  </div>
  <div class="mb-3">
    <label for="toDateInput" class="form-label">To:</label>
    <input
      type="date"
      class="form-control"
      id="toDateInput"
      aria-describedby="to date input"
      bind:value={to}
    />
  </div>
  <PaypalButton
    {paypalClientId}
    {createOrder}
    {onApprove}
    {onError}
    {onCancel}
  />
</form>
