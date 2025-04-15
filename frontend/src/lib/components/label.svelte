<script lang="ts">
  import type { Snippet } from "svelte";

  let { text, children }: { text: string; children: Snippet } = $props();
</script>

<label class="flex flex-col gap-3">
  <span class="text-neutral-500 font-medium">{text}</span>
  {@render children()}
</label>
