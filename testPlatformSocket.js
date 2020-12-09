const ws = require('ws');

const wss = new ws.Server({ port: 5685 });
wss.on('connection', ws => {
  ws.on('message', message => console.log('M: ', message));
  ws.onclose = () => {console.log('CONNECTED: ');};
});
