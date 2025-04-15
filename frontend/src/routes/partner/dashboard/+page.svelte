<script lang="ts">
  import Pie from "$lib/components/pie.svelte";
  import { getStats } from "$lib/data/business";
  import RiQrCodeFill from "svelte-remixicon/RiQrCodeFill.svelte";
  import ProgramCreateForm from "./program-create-form.svelte";
  import Label from "$lib/components/label.svelte";
  import AvatarUpload from "./avatar-upload.svelte";

  let statsPromise = $state(getStats());
</script>

<main class="p-4 w-full flex flex-col gap-2 max-w-2xl mx-auto">
  <AvatarUpload />
  <a
    href="/partner/scan"
    class="font-medium text-neutral-700 bg-neutral-100 px-6 py-3 rounded-2xl flex items-center gap-2"
  >
    <RiQrCodeFill />
    Сканировать коды
  </a>
  {#await statsPromise}
    <div class="h-64 bg-neutral-100 rounded-2xl animate-pulse"></div>
    <div class="h-64 bg-neutral-100 rounded-2xl animate-pulse"></div>
    <div class="h-64 bg-neutral-100 rounded-2xl animate-pulse"></div>
  {:then stats}
    {#if stats}
      <Pie
        title="Возраст"
        values={[
          { color: "#FF6933", title: "до 18", value: stats.children! },
          { color: "#FFBD42", title: "18-30", value: stats.youngsters! },
          { color: "#5AA7B5", title: "30-50", value: stats.middle_aged! },
          { color: "#3D5A99", title: "50-70", value: stats.old! },
          { color: "#8D43AD", title: "от 70", value: stats.very_old! },
        ]}
      />
      <Pie
        title="Пол"
        values={[
          { color: "pink", title: "Женский", value: stats.female_count! },
          { color: "blue", title: "Мужской", value: stats.male_count! },
        ]}
      />
      <div
        class="p-4 rounded-2xl border-2 border-neutral-100 flex flex-col gap-2"
      >
        <Label text="Всего пользователей">
          {stats.total_clients!}
        </Label>
        <Label text="Накоплено очков">
          {stats.total_points!}
        </Label>
        <Label text="Выдано наград">
          {stats.total_rewarded!}
        </Label>
      </div>
    {:else}
      <ProgramCreateForm oncreated={() => (statsPromise = getStats())} />
    {/if}
  {/await}
</main>
