// Replace this code with your server-side script that fetches the notifications
var notifications = [
    "You have an appointment with Abdul Rauf on April 20, 2023 at 2:00 PM.",
    "New patient Renish Okago has been added to your patient list.",
    "You have received a new test result for Kisembo Ivan."
];

// Get the notification list element
var notificationList = document.getElementById("notification-list");

// Clear the existing notifications
notificationList.innerHTML = "";

// Loop through the notifications and add them to the list
for (var i = 0; i < notifications.length; i++) {
    var notification = notifications[i];

    var li = document.createElement("li");

    var icon = document.createElement("span");
    icon.className = "notification-icon";
    icon.innerHTML = '<i class="fas fa-bell"></i>';
    li.appendChild(icon);

    var text = document.createElement("span");
    text.className = "notification-text";
    text.innerText = notification;
    li.appendChild(text);

    notificationList.appendChild(li);
}