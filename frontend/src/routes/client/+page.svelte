<script lang="ts">
  import QRCode from "@castlenine/svelte-qrcode";
  import RiLogoutBoxRLine from "svelte-remixicon/RiLogoutBoxRLine.svelte";

  import { getPrograms, getQrCodeData, logout } from "$lib/data/client";
  import RegistartionDialog from "./registartion-dialog.svelte";
  import Progress from "$lib/components/progress.svelte";

  let qrPromise = $state(getQrCodeData());
  let programsPromise = $state(getPrograms());

  let regOpen = $state(false);
</script>

<main class="flex flex-col w-full max-w-md mx-auto">
  <section
    class="bg-purple-500 w-full py-6 px-8 gap-4 flex flex-col rounded-b-2xl text-white"
  >
    {#await qrPromise}
      <div class="bg-neutral-100 rounded-lg animate-pulse h-12 w-full"></div>
    {:then data}
      {#if data.name}
        <div class="font-medium flex items-center justify-between">
          <span>Здравствуй, {data.name}!</span>
          <button
            onclick={async () => {
              await logout();
              qrPromise = getQrCodeData();
              programsPromise = getPrograms();
            }}
          >
            <RiLogoutBoxRLine />
          </button>
        </div>
      {:else}
        <button
          class="rounded-lg bg-white p-4 text-start leading-5 font-medium text-black
          border-2 border-purple-200"
          onclick={() => (regOpen = true)}
        >
          Войдите в аккаунт, чтобы получать награды и не потерять прогресс!
        </button>
      {/if}
    {/await}
    <div
      class="rounded-lg bg-white aspect-square p-4 flex flex-col text-purple-500"
    >
      {#await qrPromise}
        <div class="w-full bg-neutral-100 rounded-md aspect-square"></div>
      {:then qr}
        <QRCode data={qr.token!} isResponsive color="currentColor" />
      {/await}
    </div>
    <p class="text-2xl font-semibold">Покажи QR кассиру чтобы учесть покупку</p>
  </section>
  <section class="p-6 flex flex-col gap-4">
    <h2 class="font-semibold text-xl">Программы лояльности</h2>
    {#await programsPromise}
      <div class="bg-neutral-100 h-24 rounded-lg animate-pulse"></div>
      <div class="bg-neutral-100 h-24 rounded-lg animate-pulse"></div>
      <div class="bg-neutral-100 h-24 rounded-lg animate-pulse"></div>
    {:then programs}
      {#each programs as program}
        <figure
          class="bg-neutral-100 p-4 flex flex-col gap-3 rounded-lg font-medium"
        >
          <Progress current={program.points!} target={program.target!} />
          <figcaption>{program.name}</figcaption>
          <div class="flex items-center gap-2 text-neutral-500 text-xs">
            <img
              src="/api/business/{program.business_id!}/image"
              alt="Изображение компании"
              class="size-4 rounded object-cover"
            />
            <p>{program.business_name}</p>
          </div>
        </figure>
      {:else}
        Доступных программ лояльности нет. Время начать собирать баллы!
      {/each}
    {/await}
  </section>
</main>

<RegistartionDialog
  open={regOpen}
  onfinished={() => {
    regOpen = false;
    qrPromise = getQrCodeData();
    programsPromise = getPrograms();
  }}
/>
