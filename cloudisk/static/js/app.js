import { getFiles, upload } from "./api.js";

window.addEventListener("popstate", getFiles);

window.addEventListener("dragenter", e => e.preventDefault());

window.addEventListener("dragover", e => {
    e.preventDefault();
    if (e.dataTransfer) e.dataTransfer.dropEffect = "copy";
});

window.addEventListener("drop", async e => {
    e.preventDefault();
    await upload(e.dataTransfer.items);
});

document.addEventListener("DOMContentLoaded", getFiles);
