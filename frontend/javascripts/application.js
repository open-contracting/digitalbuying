import { Button } from "govuk-frontend";
import Accordion from "./components/accordion";
import Header from "./components/header";

(() => {
    const $accordions = document.querySelectorAll('[data-module="govuk-accordion"]');

    if ($accordions) {
        for (const item of $accordions) {
            new Accordion(item).init();
        }
    }

    const $mainmenus = document.querySelectorAll('[data-module="ictcg-header-mainmenu"]');

    if ($mainmenus) {
        for (const item of $mainmenus) {
            new Header(item).init();
        }
    }

    const $buttons = document.querySelectorAll('a[role="button"]');

    if ($button) {
        for (const item of $buttons) {
            new Button(item).init();
        }
    }
})();
