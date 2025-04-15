<script lang="ts">
  import { invalidateAll } from "$app/navigation";
  import Dialog from "$lib/components/dialog.svelte";
  import Input from "$lib/components/input.svelte";
  import Label from "$lib/components/label.svelte";
  import Select from "$lib/components/select.svelte";
  import { login, regsiter } from "$lib/data/client";

  let { open, onfinished }: { open: boolean; onfinished: () => void } =
    $props();
  let step = $state(0);

  let name = $state("");
  let email = $state("");
  let password = $state("");
  let gender = $state("unknown");
  let location = $state("");
  let age = $state<number>(undefined!);
</script>

<Dialog
  title="Регистрация"
  onnext={async () => {
    if (step === 0) {
      const res = await login(email, password);
      if (res) {
        onfinished();
        return;
      }
    }
    if (++step == 3) {
      await regsiter(email, password, name, age, location, gender);
      onfinished();
    }
  }}
  onback={step > 0 && step < 3 && (() => --step)}
  disabled={(step === 0 && (!email.trim() || password.length < 8)) ||
    (step === 1 && (!name.trim() || !age)) ||
    (step === 2 && !location.trim()) ||
    step >= 3}
  {open}
>
  {#if step === 0}
    <Label text="Почта">
      <Input type="email" bind:value={email} placeholder="meow@example.com" />
    </Label>
    <Label text="Пароль">
      <Input type="password" bind:value={password} placeholder="••••••••" />
    </Label>
  {:else if step === 1}
    <Label text="Имя и фамилия">
      <Input bind:value={name} placeholder="Терри Девис" />
    </Label>
    <Label text="Возраст">
      <Input
        type="number"
        bind:value={age}
        placeholder="42"
        min={12}
        max={150}
      />
    </Label>
  {:else if step === 2}
    <Label text="Город">
      <Input bind:value={location} placeholder="Яхонты" />
    </Label>
    <Label text="Пол">
      <Select bind:value={gender}>
        <option value="unknown">Не указан</option>
        <option value="male">Мужской</option>
        <option value="female">Женский</option>
      </Select>
    </Label>
  {:else}
    <div
      class="mx-auto size-24 border-transparent border-2 border-b-black rounded-full animate-spin"
    ></div>
  {/if}
</Dialog>
