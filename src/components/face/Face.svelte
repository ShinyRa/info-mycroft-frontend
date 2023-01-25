<script>
	import { theme } from '../theme/themeStore';

	import { Expressions } from './expression-states';
	import { EyeStates } from './eye-states';

	import { ExpressionsToEyeStates } from './expressions-to-eyestates';
	import { EyeStatesToImgSrc } from './eyestates-to-img-src';

	let leftEye;
	let leftEyeState = EyeStates.Neutral;
	let rightEye;
	let rightEyeState = EyeStates.Neutral;

	let expressionQueue = [];
	let expressionAnimationPromise = null;

	const getKeyByValue = (object, value) => {
		return Object.keys(object).find((key) => JSON.stringify(object[key]) === JSON.stringify(value));
	};

	export const switchExpression = (expression) => {
		if (expression == null) return;
		//then write logic to push correct animations for each eye to achieve smooth switch of expressions
		let lastPair = [];

		const queueLength = expressionQueue.length;
		if (queueLength > 0) {
			lastPair = expressionQueue[queueLength - 1];
		} else {
			lastPair = [leftEyeState, rightEyeState];
		}

		if (expression == Expressions.Neutral) {
			expressionQueue.unshift(ExpressionsToEyeStates.Neutral);

			if (expressionAnimationPromise == null) startExpressionAnimations();
			return;
		}

		let lastExpression = getKeyByValue(ExpressionsToEyeStates, lastPair);

		if (expression == Expressions.Winking) {
			if (Expressions[lastExpression] != Expressions.Neutral) {
				expressionQueue.unshift(ExpressionsToEyeStates.Neutral);
			}

			expressionQueue.unshift(ExpressionsToEyeStates.Winking);

			if (expressionAnimationPromise == null) startExpressionAnimations();
			return;
		}

		if (expression == lastExpression) {
			expressionQueue.unshift(lastPair);
		} else {
			if (Expressions[lastExpression] != Expressions.Neutral) {
				expressionQueue.unshift(ExpressionsToEyeStates.Neutral);
			}

			let expressionIndex = getKeyByValue(Expressions, expression);
			expressionQueue.unshift(ExpressionsToEyeStates[expressionIndex]);
		}

		if (expressionAnimationPromise) return;

		startExpressionAnimations();
	};

	const startExpressionAnimations = () => {
		expressionAnimationPromise = new Promise(async (resolve) => {
			//1. take the first pair of eye animations form the queue
			while (expressionQueue.length > 0) {
				let pair = expressionQueue.pop();

				//2. for each eye: check that the state is not the eyes current state, if not: switch the src to new image
				//rewrite to be usable as function for both eyes
				if (leftEyeState != pair[0]) {
					let img;
					let reversed = '';

					if (pair[0] == EyeStates.Neutral) {
						img = EyeStatesToImgSrc[leftEyeState];
						reversed = '_reverse';
					} else {
						img = EyeStatesToImgSrc[pair[0]];
						reversed = '';
					}

					if (leftEyeState == EyeStates.Down || pair[0] == EyeStates.Down) {
						leftEye.style = 'transform: scaleY(-1)';
					} else {
						leftEye.style = 'transform: scaleY(1)';
					}

					let newSrc = `img/eye_animations/${$theme}/${img}${reversed}.svg`;
					leftEye.src = newSrc;
					leftEyeState = pair[0];
					refreshImage(leftEye);
				}

				if (rightEyeState != pair[1]) {
					let img;
					let reversed = '';

					if (pair[1] == EyeStates.Neutral) {
						img = EyeStatesToImgSrc[rightEyeState];
						reversed = '_reverse';
					} else {
						img = EyeStatesToImgSrc[pair[1]];
						reversed = '';
					}

					if (rightEyeState == EyeStates.Down || pair[1] == EyeStates.Down) {
						rightEye.style = 'transform: scaleY(-1)';
					} else {
						rightEye.style = 'transform: scaleY(1)';
					}

					let newSrc = `img/eye_animations/${$theme}/${img}${reversed}.svg`;
					rightEye.src = newSrc;
					rightEyeState = pair[1];
					refreshImage(rightEye);
				}

				//3. set an await for 0.4s
				await new Promise((awaitResolve) => setTimeout(awaitResolve, 400));
			}

			//4. go to step 1
			//5. repeat until queue is empty -> resolve
			resolve(true);
		}).then(() => {
			expressionAnimationPromise = null;
		});
	};

	const refreshImage = (element) => {
		// wacky code to reload image source to reset css animation concistently
		if (!element) return;

		let timestamp = new Date().getTime();
		let imgURL = element.src.split('?')[0];

		let queryString = '?t=' + timestamp;

		element.src = imgURL + queryString;
	};
</script>

<div class="face">
	<img
		bind:this={leftEye}
		src="img/eye_animations/{$theme}/eye_neutral.svg"
		id="leftEye"
		class="eye"
		alt="eye"
	/>
	<img
		bind:this={rightEye}
		src="img/eye_animations/{$theme}/eye_neutral.svg"
		id="rightEye"
		class="eye"
		alt="eye"
	/>
</div>

<style>
	.eye {
		max-width: 18%;
		margin: 0 auto;
		padding: 4%;
	}
</style>
