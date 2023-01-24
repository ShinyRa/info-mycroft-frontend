<script>
	import { onMount } from 'svelte';
	import { fade, fly, slide } from 'svelte/transition';
	import * as eases from 'svelte/easing';
	import Microphone from './Microphone.svelte';
	import { elasticIn } from 'svelte/easing';

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

	onMount(async () => {
		loaded = true;

		socket = new WebSocket('ws://10.0.0.241:1337/');
	});

	const saveQuestion = (question, answer) => {
		questions.push({
			question: question.join(' '),
			answer: answer
		});
		questions = questions;
	};
</script>

<div class="touch" on:click={() => startRecording()} on:keypress={() => startRecording()}>
	{#if loaded}
		<div class="page">
			<section class="section">
				{#key state}
					<h1 class="title">{state ? "I'm listening..." : "I'm thinking..."}</h1>
				{/key}
				<Microphone
					{socket}
					onMessage={(question, answer) => saveQuestion(question, answer)}
					bind:state
					bind:question
					bind:answer
					bind:startRecording
				/>
			</section>
			<section class="section recording">
				<section class="section preview">
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
				</section>
			</section>

			{#key questions}
				<section class="section footnote">
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
			{/key}
		</div>
	{/if}
</div>

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
