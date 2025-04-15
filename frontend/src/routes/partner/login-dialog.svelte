<script lang="ts">
  import Dialog from "$lib/components/dialog.svelte";
  import Input from "$lib/components/input.svelte";
  import Label from "$lib/components/label.svelte";
  import { login } from "$lib/data/business";

  let failed = $state(false);

  let email = $state("");
  let password = $state("");

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
  title="Авторизация"
  next="Войти"
  onnext={async () => {
    failed = false;
    const res = await login(email, password);
    if (!res) failed = true;
    else onfinish();
  }}
  disabled={!email.trim() || !password}
  {open}
>
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
  <button type="button" class="font-medium text-start" onclick={onswitch}>
    Создать аккаунт --&gt;
  </button>
  {#if failed}
    <span class="text-red-800">
      Учётные данные не подошли, попробуйте снова.
    </span>
  {/if}
</Dialog>
