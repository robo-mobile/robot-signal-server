
const SignalEmitter = function(options) {
  const {isControl, signalServer, id} = options;
  this.events = {};
  const url = `${signalServer}${isControl ? '' : 'platform'}?id=${id}`;
  this.connection = new WebSocket(url);
  this.connection.onerror = err => {
    console.log(err);
    console.log(`WebSocket error: ${err}`);
  };
  this.connection.onmessage = e => {
    const {event, data} = JSON.parse(e.data);
    this.emit(event, data);
  }
};

SignalEmitter.prototype.on = function(event, callback) {
  if (this.events[event]) {
    this.events[event].push(callback);
  } else {
    this.events[event] = [callback]
  }
};

SignalEmitter.prototype.emit = function(event, ...data) {
  if (this.events[event]) {
    this.events[event].forEach( fn => fn(...data));
  }
};

SignalEmitter.prototype.send = function(event, data) {
  this.connection.send(JSON.stringify({event, data}));
};

export default SignalEmitter;
