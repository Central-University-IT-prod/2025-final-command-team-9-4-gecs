<script lang="ts">
  let {
    title,
    values,
  }: {
    title: string;
    values: {
      value: number;
      color: string;
      title: string;
    }[];
  } = $props();
  let canvas: HTMLCanvasElement;

  $effect(() => {
    const resize = () => {
      canvas.width = canvas.clientWidth;
      canvas.height = canvas.clientHeight;
      draw();
    };
    window.addEventListener("resize", resize);
    resize();
    return () => window.removeEventListener("resize", resize);
  });

  const draw = $derived(() => {
    const sum = values.reduce((p, c) => p + c.value, 0);
    const ctx = canvas.getContext("2d")!;
    ctx.imageSmoothingQuality = "high";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let offset = 0;
    const x = canvas.width / 2,
      y = canvas.height / 2;
    const r = Math.min(x, y) - 24;
    if (sum === 0) {
      ctx.fillStyle = "gray";
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
      return;
    }
    for (const value of values) {
      const proportion = value.value / sum;
      ctx.beginPath();
      ctx.fillStyle = value.color;
      ctx.moveTo(x, y);
      ctx.lineTo(
        x + Math.cos(offset * Math.PI * 2) * r,
        y + Math.sin(offset * Math.PI * 2) * r
      );
      ctx.arc(
        canvas.width / 2,
        canvas.height / 2,
        r,
        offset * Math.PI * 2,
        (offset + proportion) * Math.PI * 2
      );
      ctx.lineTo(canvas.width / 2, canvas.height / 2);
      ctx.fill();
      offset += proportion;
    }
  });
</script>

<section
  class="flex flex-col gap-2 p-4 border-2 border-neutral-100 rounded-2xl"
>
  <h3 class="font-semibold text-2xl text-start">{title}</h3>
  <canvas bind:this={canvas} class="h-64"></canvas>
  <div class="flex items-center justify-center gap-4 flex-wrap">
    {#each values as { color, title }}
      <div class="flex items-center gap-1 text-neutral-500 text-sm">
        <div class="size-3 rounded" style="background: {color}"></div>
        {title}
      </div>
    {/each}
  </div>
</section>
