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

  let from: string;
  let to: string;
  let msg: string | undefined;

  async function createOrder(
    data: CreateOrderData,
    actions: CreateOrderActions
  ) {
    const createOrderRequest = await fetch(URI, {
      method: "POST",
      body: JSON.stringify({
        houseId: vivienda.id,
        startDate: from,
        endDate: to,
      }),
    }).then((x) => x.json());
    return await actions.order.create(createOrderRequest);
  }
  async function onApprove(data: OnApproveData, actions: OnApproveActions) {
    return await actions.order?.capture().then(async (orderData) => {
      const response = await fetch(URI, {
        method: "PUT",
        body: JSON.stringify({
          paypalTransactionId: orderData.id,
          bookingId: vivienda.id,
        }),
      });
      if (!response.ok) {
        msg = await response.json().then((x) => x.detail);
        throw new Error("Create order error");
      }
    });
  }
  async function onCancel(
    data: Record<string, any>,
    actions: OnCancelledActions
  ) {}
  async function onError(error: Record<string, any>) {
    console.log(error);
    if (!from || !to) {
      msg = "Missing from and/or to fields";
    }
  }
</script>

<form>
  {#if msg}
    <div class="alert alert-danger" role="alert">
      {msg}
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
