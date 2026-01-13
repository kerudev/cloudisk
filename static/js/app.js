import { getFiles, upload } from "./api.js";

document.addEventListener("DOMContentLoaded", getFiles);

window.addEventListener("popstate", getFiles);

window.addEventListener("dragenter", e => e.preventDefault());

window.addEventListener("dragover", e => {
    e.preventDefault();
    if (e.dataTransfer) e.dataTransfer.dropEffect = "copy";
});

window.addEventListener("drop", async e => {
    e.preventDefault();

    const files = [...e.dataTransfer.items]
        .filter(item => item.kind === "file")
        .map(item => item.getAsFile());

    await upload(files);
});

const uploader = document.querySelector("#upload-input");

uploader.addEventListener("change", async () => await upload([...uploader.files]));

document.querySelector("#upload-btn")
    .addEventListener("click", () => uploader.click());
