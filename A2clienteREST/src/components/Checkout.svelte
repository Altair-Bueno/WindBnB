<script lang="ts">
  import type {
    CreateOrderActions,
    CreateOrderData,
    OnApproveActions,
    OnApproveData,
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
    const fromTimestamp = Date.parse(from);
    const toTimestamp = Date.parse(to);

    const response = await fetch(URI, {
      method: "POST",
      body: JSON.stringify({
        houseId: vivienda.id,
        startDate: new Date(fromTimestamp),
        endDate: new Date(toTimestamp),
      }),
    });
    console.log(response);
    if (!response.ok) {
      throw new Error("Create order error");
    }

    const days = Math.abs(
      (fromTimestamp - toTimestamp) / (1000 * 60 * 60 * 24)
    );
    const value = vivienda.price * days;
    return await actions.order.create({
      purchase_units: [
        {
          amount: {
            value: value.toString(),
          },
        },
      ],
    });
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
      console.log(response);
      if (!response.ok) {
        throw new Error("Create order error");
      }
    });
  }
</script>

<form>
  {#if msg}
    {msg}
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
  {#if from && to}
    <PaypalButton {paypalClientId} {createOrder} {onApprove} />
  {/if}
</form>
