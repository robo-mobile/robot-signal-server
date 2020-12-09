const url = require('url');
const path = require('path');
const fs = require('fs');
const { trim } = require('./functions.js');

const routeParser = (req, res) => {
  const urlParams = url.parse(req.url, true);
  const urlPath = trim(urlParams.pathname, '/');
  const query = urlParams.query;
  let html = '';

  switch (urlPath) {
    case 'platform':
      html = fs.readFileSync(path.join(__dirname, './public/platform.html'), 'utf8');
      break;
    case '':
      html = fs.readFileSync(path.join(__dirname, './public/control.html'), 'utf8');
      break;
    default:
      return false;
  }
  res.writeHeader(200, {"Content-Type": "text/html"});
  res.write(html);
  res.end();
  return true;
}

module.exports = routeParser;
