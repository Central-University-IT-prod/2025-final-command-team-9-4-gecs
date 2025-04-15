<script>
  import RiUploadLine from "svelte-remixicon/RiUploadLine.svelte";
  import { updateAvatar } from "$lib/data/business";
</script>

<div class="flex items-center gap-5">
  <label
    class="p-4 flex items-center justify-center aspect-square w-16 border-2 border-neutral-400 border-dashed rounded-2xl"
  >
    <input
      class="sr-only"
      type="file"
      accept="image/*"
      onchange={async (e) => {
        const files = e.currentTarget.files;
        const file = files?.item(0);
        if (!file) return;
        await updateAvatar(file);
      }}
    />
    <RiUploadLine />
  </label>
  <div class="font-semibold py-1 px-3 bg-neutral-100 rounded-lg relative">
    Обновить изображение компании
    <div
      class="border-8 right-full absolute top-1/2 -translate-y-1/2 border-transparent border-r-neutral-100 translate-x-0.5"
    ></div>
  </div>
</div>
