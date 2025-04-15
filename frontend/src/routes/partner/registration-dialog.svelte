<script lang="ts">
  import Dialog from "$lib/components/dialog.svelte";
  import Input from "$lib/components/input.svelte";
  import Label from "$lib/components/label.svelte";
  import { regsiter } from "$lib/data/business";

  let failed = $state(false);

  let email = $state("");
  let name = $state("");
  let password = $state("");
  let location = $state("");

  let {
    open,
    onswitch,
    onfinish,
  }: {
    open: boolean;
    onswitch: () => void;
    onfinish: () => void;
  } = $props();
</script>

<Dialog
  title="Регистрация"
  next="Создать"
  onnext={async () => {
    failed = false;
    const res = await regsiter(email, password, name, "", location);
    if (!res) failed = true;
    else onfinish();
  }}
  disabled={!email.trim() || !password}
  {open}
>
  <Label text="Название компании">
    <Input bind:value={name} placeholder="Инвест-кафе Пульс" required />
  </Label>
  <Label text="Почта">
    <Input
      type="email"
      bind:value={email}
      placeholder="admin@example.com"
      required
    />
  </Label>
  <Label text="Пароль">
    <Input
      type="password"
      bind:value={password}
      placeholder="••••••••"
      required
    />
  </Label>
  <Label text="Город">
    <Input bind:value={location} placeholder="Яхонты" required />
  </Label>
  <button type="button" class="font-medium text-start" onclick={onswitch}>
    Уже есть аккаунт --&gt;
  </button>
  {#if failed}
    <span class="text-red-800">
      Не удалось создать компанию, возможно почта занята.
    </span>
  {/if}
</Dialog>
