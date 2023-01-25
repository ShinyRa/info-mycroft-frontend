<script>
	import { onMount } from 'svelte';
	import { fade, fly, slide } from 'svelte/transition';
	import { theme } from '../../components/theme/themeStore';
	import TextField from '../../components/input/TextField.svelte';
	import Face from '../../components/face/Face.svelte';
	import { Expressions } from '../../components/face/expression-states';
	import { elasticIn } from 'svelte/easing';
	import AudioPlayer from '../../components/audio/AudioPlayer.svelte';

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
	let switchExpression;

	const intro = [
		{
			dialogue: '',
			expression: Expressions.Neutral
		},
		{
			dialogue: 'Hi, I am Kiko !',
			expression: Expressions.Talking
		},
		{
			dialogue: 'I know a lot about travel information or weather updates for example',
			expression: Expressions.Winking
		},
		{
			dialogue: "If you need me, I'm listening...",
			expression: Expressions.Neutral
		},
		{
			dialogue: '',
			expression: Expressions.Neutral
		}
	];

	let dialogueIndex = 0;
	let renderInput = false;

	onMount(async () => {
		loaded = true;

		socket = new WebSocket('ws://10.0.0.241:1337/');

		let introSequence = setInterval(() => {
			dialogueIndex++;
			switchExpression(intro[dialogueIndex].expression);
			if (dialogueIndex != 1) {
				saveQuestion(null, intro[dialogueIndex - 1].dialogue);
			}
			if (intro[dialogueIndex + 1] == null) {
				renderInput = true;
				clearInterval(introSequence);
			}
		}, 2500);

		socket.onmessage = (event) => {
			if (event.data == answer) {
				return;
			}
			answer = event.data;
			if (
				answer.includes("don't understand") ||
				answer.includes('rephrase your request') ||
				answer.includes("didn't catch that") ||
				answer.includes('not sure I understood you') ||
				answer.includes('say that a different way') ||
				answer.includes("don't know")
			) {
				switchExpression(Expressions.Listening);
				playFail();
			} else {
				switchExpression(Expressions.Talking);
				playSuccess();
			}
			setTimeout(() => {
				readOutLoud(event.data);
			}, 750);
			setTimeout(() => {
				saveQuestion(question, answer);
				answer = '';
			}, 10000);
		};
	});

	const readOutLoud = (message) => {
		let speech = new SpeechSynthesisUtterance();
		speech.text = message;
		speech.volume = 1;
		speech.rate = 1;
		speech.pitch = 1;
		window.speechSynthesis.speak(speech);
	};

	const saveQuestion = (question, answer) => {
		questions.push({
			question: question,
			answer: answer
		});
		questions = questions;
	};

	const onInputFocus = () => {
		switchExpression(Expressions.Talking);
	};

	const onInputFocusOut = () => {
		switchExpression(Expressions.Neutral);
	};

	const submit = () => {
		switchExpression(Expressions.Thinking);
		socket.send(textFieldValue);
	};

	let playHello;
	let playFail;
	let playSuccess;
</script>

{#if loaded}
	<AudioPlayer bind:playHello bind:playFail bind:playSuccess />
	<div class="page {$theme}">
		{#key loaded}
			<section class="section emotion" in:fade={{ duration: 1500 }}>
				<Face bind:switchExpression />
			</section>
		{/key}
		<section class="section userinput {$theme}">
			{#key dialogueIndex}
				{#key answer}
					<div in:fly={{ duration: 500, delay: 450 }} out:fly={{ x: 0, y: 50 }}>
						{#if renderInput}
							<div class="answer">
								<h1 class="title {$theme}">{answer ? answer : ' '}</h1>
							</div>
						{:else}
							<h1 class="title {$theme}">{intro[dialogueIndex].dialogue}</h1>
						{/if}
					</div>
				{/key}
				{#if renderInput}
					<div in:fly={{ duration: 75, delay: 450 }}>
						<TextField
							bind:value={textFieldValue}
							onFocus={onInputFocus}
							onFocusOut={onInputFocusOut}
							onSubmit={submit}
						/>
					</div>
				{/if}
			{/key}
			<section class="section preview">
				{#each question as word, index}
					<div
						class="word-container"
						in:fly={{ duration: 75, x: 0, y: -15, easing: elasticIn, delay: index * 75 }}
					>
						{word}
					</div>
				{/each}
			</section>
		</section>

		<section class="section history">
			<ul>
				{#if questions.reverse()[0]}
					{#key dialogueIndex}
						<li
							class="list-item"
							in:fly={{ x: 0, y: -50, easing: elasticIn, delay: 450, duration: 75 }}
						>
							{#if questions.reverse()[0].question != null}
								<h3 class="subtitle">
									{questions.reverse()[0].question}
								</h3>
							{/if}
							<h1 class="answer">{questions.reverse()[0].answer}</h1>
						</li>
					{/key}
				{/if}
			</ul>
		</section>
	</div>
{/if}

<style>
	.page {
		height: 100vh;
		text-align: center;
		flex-direction: column;
	}
	.userinput {
		height: 20rem;
		position: relative;
	}
	.title {
		font-style: normal;
		font-weight: 700;
		font-size: 5rem;
	}
	.history {
		height: 20rem;
	}

	.word-container {
		display: flex;
		font-size: 3rem;
	}

	.answer {
		color: #1c8fd7;
		font-size: 4rem;
		min-height: 4rem;
		margin-bottom: 4rem;
	}
</style>
