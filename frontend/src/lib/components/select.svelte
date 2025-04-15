<script lang="ts">
  import type { HTMLSelectAttributes } from "svelte/elements";

  let {
    children,
    value = $bindable(),
    ...props
  }: Omit<HTMLSelectAttributes, "class"> = $props();
</script>

<select
  class="p-4 border border-neutral-100 rounded-xl placeholder-neutral-500 outline-none font-medium"
  bind:value
  {...props}
>
  {#if children}
    {@render children()}
  {/if}
</select>
