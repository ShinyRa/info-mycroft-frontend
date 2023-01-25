<script>
	// import Microphone from './Microphone.svelte';

	export let onFocus;
	export let onFocusOut;
	export let value;
	export let onSubmit;
</script>

<div class="field">
	<input
		class="input is-large is-rounded"
		type="text"
		bind:value
		placeholder="What is the time?"
		on:focus={() => onFocus()}
		on:focusout={() => onFocusOut()}
	/>
	<button class="button is-primary" on:click={onSubmit}> Send </button>
</div>

<style>
	.field {
		justify-content: center;
		align-items: center;
		display: flex;
	}
	input {
		max-width: 50rem;
	}
	button {
		margin-left: 3rem;
		height: 3rem;
	}
</style>
