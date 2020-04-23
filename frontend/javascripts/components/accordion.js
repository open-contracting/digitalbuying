import { Accordion } from 'govuk-frontend'

// Update "Open all / Close all" button text to include translated versions
Accordion.prototype.updateOpenAllButton = function (expanded) {
  const el = document.querySelector('[data-module="govuk-accordion"]')
  var newButtonText = expanded ? el.getAttribute('data-close-text') : el.getAttribute('data-open-text')
  newButtonText += '<span class="govuk-visually-hidden"> sections</span>'
  this.$openAllButton.setAttribute('aria-expanded', expanded)
  this.$openAllButton.innerHTML = newButtonText
}

exports.Accordion = Accordion
