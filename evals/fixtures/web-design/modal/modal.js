const modal = document.getElementById('confirm');
const overlay = document.getElementById('overlay');

document.querySelectorAll('.delete').forEach((button) => {
  button.addEventListener('click', () => {
    modal.dataset.id = button.dataset.id;
    modal.hidden = false;
    overlay.hidden = false;
  });
});

function closeModal() {
  modal.hidden = true;
  overlay.hidden = true;
}

overlay.addEventListener('click', closeModal);
document.getElementById('confirm-delete').addEventListener('click', async () => {
  await fetch(`/api/projects/${modal.dataset.id}`, { method: 'DELETE' });
  closeModal();
});
