<script>
	import { onMount } from 'svelte';
	import { bounceIn } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	let socket;

	let questions = [];

	let question = '';
	let answer = '';

	let SpeechRecognition;

	/**
	 * @type {{ continuous: boolean; onresult: { (event: any): void; (event: any): void; }; }}
	 */
	let recognition;
	/**
	 * @type boolean
	 */
	let loaded;

	let time = 5000;

	let timeElapsed = 0;

	let state;

	onMount(async () => {
		loaded = true;

		socket = new WebSocket('ws://10.0.0.241:1337/');

		socket.onmessage = (event) => {
			console.log(event);
			answer = event.data;
			readOutLoud(event.data);
			saveQuestion();
		};

		// socket.addEventListener('open', (event) => {
		// 	socket.send('Hello Server!');
		// });

		try {
			SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
			recognition = new SpeechRecognition();
		} catch (e) {
			console.error(e);
		}
		recognition.lang = 'en-US';
		recognition.continuous = true;
		recognition.onresult = function (event) {
			let current = event.resultIndex;
			let transcript = event.results[current][0].transcript;
			question += transcript;
		};
	});

	function readOutLoud(message) {
		let speech = new SpeechSynthesisUtterance();
		speech.text = message;
		speech.volume = 1;
		speech.rate = 1;
		speech.pitch = 1;
		window.speechSynthesis.speak(speech);
	}

	const startRecording = () => {
		question = '';
		answer = '';
		recognition.start();
		state = 1;
		timeElapsed = 0;

		let recording = setInterval(() => {
			timeElapsed += 10;
		}, 10);
		setTimeout(() => {
			clearInterval(recording);
			stopRecording();
		}, time);
	};

	const stopRecording = () => {
		recognition.stop();
		state = 0;
		console.log('sending:' + question);
		socket.send(question);
	};

	const saveQuestion = () => {
		questions.push({
			question: question,
			answer: answer
		});
		questions = questions;
	};
</script>

{#if loaded}
	<div class="page">
		<section class="section">
			{#key state}
				<h1 class="title">{state ? "I'm listening..." : "I'm thinking..."}</h1>
			{/key}
			<progress class="progress is-info" value={timeElapsed} max={time} />
		</section>
		<section class="section recording">
			<section class="section preview">
				{#key question}
					<h2 class="subtitle">{question}</h2>
				{/key}
				{#key answer}
					<h1 class="title answer">{answer}</h1>
				{/key}
			</section>
		</section>
		<button class="button is-primary" on:click={startRecording}>Record</button>

		{#key questions}
			<section class="section footnote">
				<ul>
					{#each questions.reverse() as qst}
						<li class="list-item" in:slide={{ easing: bounceIn }}>
							<h3 class="subtitle">
								{qst.question}
							</h3>
							<h1 class="title answer">{qst.answer}</h1>
						</li>
					{/each}
				</ul>
			</section>
		{/key}
	</div>
{/if}

<style>
	.page {
		height: 100vh;
		background: #f4f4f4;
		text-align: center;
	}
	.recording {
		height: 25rem;
		position: relative;
		padding: 6rem;
		background-image: url('/img/dots.png');
		background-repeat: no-repeat;
		background-position: center;
		margin: 2rem;
	}
	.title {
		font-style: normal;
		font-weight: 700;
		font-size: 48px;
		line-height: 54px;
	}
	.footnote {
		height: 25rem;
	}

	.answer {
		color: #0072bb;
	}
</style>
