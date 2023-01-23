var s = (elem) => {
  return document.querySelector(elem);
};
var a = (elem) => {
  return document.querySelectorAll(elem);
};
(function () {
  'use strict'
  var tooltipTriggerList = [].slice.call(a('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})();
[].forEach.call(a("a.nav-link"), function(elem) {
  elem.onclick = function() {
    s("a.active").classList.remove("active");
    elem.classList.add("active");
    s("iframe").src = "/log/?display=" + elem.children[0].children[0].getAttribute("xlink:href").slice(1);
  };
});
var inputname = {"bloodpressure":["Systolic","Diastolic","Pulse"],"oximetry":["Oximetry","Pulse"],"temperature":["Temperature"],"glucose":["Glucose"],"medication":["Medicine","Dosage"]};
if (s("button#add")) {
  s("button#add").onclick = () => {
    var type = new URL(window.location.href).searchParams.get("display");
    window.location.href = `/log?form=${type}`;
  };
}
if (s("form#form")) {
  s("form#form").onsubmit = (e) => {
    e.preventDefault();
    var type = new URL(window.location.href).searchParams.get("form");
    newlog = {};
    newlog["date"] = new Date().toString();
    for (i in inputname[type]) {
      newlog[inputname[type][i].toLowerCase()] = s(`input[name='${inputname[type][i].toLowerCase()}']`).value;
    }
    newlog["comment"] = s("input#floatingComment").value;
    window.location.href = `/log?update=${type}&value=${encodeURIComponent(JSON.stringify(newlog))}`;
  };
}
