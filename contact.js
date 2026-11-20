/* CLS contact: turns the quote and request forms into a ready-to-send email to res@clsgt.com.
   There is no form backend, so nothing is stored or sent by the website itself. */
(function () {
  var TO = 'res@clsgt.com';
  function fieldLabel(el) {
    var group = el.closest('.form-group');
    if (group) { var l = group.querySelector('label'); if (l) return l.textContent.trim(); }
    if (el.tagName === 'SELECT' && el.options.length && el.options[0].disabled) return el.options[0].textContent.trim();
    return (el.getAttribute('placeholder') || el.name || 'Info').trim();
  }
  window.clsMailForm = function (target, subject) {
    var box = target;
    if (target && target.preventDefault) { target.preventDefault(); box = target.target; }
    var lines = [];
    box.querySelectorAll('input, select, textarea').forEach(function (el) {
      if (el.type === 'hidden' || el.type === 'submit' || el.name === 'bot-field') return;
      var v = (el.value || '').trim();
      if (v) lines.push(fieldLabel(el) + ': ' + v);
    });
    var body = 'Hi CLS team,\n\n' + (lines.length ? lines.join('\n') : '') + '\n\nThanks!';
    window.location.href = 'mailto:' + TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    var note = box.querySelector('.cls-mail-note');
    if (note) note.style.display = 'block';
    return false;
  };
})();
