<script>
  export let count = 0;
</script>

<button class="btn btn-primary" on:click={() => count++}>
  Click me: {count}
</button>
