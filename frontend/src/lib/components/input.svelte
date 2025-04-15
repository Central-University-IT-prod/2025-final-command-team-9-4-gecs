<script lang="ts">
  import type { HTMLInputAttributes } from "svelte/elements";

  let {
    class: className,
    value = $bindable(),
    ...props
  }: HTMLInputAttributes = $props();
</script>

<input
  class={`p-4 border border-neutral-100 rounded-xl placeholder-neutral-500 outline-none font-medium ${className ?? ""}`}
  bind:value
  {...props}
/>
