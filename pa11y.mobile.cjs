const base = require("./pa11y.default.cjs");

module.exports = {
  ...base,
  viewport: {
    width: 320,
    height: 480,
    deviceScaleFactor: 2,
    isMobile: true,
  },
};
