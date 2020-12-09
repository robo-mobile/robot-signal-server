
const trim = (str, chars) => str.split(chars).filter(Boolean).join(chars);

module.exports = {
  trim
}
