// Turns each protected email placeholder (templates/includes/protected_email.html)
// into a clickable mailto link. The address is only assembled in the browser,
// so it never appears in full in the HTML served to scrapers.
document.querySelectorAll(".protected-email").forEach(function (placeholder) {
  var address = placeholder.dataset.user + "@" + placeholder.dataset.domain;
  var link = document.createElement("a");
  link.href = "mailto:" + address;
  link.textContent = address;
  placeholder.replaceWith(link);
});
