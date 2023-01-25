<script>
	import { onMount } from 'svelte';
	import { fade, fly, slide } from 'svelte/transition';
	import { theme } from '../../components/theme/themeStore';
	import { elasticIn } from 'svelte/easing';
	import TextField from '../../components/input/TextField.svelte';
	import Face from '../../components/face/Face.svelte';

	/**
	 * @type {WebSocket}
	 */
	let socket;

	/**
	 * @type {any[]}
	 */
	let questions = [];

	/**
	 * @type boolean
	 */
	let loaded;

	let state;

	let startRecording;
	let question = [];
	let answer = '';
	let textFieldValue;

	const dialogue = [
		'Hi, I am Kiko !',
		'I know a lot about travel information or weather updates for example',
		'If you need me, I’m listening...'
	];

	let dialogueIndex = 0;

	onMount(async () => {
		loaded = true;

		socket = new WebSocket('ws://10.0.0.241:1337/');

		setInterval(() => {
			dialogueIndex++;
		}, 5000);
	});

	const saveQuestion = (question, answer) => {
		questions.push({
			question: question.join(' '),
			answer: answer
		});
		questions = questions;
	};
</script>

{#if loaded}
	<div class="page {$theme}">
		<section class="section emotion">
			<Face />
		</section>
		<section class="section input">
			{#key dialogueIndex}
				<div in:fade={{ duration: 500 }}>
					<h1>{dialogue[dialogueIndex]}</h1>
				</div>
			{/key}
			<TextField bind:value={textFieldValue} />
			<!-- <section class="section preview">
				{#each question as word, index}
					<div
						class="word-container"
						in:fly={{ duration: 75, x: 0, y: -15, easing: elasticIn, delay: index * 75 }}
					>
						{word}
					</div>
				{/each}
				<div class="answer">
					{#key answer}
						<h1 class="title answer">{answer}</h1>
					{/key}
				</div>
			</section> -->
		</section>

		<!-- {#key questions}
			<section class="section history">
				<ul>
					{#each questions.reverse() as qst}
						<li class="list-item" transition:slide={{ duration: 250, easing: elasticIn }}>
							<h3 class="subtitle">
								{qst.question}
							</h3>
							<h1 class="title answer">{qst.answer}</h1>
						</li>
					{/each}
				</ul>
			</section>
		{/key} -->
	</div>
{/if}

<style>
	.page {
		height: 100vh;
		text-align: center;
		flex-direction: column;
	}
	/* .input {
		height: 25rem;
		position: relative;
		padding: 6rem;
		background-image: url('/img/dots.png');
		background-repeat: no-repeat;
		background-position: center;
		margin: 2rem;
	} */
	.title {
		font-style: normal;
		font-weight: 700;
		font-size: 48px;
		line-height: 54px;
	}
	.history {
		height: 25rem;
	}
	.preview {
		display: flex;
		flex-direction: row;
		gap: 1.5rem;
		flex-wrap: wrap;
	}

	.word-container {
		display: flex;
		font-size: 3rem;
	}

	.answer {
		color: #0072bb;
	}
</style>
