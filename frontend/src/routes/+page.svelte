<script lang="ts">
  import RiBarChartBoxFill from "svelte-remixicon/RiBarChartBoxFill.svelte";
  import RiQrCodeFill from "svelte-remixicon/RiQrCodeFill.svelte";
</script>

<main
  class="flex flex-col font-medium px-4 gap-6 h-screen justify-around text-2xl text-center"
>
  <a
    href="/client"
    class="text-purple-800 flex items-center justify-center gap-3 max-sm:flex-col"
  >
    <RiQrCodeFill class="max-sm:text-4xl" />
    Клиентское приложение <span class="max-sm:hidden">--&gt;</span>
  </a>
  <a
    href="/partner"
    class="text-purple-800 flex items-center justify-center gap-3 max-sm:flex-col"
  >
    <RiBarChartBoxFill class="max-sm:text-4xl" />
    Личный кабинет партнёра <span class="max-sm:hidden">--&gt;</span>
  </a>
</main>
