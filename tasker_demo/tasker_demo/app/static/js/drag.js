const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

document.addEventListener("DOMContentLoaded", () => {
  let dragging = null;

  // marca itens arrastáveis
  document.querySelectorAll(".draggable").forEach(el => {
    el.addEventListener("dragstart", () => dragging = el);
    el.addEventListener("dragend",   () => dragging = null);
  });

  // listas recebedoras
  document.querySelectorAll(".droplist").forEach(list => {
    list.addEventListener("dragover", e => e.preventDefault());

    list.addEventListener("dragenter", () => list.classList.add("drag-over"));
    list.addEventListener("dragleave", () => list.classList.remove("drag-over"));

    list.addEventListener("drop", async e => {
      e.preventDefault();
      if (!dragging) return;

      // visual
      list.classList.remove("drag-over");
      list.appendChild(dragging);

      // calcula posição e payload
      const items   = Array.from(list.querySelectorAll(".draggable"));
      const position = items.indexOf(dragging);
      const taskId   = dragging.dataset.taskId;
      const status   = list.dataset.status;

      try {
        await axios.patch(`/tasks/${taskId}/move`, { status, position }, {
          headers: { "X-CSRFToken": csrfToken }
        });
      } catch (err) {
        alert("Erro ao mover tarefa");
        console.error(err);
      }
    });
  });
});
