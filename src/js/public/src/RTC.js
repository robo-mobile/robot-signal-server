/** @module RTC */
import {platformSocket} from './platformSocket.js';
import {config} from './rtcConfig.js';

/** Основной класс для управления RTC соединением */
export default class RTC {
  /**
   * Принимает обьект с опциями и структуру для работы с сигнальным сервером
   * @param {Object} options - Обьект опций соединения
   * @param {boolean} options.isControl - Указатель который сообщает это соединение панели управления или платформы
   * @param {Object} signalEmitter - Обьект для работы из сигнальным сервером
   */
  constructor(options, signalEmitter) {
    this.handlers = {};
    this.isControl = options.isControl;
    this.SE = signalEmitter;
    this.platformSocketUri = options.platformSocket;
    this.pc = new RTCPeerConnection(config);

    /* Ф-я навешивает обработчики на экземлпяр RTCPeerConnection */
    pcHandlers(this.pc, this);
    /* Ф-я навешивает обработчики на экземлпяр SignalEmitter */
    seHandlers(this);

    if (options.isControl) {
      this.channel = this.pc.createDataChannel('RTCDataChannel');
      this.channel.onopen = () => this.emit('dataChannel', this.channel);
    } else {
      this.pc.ondatachannel = (e) => {
        this.channel = e.channel;
        this.channel.onmessage = (e) => this._parseControlMessage(e);
        let timerId = setInterval(() => {
          /* Костиль нужен для оповещения что соединение отвалось. Так как событие connectionstatechange не срабатывает
          именно на Raspberry Pi */
          if (this.pc.iceConnectionState === 'disconnected' || this.pc.iceConnectionState === 'failed') {
            clearInterval(timerId);
            timerId = null;
            this.emit('disconnected');
          }
        }, 1000);
      };
    }
  }

  /**
   * Метод для добавления своих обработчиков событий
   */
  on(eventName, handler) {
    if (!this.handlers[eventName]) {
      this.handlers[eventName] = [];
    }
    this.handlers[eventName].push(handler);
  }

  /**
   * Метод для вызова событий
   */
  emit(eventName, ...values) {
    this.handlers[eventName].forEach(fn => fn.apply(this, values));
  }


  /**
   * Процедура устанавливает уточненное описание сеанса
   */
  _setRemoteSDP(sdp) {
    this.pc.setRemoteDescription(new RTCSessionDescription(sdp), () => {
      if(this.pc.remoteDescription.type == 'offer') {
        this.createAnswer();
      }
    }, err => {
      console.log('Failed to setRemoteDescription():', err);
    });
  }

  /**
   * Процедура создает offer и отправляет его через сигнальный сервер
   */
  async createOffer() {
    const offer = await this.pc.createOffer({offerToReceiveVideo: true});
    this.pc.setLocalDescription(offer);
    this.SE.send('SDP', offer);
  }

  /**
   * Процедура создает answer. Устанавливает соединение с веб-сокетом запущеном на localhost платформ
   * и отправляет answer или ошибку через сигнальный сервер
   */
  async createAnswer() {
    try {
      await this._addStream();
      this.platformSocket = await platformSocket(this.platformSocketUri);
      const answer = await this.pc.createAnswer();
      this.pc.setLocalDescription(answer);
      this.SE.send('SDP', answer);
    } catch (err) {
      console.error(err);
      this.SE.send('ERROR', err);
    }
  }

  /**
   * Ф-я получает видео поток и врзвращает его
   * @return {stream} обьект видео потока
   */
  async _addStream() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({video: true, audio: false});
      stream.getTracks().forEach(track => this.pc.addTrack(track, stream));
      return stream;
    } catch (err) {
      console.error(err);
      this.SE.send('ERROR', err);
    }
  }

  /**
   * Процедура парсит полученное через webrtc сообщение и отправляет его себе на ws://localhost
   */
  _parseControlMessage(e) {
    const message = JSON.parse(e.data);
    if(this.platformSocket && this.platformSocket.send) {
      this.platformSocket.send(JSON.stringify(message.data));
    }
  }
}

/**
 * Процедура навешивает обработчики на экземпляр RTCPeerConnection
 * @param {Object} pc - Экземпляр RTCPeerConnection
 * @param {Object} _this - контекст экземпляра нашего класса RTC
 */
function pcHandlers(pc, _this) {
  _this.pc.onicecandidate = evt => {
    if (evt.candidate) _this.SE.send('ICE', evt.candidate);
  };

  _this.pc.onconnection = () => console.log('Connection established');

  _this.pc.addEventListener('track', e => {
    _this.emit('videoStream', e.streams[0]);
  });

  _this.pc.onconnectionstatechange = ev => {
    if (_this.isControl) {
      _this.emit('connectionStateChange', _this.pc.connectionState);
    } else {
      if (['disconnected', 'closed', 'failed'].some(state => _this.pc.connectionState === state)) {
        _this.emit('disconnected');
      }
    }
  };
}

/**
 * Процедура навешивает обработчики на экземпляр SignalEmitter
 * @param {Object} _this - контекст экземпляра нашего класса RTC
 */
function seHandlers(_this) {
  _this.SE.on('SDP', sdp => {
    _this._setRemoteSDP(sdp);
  });
  _this.SE.on('ICE', ice => {
    _this.pc.addIceCandidate(new RTCIceCandidate(ice));
  });
  _this.SE.on('ERROR', err => {
    console.log('ERROR: ', err);
  });
}
