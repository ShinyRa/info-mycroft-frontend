<script>
	import { onMount } from 'svelte';
	import { fade, slide } from 'svelte/transition';
	import { elasticOut } from 'svelte/easing';
	import { goto } from '$app/navigation';

	let loaded = false;

	onMount(async () => {
		loaded = true;
	});

	const navigate = () => goto('/talk');
</script>

<div class="touch" on:click={() => navigate()} on:keypress={() => navigate()}>
	{#if loaded}
		<div class="page">
			<section class="section">
				<h1 class="title">W A V E</h1>
				<h3 class="subtitle">Don't be shy!</h3>
			</section>
			<section class="section wrapper-welcome">
				<section class="section welcome is-medium">
					<img src="/img/dots.png" class="dots" alt="dots" />
					<img
						src="/img/wave.png"
						class="wave"
						alt="waving hand"
						in:slide={{ duration: 750, easing: elasticOut }}
						on:click={() => navigate()}
						on:keypress={() => navigate()}
					/>
				</section>
			</section>
			<section class="section footnote" in:fade={{ delay: 1000 }}>
				<img src="/img/footer.png" class="footnote" alt="Start by saying Hello Mycroft!" />
			</section>
		</div>
	{/if}
</div>

<style>
	.touch {
		position: absolute;
		height: 100vh;
		width: 100vw;
	}
	.page {
		height: 100vh;
		background: #f4f4f4;
		text-align: center;
	}

	.title {
		font-style: normal;
		font-weight: 700;
		font-size: 48px;
		line-height: 54px;

		color: #0072bb;
	}

	.wrapper-welcome {
		padding: 3rem;
	}

	.welcome {
		position: relative;
		text-align: center;
		width: 40rem;
		margin: 0 auto;
		padding: 0;
	}
	.subtitle {
		font-weight: 400;
		font-size: 36px;
		line-height: 41px;

		color: #313131;
	}

	.wave {
		position: absolute;
		height: 20rem;
		left: calc(20rem - 25%);
		top: 8%;

		/* top: 5%; */
	}

	.footnote {
		margin: 0 auto;
		width: 40rem;
		padding-top: 3rem;
	}
</style>
