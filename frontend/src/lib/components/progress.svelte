<script lang="ts">
  import RiCheckFill from "svelte-remixicon/RiCheckFill.svelte";
  import RiGiftFill from "svelte-remixicon/RiGiftFill.svelte";
  import RiShoppingBasket2Line from "svelte-remixicon/RiShoppingBasket2Line.svelte";

  let { target, current }: { target: number; current: number } = $props();
</script>

<div class="flex">
  {#each { length: target! + 1 } as _, i}
    {@const isTarget = i == target!}
    {@const wasReached =
      i < current! % target! ||
      (isTarget && !!current && current % target === 0)}
    <div
      class="size-12 rounded-full bg-white not-first:-ml-3 border-2 border-neutral-100 flex items-center justify-center
      data-[target=true]:border-purple-500 data-[target=true]:data-[reached=true]:bg-purple-500 data-[target=true]:data-[reached=true]:text-white"
      data-target={isTarget}
      data-reached={wasReached}
    >
      {#if isTarget}
        <RiGiftFill />
      {:else if wasReached}
        <RiCheckFill />
      {:else}
        <RiShoppingBasket2Line />
      {/if}
    </div>
  {/each}
</div>
