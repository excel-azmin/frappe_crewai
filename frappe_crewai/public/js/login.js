document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
  
    if (form) {
      form.addEventListener("submit", function (e) {
        const username = form.querySelector('input[name="usr"]').value;
        const password = form.querySelector('input[name="pwd"]').value;
  
        if (!username || !password) {
          e.preventDefault();
          alert("Please enter both username and password.");
        }
      });
    }
  });
  