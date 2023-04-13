const addPrescriptionButton = document.getElementById("add-prescription");
const prescriptionsTable = document.getElementById("prescriptions");
const tbody = prescriptionsTable.querySelector("tbody");

addPrescriptionButton.addEventListener("click", () => {
  const newRow = document.createElement("tr");
  newRow.innerHTML = `
    <td contenteditable="true"></td>
    <td contenteditable="true"></td>
    <td contenteditable="true"></td>
    <td contenteditable="true"></td>
    <td contenteditable="true"></td>
  `;
  tbody.appendChild(newRow);
});