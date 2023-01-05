import WebSocket from 'ws';

const socket = new WebSocket('ws://10.0.0.241:1337/', {
	perMessageDeflate: false
});

socket.onmessage = (event) => {
	console.log(event.data);
};
