class Cookie {
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
    const $form = $module.querySelector('.ictcg-cookie-banner--form')
    if (!$form) {
      return
    }

    $form.addEventListener('submit', this.handleSubmit.bind(this))
  }

  /**
  * An event handler for submit event on $form
  * @param {object} event event
  */
  handleSubmit (event) {
    event.preventDefault()
    const $form = this.$module.querySelector('.ictcg-cookie-banner--form')
    const xhr = new XMLHttpRequest()  /* eslint-disable-line */
    const data = new FormData($form)  /*  eslint-disable-line */

    xhr.addEventListener('load', () => {
      this.$module.classList.add('ictcg-hidden')
    })

    xhr.addEventListener('error', () => {
      console.log('Oops! Something went wrong.')
    })

    xhr.open('POST', $form.action)
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    xhr.send(data)
  }
}

export default Cookie
