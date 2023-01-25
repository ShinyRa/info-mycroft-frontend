<script>
	import { onMount } from 'svelte';
	import { fly, slide } from 'svelte/transition';
	import * as eases from 'svelte/easing';
	import Microphone from './Microphone.svelte';
	import {Expressions} from "../../expression-states";
	import {EyeStates} from "../../eye-states";
	import {ExpressionsToEyeStates} from "../../expressions-to-eyestates";
	import {EyeStatesToImgSrc} from "../../eyestates-to-img-src";
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

	let leftEye;
	let leftEyeState = EyeStates.Neutral;
	let rightEye;
	let rightEyeState = EyeStates.Neutral;

	let expressionQueue = [];
	let expressionAnimationPromise = null;

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

	const getKeyByValue = (object, value) => {
  		return Object.keys(object).find(key => JSON.stringify(object[key]) === JSON.stringify(value));
	}

	const switchExpression = (expression) => { 
		console.log(expression)
		if(expression == null) return; 
		//then write logic to push correct animations for each eye to achieve smooth switch of expressions
		let lastPair = [];

		const queueLength = expressionQueue.length;
		if(queueLength > 0){
			lastPair = expressionQueue[queueLength-1];
		}
		else {
			lastPair = [leftEyeState, rightEyeState];
		}
		
		if(expression == Expressions.Neutral){
			expressionQueue.unshift(ExpressionsToEyeStates.Neutral);

			if(expressionAnimationPromise == null) startExpressionAnimations();
			return;
		} 

		let lastExpression = getKeyByValue(ExpressionsToEyeStates, lastPair);

		if(expression == Expressions.Winking){
			if(Expressions[lastExpression] != Expressions.Neutral){
				expressionQueue.unshift(ExpressionsToEyeStates.Neutral);
			} 

			expressionQueue.unshift(ExpressionsToEyeStates.Winking);

			if(expressionAnimationPromise == null) startExpressionAnimations();
			return;
		}

		if(expression == lastExpression){
			expressionQueue.unshift(lastPair);
		} else {
			if(Expressions[lastExpression] != Expressions.Neutral){
				expressionQueue.unshift(ExpressionsToEyeStates.Neutral);
			} 

			let expressionIndex = getKeyByValue(Expressions, expression);
			expressionQueue.unshift(ExpressionsToEyeStates[expressionIndex]);
		}

		if(expressionAnimationPromise) return;

		startExpressionAnimations();
	};

	const startExpressionAnimations = () => {
		console.log(expressionQueue)
		expressionAnimationPromise = new Promise(async (resolve) => {
			//1. take the first pair of eye animations form the queue
			while(expressionQueue.length > 0){
				let pair = expressionQueue.pop();
				console.log(pair)

				//2. for each eye: check that the state is not the eyes current state, if not: switch the src to new image
				//rewrite to be usable as function for both eyes
				if(leftEyeState != pair[0]) {
					let img;
					let reversed = "";

					if(pair[0] == EyeStates.Neutral){
						img = EyeStatesToImgSrc[leftEyeState]
						reversed = "_reverse"
					} else{
						img = EyeStatesToImgSrc[pair[0]]
						reversed = ""
					}

					if(leftEyeState == EyeStates.Down || pair[0] == EyeStates.Down){
						leftEye.style = "transform: scaleY(-1)";
					} else {
						leftEye.style = "transform: scaleY(1)";
					}
					
					let newSrc = `img/eye_animations/dark/${img}${reversed}.svg`
					leftEye.src = newSrc
					leftEyeState = pair[0]
					refreshImage(leftEye);
				}

				if(rightEyeState != pair[1]) {
					let img;
					let reversed = "";

					if(pair[1] == EyeStates.Neutral){
						img = EyeStatesToImgSrc[rightEyeState]
						reversed = "_reverse"
					} else{
						img = EyeStatesToImgSrc[pair[1]]
						reversed = ""
					}

					if(rightEyeState == EyeStates.Down || pair[1] == EyeStates.Down){
						rightEye.style = "transform: scaleY(-1)";
					} else {
						rightEye.style = "transform: scaleY(1)";
					}

					let newSrc = `img/eye_animations/dark/${img}${reversed}.svg`
					rightEye.src = newSrc
					rightEyeState = pair[1]
					refreshImage(rightEye);
				}

				//3. set an await for 0.4s 
				await new Promise(awaitResolve => setTimeout(awaitResolve, 400))
			}
			
			
			//4. go to step 1
			//5. repeat until queue is empty -> resolve
			resolve(true); 
		}).then(()=>{expressionAnimationPromise = null});
	};

	const refreshEyes = () => {
		refreshImage(leftEye);
		refreshImage(rightEye);
	};

	const refreshImage = (element) => {    
		// wacky code to reload image source to reset css animation concistently
		if(!element) return;

		var timestamp = new Date().getTime();  
		let imgURL = element.src.split('?')[0]
	
		var queryString = "?t=" + timestamp;    
	
		element.src = imgURL + queryString;    
	};

</script>

<div class="touch" on:click={() => startRecording()} on:keypress={() => startRecording()}>
	{#if loaded}
		<div class="page">
			<section class="section">
				<img bind:this={leftEye} src="img/eye_animations/dark/eye_neutral.svg" id="leftEye"  alt="eye">
			<img bind:this={rightEye} src="img/eye_animations/dark/eye_neutral.svg" id="rightEye"  alt="eye">
				{#key state}
					<h1 class="title">
						{#if state == Expressions.Thinking} "I'm listening..."
						{:else if state == Expressions.Winking} "I'm winking..." {/if}
					</h1>
					{switchExpression(state)}
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
		background: #00568f;
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
