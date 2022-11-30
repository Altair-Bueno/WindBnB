<script lang="ts">
  import type {
    CreateOrderActions,
    CreateOrderData,
    OnApproveActions,
    OnApproveData,
  } from "@paypal/paypal-js";
  import type { Vivienda } from "../api/A2viviendasREST";
  import PaypalButton from "./PaypalButton.svelte";

  export let vivienda: Vivienda;
  export let paypalClientId: string;
  let from: string;
  let to: string;
  let msg: string | undefined;

  async function createOrder(
    data: CreateOrderData,
    actions: CreateOrderActions
  ) {
    const days = Math.abs(
      (Date.parse(from) - Date.parse(to)) / (1000 * 60 * 60 * 24)
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
    return await actions.order?.capture().then((orderData) => {
      console.log(orderData);
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
