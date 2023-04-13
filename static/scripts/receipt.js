const paymentForm = document.getElementById('payment-form');
const submitButton = paymentForm.querySelector('[name="submit-button"]');

function submitAndRedirect() {
  // Get the form values
  const name = paymentForm.querySelector('[name="name"]').value;
  const email = paymentForm.querySelector('[name="email"]').value;
  const phoneNumber = paymentForm.querySelector('[name="phone"]').value;
  const countryCode = paymentForm.querySelector('[name="country-code"]').value;
  const address = paymentForm.querySelector('[name="address"]').value;
  const reason = paymentForm.querySelector('[name="reason"]').value;
  const amountBilled = paymentForm.querySelector('[name="amount-billed"]').value;
  const amountPaid = paymentForm.querySelector('[name="amount-paid"]').value;
  const paymentMethod = paymentForm.querySelector('[name="payment-method"]').value;
  const date = paymentForm.querySelector('[name="date"]').value;
  const insuranceId = paymentForm.querySelector('[name="insurance-id"]').value;
    
  // Store the form values in localStorage
  localStorage.setItem('name', name);
  localStorage.setItem('email', email);
  localStorage.setItem('phoneNumber', phoneNumber);
  localStorage.setItem('countryCode', countryCode);
  localStorage.setItem('address', address);
  localStorage.setItem('reason', reason);
  localStorage.setItem('amountBilled', amountBilled);
  localStorage.setItem('amountPaid', amountPaid);
  localStorage.setItem('paymentMethod', paymentMethod);
  localStorage.setItem('date', date);
  localStorage.setItem('insuranceId', insuranceId);

  // Redirect the user to the receipt page
  window.location.href = '../templates/receipt.html';
}

submitButton.addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the form from submitting
  submitAndRedirect(); // Call the function to submit the form and redirect
});