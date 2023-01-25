<script>
	import { onMount } from 'svelte';
	import { fade, scale } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import { quintOut } from 'svelte/easing';

	let loaded = false;
	let animation = 0;

	let theme = 'dark';

	onMount(async () => {
		loaded = true;
		setInterval(() => {
			animation += 1;
			if (animation == 3) {
				animation = 0;
			}
		}, 1700);
	});

	const switchTheme = () => {
		console.log('switch');
		theme = theme == 'dark' ? 'light' : 'dark';
		animation = 2;
	};

	const navigate = () => goto('/talk');
</script>

{#if loaded}
	<div class="touch" on:click={() => navigate()} on:keypress={() => navigate()} />
	{#key theme}
		<div class="page {theme}" in:scale={{ start: 0.9, easing: quintOut, duration: 500 }}>
			<button class="button {theme == 'dark' ? 'light' : 'dark'}" on:click={() => switchTheme()}
				>{#if theme == 'dark'}☀️{:else}🌑{/if}</button
			>
			{#if animation == 0}
				<img
					src="/img/{theme}/touch-icon-2.png"
					class="touch-icon"
					in:scale={{ opacity: 0.5, start: 0.5, easing: quintOut, duration: 250 }}
				/>
			{:else if animation == 1}
				<img src="/img/{theme}/touch-icon.png" class="touch-icon" out:fade />
			{/if}
		</div>
	{/key}
{/if}

<style>
	button {
		position: absolute;
		margin: 2rem;
		right: 0;
		border: none;
	}
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
	.dark {
		background-color: #00568f;
		color: white;
	}
	.light {
		background-color: white;
		color: #00568f;
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
