class Header {
  constructor ($module) {
    this.$module = $module
  }

  init () {
    // Check for module
    const $module = this.$module
    if (!$module) {
      return
    }

    // Check for button
    const $toggleButton = $module.querySelector('.ictcg-js-header-toggle')
    if (!$toggleButton) {
      return
    }

    // Handle $toggleButton click events
    $toggleButton.addEventListener('click', this.handleClick.bind(this))

    const $menuitems = $module.querySelectorAll('.ictcg-header__navigation-item')
    if ($menuitems.length > 0) {
      this.setActiveNavItem($menuitems)
    }
  }

  /**
  * set active item
  * @param {object} nodelist elements
  */
  setActiveNavItem ($nodelist) {
    for (const $item of $nodelist) {
      const navLink = $item.getElementsByTagName('a')[0].getAttribute('href')

      if (window.location.pathname.includes(navLink)) {
        $item.classList.add('ictcg-header__navigation-item--active')
      }
    }
  }

  /**
  * Toggle class
  * @param {object} node element
  * @param {string} className to toggle
  */
  toggleClass (node, className) {
    if (node.className.indexOf(className) > 0) {
      node.className = node.className.replace(` ${className}`, '')
    } else {
      node.className += ` ${className}`
    }
  }

  /**
  * An event handler for click event on $toggleButton
  * @param {object} event event
  */
  handleClick (event) {
    const $module = this.$module
    const $toggleButton = event.target || event.srcElement
    const $target = $module.querySelector(`#${$toggleButton.getAttribute('aria-controls')}`)

    // If a button with aria-controls, handle click
    if ($toggleButton && $target) {
      this.toggleClass($target, 'ictcg-header__navigation--open')
      this.toggleClass($toggleButton, 'ictcg-header__menu-button--open')

      $toggleButton.setAttribute('aria-expanded', $toggleButton.getAttribute('aria-expanded') !== 'true')
      $target.setAttribute('aria-hidden', $target.getAttribute('aria-hidden') === 'false')
    }
  }
}

export default Header
