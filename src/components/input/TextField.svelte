<script>
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
	<button class="button" on:click={onSubmit}>
		<img src="/img/icon/send-icon.png" class="send-icon" />
	</button>
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

	.send-icon {
		height: 100%;
	}
	button {
		margin-left: 1rem;
		height: 3.4rem;
		background-color: transparent;
		border: none;
	}
</style>
