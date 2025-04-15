import tailwindcss from "@tailwindcss/vite";
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';

export default defineConfig({
	plugins: [
		sveltekit(),
		SvelteKitPWA({
            pwaAssets: {
                config: true,
            },
            manifest: {
				name: "LoaylLottie",
				short_name: "LoyalLottie",
                theme_color: "#ffffff",
                lang: "ru",
            },
		}),
		tailwindcss()
	]
});
