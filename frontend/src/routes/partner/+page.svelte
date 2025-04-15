<script lang="ts">
  import { goto } from "$app/navigation";
  import { getToken } from "$lib/data/business";
  import LoginDialog from "./login-dialog.svelte";
  import RegistrationDialog from "./registration-dialog.svelte";

  $effect(() => {
    if (!!getToken()) goto("/partner/dashboard");
  });

  let login = $state(true);
</script>

<LoginDialog
  open={login}
  onswitch={() => (login = false)}
  onfinish={() => goto("/partner/dashboard")}
/>
<RegistrationDialog
  open={!login}
  onswitch={() => (login = true)}
  onfinish={() => goto("/partner/dashboard")}
/>
