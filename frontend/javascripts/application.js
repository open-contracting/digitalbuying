
import './polyfills/foreach'
import './polyfills/includes'
import Accordion from './components/accordion'
import Header from './components/header'
import { Button } from 'govuk-frontend'

(function () {
  var $accordions = document.querySelectorAll('[data-module="govuk-accordion"]')

  if ($accordions) {
    $accordions.forEach($accordion => new Accordion($accordion).init())
  }

  var $mainmenu = document.querySelectorAll('[data-module="ictcg-header-mainmenu"]')

  if ($mainmenu) {
    $mainmenu.forEach($mainmenu => new Header($mainmenu).init())
  }

  var $button = document.querySelectorAll('a[role="button"]')

  if ($button) {
    $button.forEach($button => new Button($button).init())
  }
})()
