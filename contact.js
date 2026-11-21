/* CLS forms: sends quote, program and job forms to Netlify Forms without leaving the page.
   Each entry is stored in Netlify and posted to the CLS Slack channel. */
(function () {
  function show(form, text, ok) {
    var el = form.querySelector('.cls-form-status');
    if (!el) return;
    el.textContent = text;
    el.style.display = 'block';
    el.style.fontWeight = ok ? '600' : '400';
  }
  window.clsSendForm = function (event) {
    event.preventDefault();
    var form = event.target;
    var btn = form.querySelector('button[type="submit"]');
    var label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
    var data = new FormData(form);
    if (!data.get('form-name')) data.append('form-name', form.getAttribute('name'));
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(data).toString()
    }).then(function (res) {
      if (!res.ok) throw new Error('status ' + res.status);
      if (window.clsTrackForm) {
        var lbl = data.get('form_label');
        window.clsTrackForm(form.getAttribute('name'), lbl ? String(lbl) : '');
      }
      form.reset();
      show(form, 'Thanks! We got it and will be in touch soon.', true);
    }).catch(function () {
      show(form, 'Sorry, that did not go through. Please call 650.460.8778 or email res@clsgt.com.', false);
    }).finally(function () {
      if (btn) { btn.disabled = false; btn.textContent = label; }
    });
    return false;
  };
})();
