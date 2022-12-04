<script lang="ts">
  import {
    CreateOrderActions,
    CreateOrderData,
    loadScript,
    OnApproveActions,
    OnApproveData,
    OnCancelledActions,
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
  export let onError: undefined | ((error: Record<string, any>) => void) =
    undefined;
  export let onCancel:
    | undefined
    | ((data: Record<string, any>, actions: OnCancelledActions) => void) =
    undefined;

  let paypalButtonContainer: HTMLElement;

  loadScript({ "client-id": paypalClientId }).then((paypal) => {
    if (paypal && paypal.Buttons) {
      paypal
        .Buttons({ createOrder, onApprove, onError, onCancel })
        .render(paypalButtonContainer);
    }
  });
</script>

<div id="paypal-button-container" bind:this={paypalButtonContainer} />
