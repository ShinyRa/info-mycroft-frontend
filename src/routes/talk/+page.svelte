<script>
	import { onMount } from 'svelte';

	/**
	 * @type {BlobPart[] | undefined}
	 */
	let media = [];
	/**
	 * @type {MediaRecorder | null}
	 */
	let mediaRecorder = null;

	/**
	 * @type {number}
	 * 1 = recording
	 * 0 = stopped
	 */
	let state;

	let audio;
	/**
	 * @type boolean
	 */
	let loaded;

	let time = 1000;

	let timeElapsed = 0;

	onMount(async () => {
		const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

		mediaRecorder = new MediaRecorder(stream);
		mediaRecorder.ondataavailable = (e) => media?.push(e.data);
		mediaRecorder.onstop = function () {
			const blob = new Blob(media, { type: 'audio/ogg; codecs=opus' });
			media = [];
			audio.src = window.URL.createObjectURL(blob);
		};
		loaded = true;
	});
	function startRecording() {
		mediaRecorder?.start();
		state = 1;
		timeElapsed = 0;

		let recording = setInterval(() => {
			timeElapsed += 10;
		}, 10);
		setTimeout(() => {
			console.log('Time');
			clearInterval(recording);
			stopRecording();
		}, time);
	}
	function stopRecording() {
		console.log(media);
		mediaRecorder?.stop();
		state = 0;
	}
</script>

{#if loaded}
	<div class="page">
		<section class="section">
			{#key state}
				<h1 class="title">{state ? "I'm listening..." : "I'm thinking..."}</h1>
			{/key}
			<progress class="progress is-info" value={timeElapsed} max={time}>45%</progress>
			<div id="waveform" />
		</section>
		<audio controls bind:this={audio} />
		<button on:click={startRecording}>Record</button>
		<button on:click={stopRecording}>Stop</button>
	</div>
{/if}

<style>
	.page {
		text-align: center;
	}
	.title {
		font-style: normal;
		font-weight: 700;
		font-size: 48px;
		line-height: 54px;
	}
</style>
