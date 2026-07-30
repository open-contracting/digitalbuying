const base = require("./pa11y.default.cjs");

module.exports = {
  defaults: {
    ...base.defaults,
    viewport: {
      width: 320,
      height: 480,
      deviceScaleFactor: 2,
      isMobile: true,
    },
  },
};
