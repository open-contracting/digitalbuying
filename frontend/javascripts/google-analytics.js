export const loadGoogleAnalytics = (gaID) => {
  var ga = document.createElement('script')
  ga.type = 'text/javascript'
  ga.async = true
  ga.src = `https://www.googletagmanager.com/gtag/js?id=${gaID}`
  var s = document.getElementsByTagName('script')[0]
  s.parentNode.insertBefore(ga, s)
}
