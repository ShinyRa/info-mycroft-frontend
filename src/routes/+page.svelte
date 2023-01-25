<script>
	import { onMount } from 'svelte';
	import { fade, scale } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import { quintOut } from 'svelte/easing';
	import { theme } from '../components/theme/themeStore';
	import ThemeSwitcher from '../components/theme/ThemeSwitcher.svelte';

	let loaded = false;
	let animation = 0;

	onMount(async () => {
		loaded = true;
		setInterval(() => {
			animation += 1;
			if (animation == 3) {
				animation = 0;
			}
		}, 1700);
	});

	const navigate = () => goto('/talk');
</script>

{#if loaded}
	<div class="touch" on:click={() => navigate()} on:keypress={() => navigate()} />
	{#key $theme}
		<ThemeSwitcher />
		<div class="page {$theme}" in:scale={{ start: 0.9, easing: quintOut, duration: 500 }}>
			{#if animation == 0}
				<img
					src="/img/{$theme}/touch-icon-2.png"
					class="touch-icon"
					in:scale={{ opacity: 0.5, start: 0.5, easing: quintOut, duration: 250 }}
				/>
			{:else if animation == 1}
				<img src="/img/{$theme}/touch-icon.png" class="touch-icon" out:fade />
			{/if}
		</div>
	{/key}
{/if}

<style>
	.touch {
		position: absolute;
		bottom: 0;
		height: 90vh;
		width: 100vw;
	}
	.page {
		height: 100vh;
		text-align: center;
		background-repeat: no-repeat;
		background-position: center;
	}
	.page.dark {
		background-image: url('img/dark/dots.png');
	}
	.page.light {
		background-image: url('img/light/dots.png');
	}
	.touch-icon {
		margin: 25rem auto;
		height: 8rem;
		fill: white;
	}
</style>
