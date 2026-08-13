const base = require("./pa11y.default.cjs");

const knownWarnings = [
  {
    // "This element is absolutely positioned and the background color can not be determined."
    // https://www.w3.org/WAI/WCAG21/Techniques/general/G18
    // The menu button is only displayed below desktop, so it fires in this config alone.
    // Effective under the hideElements strategy only: ignore already discards these rules globally.
    rules: ["WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Abs", "WCAG2AA.Principle1.Guideline1_4.1_4_3.G145.Abs"],
    selectors: [".ictcg-header__menu-button"],
  },
];

module.exports = {
  ...base,
  defaults: {
    ...base.createDefaults(knownWarnings),
    viewport: {
      width: 320,
      height: 480,
      deviceScaleFactor: 2,
      isMobile: true,
    },
  },
};
