
import './polyfills/foreach'
import Accordion from './components/accordion'
import Header from './components/header'

(function () {
  var $accordions = document.querySelectorAll('[data-module="govuk-accordion"]')

  if ($accordions) {
    $accordions.forEach($accordion => new Accordion($accordion).init())
  }

  var $mainmenu = document.querySelectorAll('[data-module="ictcg-header-mainmenu"]')

  if ($mainmenu) {
    $mainmenu.forEach($mainmenu => new Header($mainmenu).init())
  }
})()
