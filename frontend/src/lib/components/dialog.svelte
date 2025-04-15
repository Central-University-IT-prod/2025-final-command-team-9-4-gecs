<script lang="ts">
  import type { Snippet } from "svelte";

  let {
    title,
    children,
    open,
    onnext,
    onback,
    disabled,
    next = "Далее",
    back = "Назад",
  }: {
    title: string;
    children: Snippet;
    onback?: (() => void) | false;
    onnext: () => void;
    open: boolean;
    disabled?: boolean;
    next?: string;
    back?: string;
  } = $props();
  let dialog: HTMLDialogElement;

  $effect(() => {
    if (open) dialog.showModal();
    else dialog.close();
  });
</script>

<dialog
  bind:this={dialog}
  class="w-full max-w-lg block fixed bg-transparent
  select-none opacity-0 open:opacity-100 transition pointer-events-none open:pointer-events-auto translate-y-12
  open:translate-y-0 m-auto mb-0 outline-none p-4"
>
  <form
    class="flex flex-col gap-4 p-6 bg-white rounded-2xl"
    method="dialog"
    onsubmit={(e) => {
      e.preventDefault();
      if (!disabled) onnext();
    }}
  >
    <h2 class="font-semibold text-xl text-center">
      {title}
    </h2>
    {@render children()}
    <div class="flex gap-2">
      {#if onback}
        <button
          type="button"
          class="flex-1 bg-neutral-100 p-3 rounded-lg font-semibold text-lg outline-none"
          onclick={onback}
        >
          {back}
        </button>
      {/if}
      <button
        class="flex-1 bg-neutral-100 data-[contrast=true]:bg-purple-500 data-[contrast=true]:text-white p-3 rounded-lg font-semibold text-lg outline-none disabled:opacity-50"
        data-contrast={!!onback}
        {disabled}
      >
        {next}
      </button>
    </div>
  </form>
</dialog>
