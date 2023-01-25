<script>
	import { theme } from './themeStore';

	const switchTheme = () => {
		theme.set($theme == 'dark' ? 'light' : 'dark');
	};
</script>

<button
	class="button themeswitcher {$theme == 'dark' ? 'light' : 'dark'}"
	on:click={() => switchTheme()}
	>{#if $theme == 'dark'}☀️{:else}🌑{/if}</button
>

<style>
	.themeswitcher {
		position: absolute;
		margin: 2rem;
		right: 0;
		border: none;
	}
</style>
