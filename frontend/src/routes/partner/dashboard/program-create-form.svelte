<script lang="ts">
  import Input from "$lib/components/input.svelte";
  import Label from "$lib/components/label.svelte";
  import { createProgram } from "$lib/data/business";

  let { oncreated }: { oncreated: () => void } = $props();

  let name = $state("");
  let target = $state<number>(undefined!);
  let reward = $state("");
  let maxClaims = $state<number>(undefined!);
</script>

<form
  class="flex flex-col gap-4 p-6 border-2 border-neutral-100 rounded-2xl"
  onsubmit={async (e) => {
    e.preventDefault();
    await createProgram(name, target, reward, maxClaims);
    oncreated();
  }}
>
  <h3 class="font-semibold text-lg text-start">Создать программу лояльности</h3>
  <Label text="Название">
    <Input
      placeholder="Каждый пятый стакан кофе бесплатно!"
      bind:value={name}
      required
    />
  </Label>
  <Label text="Цель накопления">
    <Input type="number" placeholder="4" bind:value={target} min={1} required />
  </Label>
  <Label text="Наименование награды">
    <Input
      placeholder="Стакан кофе на выбор (мал)"
      bind:value={reward}
      required
    />
  </Label>
  <Label text="Лимит наград">
    <Input
      type="number"
      placeholder="200"
      bind:value={maxClaims}
      min={1}
      required
    />
  </Label>
  <button
    class="flex-1 bg-neutral-100 p-3 rounded-lg font-semibold text-lg outline-none disabled:opacity-50"
    disabled={!name.trim() || !target || !reward.trim() || !maxClaims}
  >
    Создать
  </button>
</form>
