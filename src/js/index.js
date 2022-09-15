const http = require('http');
const https = require('https');
const static = require('node-static');
const ws = require('ws');
const fs = require('fs');
const url = require('url');
const routeParser = require('./routeParser');
const { trim } = require('./functions');
const { PLATFORM, CONTROL } = require('./constants.js');

const file = new(static.Server)('./public');

/**
 * @description - Здесь храним websocket'ы доступные по ключам
 * connections[id][DEVICE] где id - идентификатор платформы (4 цифры), а DEVICE - указатель на то
 * является ли сокет платформы или панелью управления
 */
connections = {

  set(device, id, ws) {
    if (!this[id]) this[id] = {};
    this[id][device] = ws;
  },
  unset(device, id) {
    try {
      delete this[id][device];
      if (!Object.keys(this[id]).length) delete this[id];
    } catch (err) {
      console.log(err);
    }
  }
};

// SSL
const options = {
  key: fs.readFileSync('./ssl/private.key', 'utf8'),
  cert: fs.readFileSync('./ssl/certificate.crt', 'utf8'),
  ca: fs.readFileSync('./ssl/ca_bundle.crt', 'utf8'),
};

// Создаем http сервер
const httpsServer = https.createServer(options, function (req, res) {
  if (routeParser(req, res)) return;
  file.serve(req, res);
}).listen(2999); //the server object listens on port 8080

// Создаем ws сервер
const wss = new ws.Server({ server: httpsServer });

const connectionHandler = (ws, req) => {
  const parsedURL = url.parse(req.url, true);
  const {id} = parsedURL.query;
  const device = trim(parsedURL.pathname, '/') === PLATFORM ? PLATFORM : CONTROL;
  if (device === PLATFORM) {
    connections.set(PLATFORM, id, ws);
  } else {
    connections.set(CONTROL, id, ws);
  }
  console.log(connections);
  ws.on('message', message => messageHandler(id, device, message, ws));
  ws.onclose = () => {
    connections[id][device].send('DISCONNECT');
    connections.unset(device, id);
    console.table(connections);
  };
}

wss.on('connection', connectionHandler);

//ф-я обработчик для полученых сообщений
const messageHandler = (id, device, message, ws) => {
  const socket = connections[id][device === PLATFORM ? CONTROL : PLATFORM];
  if (socket) socket.send(message);
};
