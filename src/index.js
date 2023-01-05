import WebSocket from 'ws'

const ws = new WebSocket("ws://10.0.0.241:6969/", { perMessageDeflate: false })
ws.onmessage = (event) => {
	console.log(event.data);
}
