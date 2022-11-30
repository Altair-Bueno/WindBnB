<script lang="ts">
  import {
    CreateOrderActions,
    CreateOrderData,
    loadScript,
    OnApproveActions,
    OnApproveData,
  } from "@paypal/paypal-js";

  export let paypalClientId: string;
  export let createOrder: (
    data: CreateOrderData,
    actions: CreateOrderActions
  ) => Promise<string>;
  export let onApprove: (
    data: OnApproveData,
    actions: OnApproveActions
  ) => Promise<void>;

  let paypalButtonContainer: HTMLElement;

  loadScript({ "client-id": paypalClientId }).then((paypal) => {
    if (paypal && paypal.Buttons) {
      paypal.Buttons({ createOrder, onApprove }).render(paypalButtonContainer);
    }
  });
</script>

<div id="paypal-button-container" bind:this={paypalButtonContainer} />
