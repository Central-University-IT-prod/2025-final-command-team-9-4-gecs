<script lang="ts">
  import RiArrowLeftSFill from "svelte-remixicon/RiArrowLeftSFill.svelte";
  import {
    checkQr,
    redeem,
    type ProgramClientScheme,
  } from "$lib/data/business";
  import jsQR from "jsqr";
  import ScannedProgramDialog from "./scanned-program-dialog.svelte";

  let preview: HTMLVideoElement;
  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D;

  let throttled = false;
  let scannedProgram = $state<ProgramClientScheme | null>(null);
  let qrToken = $state("");

  function tick() {
    if (!ctx) ctx = canvas.getContext("2d", { willReadFrequently: true })!;
    if (preview.readyState === preview.HAVE_ENOUGH_DATA) {
      canvas.width = preview.videoWidth;
      canvas.height = preview.videoHeight;
      ctx.drawImage(preview, 0, 0);
      const img = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const qr = jsQR(img.data, img.width, img.height);
      if (
        qr &&
        qr.data.startsWith("eyJhbGc") &&
        !throttled &&
        !scannedProgram
      ) {
        throttled = true;
        checkQr(qr.data).then(
          (data) => {
            if (data) {
              qrToken = qr.data;
              scannedProgram = data;
            }
            throttled = false;
          },
          () => (throttled = false)
        );
      }
    }
    requestAnimationFrame(tick);
  }

  $effect(() => {
    const req = navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "environment",
      },
      audio: false,
    });
    req
      .then((stream) => {
        stream.onremovetrack = () => {
          console.log("Stream ended");
        };
        preview.srcObject = stream;
        preview.play();

        requestAnimationFrame(tick);
      })
      .catch((e) => console.error(e));
  });
</script>

<main class="p-4 w-full max-w-xl mx-auto relative h-screen">
  <a
    href="/partner/dashboard"
    class="rounded-full bg-neutral-50 size-9 absolute left-9 top-9 flex items-center justify-center z-10"
  >
    <RiArrowLeftSFill />
  </a>
  <canvas bind:this={canvas} hidden></canvas>
  <video
    bind:this={preview}
    class="rounded-2xl h-full object-cover bg-neutral-100"
  ></video>
  <div
    class="absolute left-1/2 top-1/2 -translate-1/2 w-1/2 aspect-square grid grid-cols-2"
  >
    <div
      class="size-12 border-t-6 border-l-6 rounded-tl-2xl border-purple-500"
    ></div>
    <div
      class="size-12 border-t-6 border-r-6 rounded-tr-2xl border-purple-500 justify-self-end"
    ></div>
    <div
      class="size-12 border-b-6 border-l-6 rounded-bl-2xl border-purple-500 self-end"
    ></div>
    <div
      class="size-12 border-b-6 border-r-6 rounded-br-2xl border-purple-500 self-end justify-self-end"
    ></div>
  </div>
</main>

<ScannedProgramDialog
  data={scannedProgram}
  oncancel={() => (scannedProgram = null)}
  onredeem={async () => {
    scannedProgram = null;
    redeem(qrToken);
  }}
/>
