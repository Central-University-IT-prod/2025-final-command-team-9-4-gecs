<script lang="ts">
  import Dialog from "$lib/components/dialog.svelte";
  import Progress from "$lib/components/progress.svelte";
  import { type ProgramClientScheme } from "$lib/data/business";

  let {
    data,
    oncancel,
    onredeem,
  }: {
    data: ProgramClientScheme | null;
    oncancel: () => void;
    onredeem: () => void;
  } = $props();
  let redeemAvailable = $derived(
    !!data && !!data.points! && data.points! % data.target! === 0
  );
</script>

<Dialog
  open={!!data}
  title={redeemAvailable ? "Получение награды" : "Начисление"}
  onnext={onredeem}
  onback={oncancel}
  disabled={redeemAvailable && !data?.redeemable}
  back="Отмена"
  next="Всё верно"
>
  {#if data}
    <h3 class="font-medium">
      {#if redeemAvailable}
        У пользователя будет списана награда по акции “{data.name}”.
      {:else}
        Пользователь поулчит прогресс по акции “{data.name}”.
      {/if}
    </h3>
    <Progress current={data.points!} target={data.target!} />
    {#if redeemAvailable && !data.redeemable}
      Получение недоступно, попросите пользователя закончить профиль.
    {/if}
  {/if}
</Dialog>
