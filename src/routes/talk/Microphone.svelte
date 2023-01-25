<script type="typescript">
	import { onMount } from 'svelte';
	import { Expressions } from '../../expression-states';

	export let socket;
	export let onMessage;

	let SpeechRecognition;

	let recognition: {
		lang: string;
		continuous: boolean;
		onresult: (event: any) => void;
		start: () => void;
		stop: () => void;
	};

	let time = 7000;

	let timeElapsed = 0;

	export let state;
	export let question = '';
	export let answer = '';

	onMount(async () => {
		try {
			SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
			recognition = new SpeechRecognition();
		} catch (e) {
			console.error(e);
		}
		recognition.lang = 'en-US';
		recognition.continuous = true;
		recognition.interimResults = true;
		recognition.onresult = (event) => {
			let current = event.resultIndex;
			let transcript = event.results[current][0].transcript;
			if (transcript.length > question.length) {
				question = transcript.split(' ');
			}
		};
	});

	export const startRecording = () => {
		question = '';
		answer = '';
		recognition.start();
		state = Expressions.Listening;
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
		state = Expressions.Neutral;
		console.log('sending:' + question);
		socket.send(question.join(' '));
	};
</script>

<progress class="progress is-info" value={timeElapsed} max={time} />
