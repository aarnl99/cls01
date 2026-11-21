/* CLS traffic and conversion tracking (Google Analytics 4).
   Counts page views, quote and program form sends, phone taps and email taps. */
(function () {
  var GA_ID = 'G-XXXXXXXXXX';
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_ID);

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  /* Called by contact.js after a form is stored by Netlify. */
  window.clsTrackForm = function (formName, formLabel) {
    gtag('event', 'generate_lead', {
      form_name: formName || '',
      form_label: formLabel || '',
      page_path: location.pathname
    });
  };

  /* Phone and email taps anywhere on the page. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) {
      gtag('event', 'phone_click', { link_url: href, page_path: location.pathname });
    } else if (href.indexOf('mailto:') === 0) {
      gtag('event', 'email_click', { link_url: href.split('?')[0], page_path: location.pathname });
    }
  }, true);
})();
