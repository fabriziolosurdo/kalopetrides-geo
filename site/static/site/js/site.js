/* kalopetrideslaw.com — progressive enhancement only. Everything on the site works without this file. */
(function () {
  "use strict";

  // Mobile navigation
  var burger = document.querySelector(".burger");
  var mnav = document.getElementById("mnav");
  if (burger && mnav) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      mnav.hidden = open;
    });
  }

  // Contact form → Web3Forms, with mailto fallback (same provider and key as the previous site)
  var form = document.querySelector("[data-contact-form]");
  if (!form) return;
  var status = form.querySelector(".form__status");
  var email = status ? status.getAttribute("data-email") : "";

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (form.querySelector('[name="website"]').value) return; // honeypot
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    setStatus("sending", status.getAttribute("data-sending"));
    fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.success) { setStatus("ok", status.getAttribute("data-success")); form.reset(); }
        else { fail(); }
      })
      .catch(fail)
      .finally(function () { btn.disabled = false; });
  });

  function fail() {
    setStatus("err", status.getAttribute("data-error") + " " + email + ".");
    var m = form.querySelector('[name="message"]').value;
    var n = form.querySelector('[name="name"]').value;
    status.innerHTML += ' <a href="mailto:' + email + "?subject=" + encodeURIComponent("Enquiry from " + n) + "&body=" + encodeURIComponent(m) + '">' + email + "</a>";
  }
  function setStatus(cls, text) {
    status.className = "form__status " + cls;
    status.textContent = text;
  }
})();
