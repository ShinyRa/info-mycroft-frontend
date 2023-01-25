<script>
	let helloSound;
	let failSound;
	let goodbyeSound;
	let successSound;

	const stopAll = () => {
		helloSound.pause();
		helloSound.time = 0;

		failSound.pause();
		failSound.time = 0;

		successSound.pause();
		successSound.time = 0;
	};

	export const playHello = () => {
		stopAll();
		helloSound.play();
	};

	export const playFail = () => {
		stopAll();
		failSound.play();
	};

	export const playSuccess = () => {
		stopAll();
		successSound.play();
	};
</script>

<div class="invisible">
	<audio src="/sounds/Hello.mp3" bind:this={helloSound} />
	<audio src="/sounds/Failure.mp3" bind:this={failSound} />
	<audio src="/sounds/Goodbye.mp3" bind:this={goodbyeSound} />
	<audio src="/sounds/Success.mp3" bind:this={successSound} />
</div>

<style>
	.invicible {
		visibility: hidden;
	}
</style>
