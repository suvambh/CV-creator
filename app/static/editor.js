function addFromTemplate(containerId, templateId, emptyNoteId) {
    const container = document.getElementById(containerId);
    const template = document.getElementById(templateId);
    const emptyNote = document.getElementById(emptyNoteId);

    if (!container || !template) return;

    container.appendChild(template.content.cloneNode(true));

    if (emptyNote) {
        emptyNote.style.display = "none";
    }
}

function removeItem(button) {
    const item = button.closest(".repeatable-item");
    if (!item) return;

    const container = item.parentElement;
    item.remove();

    const emptyNoteId = container.id.replace("-list", "-empty");
    const emptyNote = document.getElementById(emptyNoteId);

    if (emptyNote && container.querySelectorAll(".repeatable-item").length === 0) {
        emptyNote.style.display = "block";
    }
}