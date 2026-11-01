const form = document.getElementById('checkout');
const submit = document.getElementById('submit');
const errors = document.getElementById('errors');

// Validate a field when the user leaves it, after they have typed something.
form.addEventListener('focusout', (event) => {
  const field = event.target;
  if (field.value) field.classList.toggle('invalid', !field.value.trim());
});

form.addEventListener('input', () => {
  submit.disabled = [...form.querySelectorAll('[placeholder$="*"]')].some((f) => !f.value.trim());
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const response = await fetch(form.action, { method: 'POST', body: new FormData(form) });
  if (!response.ok) {
    const { messages } = await response.json();
    errors.innerHTML = messages.map((m) => `<p style="color:red">${m}</p>`).join('');
    // Password rules come back from the server, e.g. "Password needs 12+ characters and a number".
    form.reset();
  }
});
