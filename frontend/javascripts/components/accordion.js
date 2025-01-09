import { Accordion } from "govuk-frontend";

// Update "Open all / Close all" button text to include translated versions
Accordion.prototype.updateOpenAllButton = function (expanded) {
    const el = document.querySelector('[data-module="govuk-accordion"]');
    this.$openAllButton.setAttribute("aria-expanded", expanded);
    this.$openAllButton.innerHTML = `${expanded ? el.getAttribute("data-close-text") : el.getAttribute("data-open-text")}<span class="govuk-visually-hidden"> sections</span>`;
};

export default Accordion;
