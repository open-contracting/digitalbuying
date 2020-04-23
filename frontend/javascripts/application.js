
import { Accordion } from './components/accordion'

(function () {
  var $accordions = document.querySelectorAll('[data-module="govuk-accordion"]')

  if ($accordions) {
    $accordions.forEach($accordion => new Accordion($accordion).init())
  }
})()
