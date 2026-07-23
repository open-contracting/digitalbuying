// In CI, PA11Y_INCLUDE_WARNINGS is set along with PA11Y_SUPPRESS_KNOWN_WARNINGS, to allow pa11y to pass.
// In development, set PA11Y_INCLUDE_WARNINGS only, to review warnings manually.
const includeWarnings = "PA11Y_INCLUDE_WARNINGS" in process.env;

// pa11y supports hiding elements or ignoring rules - but not ignoring rules for specific elements.
// So, in development, this configuration can be run using each strategy, to avoid shadowing issues.
const strategy = process.env.PA11Y_STRATEGY;

// Suppress false positive warnings.
const suppressKnownWarnings = "PA11Y_SUPPRESS_KNOWN_WARNINGS" in process.env;

const knownErrors = {
  rules: [],
  selectors: [],
};

const knownWarnings = [
  {
    // "This element is absolutely positioned and the background color can not be determined."
    // https://www.w3.org/WAI/WCAG21/Techniques/general/G18
    rules: ["WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Abs", "WCAG2AA.Principle1.Guideline1_4.1_4_3.G145.Abs"],
    selectors: ["a.govuk-skip-link", ".govuk-visually-hidden"],
  },
  {
    // "This element's text is placed on a background image." (social icons; the real ratio is ~5.2:1, #1d70b8 on #fff)
    // https://www.w3.org/WAI/WCAG21/Techniques/general/G18
    rules: ["WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.BgImage", "color-contrast"],
    selectors: ["a.ictcg-social-links__link"],
  },
  {
    // "This element's text or background contains transparency." (the real ratio is ~5.2:1, #1d70b8 on #fff)
    // https://www.w3.org/WAI/WCAG21/Techniques/general/G18
    // These fire inside .ictcg-more-info-module, whose links can also carry a genuine "color-contrast" error;
    // hiding the element would hide that error too, so these htmlcs review notices are ignored by rule instead.
    rules: ["WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Alpha", "WCAG2AA.Principle1.Guideline1_4.1_4_3.G145.Alpha"],
    selectors: [],
  },
  {
    // "Heading markup should be used if this content is intended as a heading."
    // https://www.w3.org/WAI/WCAG21/Techniques/html/H42
    rules: ["WCAG2AA.Principle1.Guideline1_3.1_3_1.H42"],
    selectors: [".govuk-grid-column-two-thirds .rich-text p", ".govuk-grid-column-two-thirds .govuk-inset-text"],
  },
  {
    // "If this element contains a navigation section, it is recommended that it be marked up as a list."
    // https://www.w3.org/WAI/WCAG21/Techniques/html/H48
    rules: ["WCAG2AA.Principle1.Guideline1_3.1_3_1.H48", "WCAG2AA.Principle1.Guideline1_3.1_3_1.H48.2"],
    selectors: [
      ".ictcg-supports-logos",
      ".ictcg-footer__sponsors-items",
      ".govuk-grid-column-two-thirds .rich-text p",
      ".ictcg-information-banner .rich-text p",
    ],
  },
  {
    // "Img element is marked so that it is ignored by Assistive Technology."
    // https://www.w3.org/WAI/WCAG21/Techniques/html/H67
    rules: ["WCAG2AA.Principle1.Guideline1_1.1_1_1.H67.2"],
    selectors: [".rich-text figure img"],
  },
];

const suppressions = [knownErrors, ...(includeWarnings && suppressKnownWarnings ? knownWarnings : [])];

// A suppression with no selector can't be hidden, so its rules are always ignored, regardless of strategy.
const withoutSelectors = suppressions.filter((suppression) => !suppression.selectors.length);
const withSelectors = suppressions.filter((suppression) => suppression.selectors.length);

const hideElements = strategy === "hideElements" ? withSelectors.flatMap((suppression) => suppression.selectors) : [];
const ignore = [
  ...withoutSelectors.flatMap((suppression) => suppression.rules),
  ...(strategy === "ignore" ? withSelectors.flatMap((suppression) => suppression.rules) : []),
];

module.exports = {
  defaults: {
    runners: ["htmlcs", "axe"],
    levelCapWhenNeedsReview: "warning",
    includeWarnings: includeWarnings,
    ...(hideElements.length ? { hideElements: hideElements.join(", ") } : {}),
    ...(ignore.length ? { ignore: ignore } : {}),
  },
};
