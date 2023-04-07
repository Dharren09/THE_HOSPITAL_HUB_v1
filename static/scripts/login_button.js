// JavaScript code to handle dropdown content
      
var dropdownBtn = document.getElementById("dropdown-btn");
var dropdownContent = document.querySelector(".dropdown-content");

dropdownBtn.addEventListener("click", function() {
  dropdownContent.classList.toggle("show");
});

var dropdownLinks = dropdownContent.getElementsByTagName("a");

for (var i = 0; i < dropdownLinks.length; i++) {
  dropdownLinks[i].addEventListener("click", function() {
    dropdownBtn.innerHTML = this.innerHTML;
    document.getElementById("usertype").value = this.innerHTML;
    dropdownContent.classList.remove("show");
  });
}

// JavaScript code to prevent form submission if usertype is not selected
var submitBtn = document.getElementById("submit-btn");

submitBtn.addEventListener("click", function(event) {
  if (document.getElementById("usertype").value == "") {
    event.preventDefault();
    alert("Please select a user type.");
  }
});