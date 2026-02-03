import { download, getFiles, upload } from "./api.js";
import { resolvePath } from "./utils.js";

export const files = async () => {
    const button = document.createElement("button");
    button.id = "upload-btn";
    button.classList = "mt-4 ml-4 p-2 bg-stone-400 outline-1 rounded-lg font-bold";
    button.textContent = "Upload file(s)";

    button.addEventListener("click", () => {
        const fileChooser = document.createElement("input");
        fileChooser.id = "upload-input";
        fileChooser.type = "file";
        fileChooser.multiple = true;
        fileChooser.hidden = true;

        fileChooser.addEventListener("change", async () => await upload([...fileChooser.files]));

        fileChooser.click();
    });

    const fileList = document.createElement("div");
    fileList.id = "file-list";
    fileList.className = "w-2xl ml-4 mt-4 rounded-lg";

    document.getElementById("root").replaceChildren(button, fileList);

    await getFiles();
}

/**
 * Creates a new `li` that contains an `a` (anchor) element.
 *
 * When the anchor element is clicked, it will behave differently based on the
 * type of path:
 * - File: downloads the file.
 * - Dir: lists the contents of the directory.
 *
 * @param {string} path - Name of the file.
 *
 * @returns {HTMLLIElement} - List element containing a clickable link.
 */
export const newRow = path => {
    const file = document.createElement("span");
    file.className = "file-name";
    file.textContent = path;

    const downloadButton = document.createElement("span");
    downloadButton.className = "download-icon";

    downloadButton.addEventListener('click', async () => download(path));

    const trashButton = document.createElement("span");
    trashButton.className = "trash-icon";

    trashButton.addEventListener('click', e => rmRow(e.target.closest("tr")));

    fetch("/static/src/assets/download.svg")
        .then(res => res.text())
        .then(svg => downloadButton.innerHTML = svg);

    fetch("/static/src/assets/trash.svg")
        .then(res => res.text())
        .then(svg => trashButton.innerHTML = svg);

    const cells = [file, downloadButton, trashButton].map((cell, idx) => {
        const td = document.createElement("td");

        const container = document.createElement("div");
        container.appendChild(cell);

        td.className = "bg-gray-400 border-b border-gray-100 py-4";
        if (idx == 0) td.classList.add("pl-4");

        td.appendChild(container);

        return td;
    });

    downloadButton.parentElement.classList.add("flex", "items-center", "justify-center");
    trashButton.parentElement.classList.add("flex", "items-center", "justify-center");

    const tr = document.createElement("tr");
    tr.append(...cells);

    return tr;
};

/**
 * Removes a link and its associated file on the backend.
 *
 * @param {HTMLLIElement} link - A list element.
 */
const rmRow = async link => {
    const text = link.querySelector(".file-name").textContent;
    const path = resolvePath(text);

    const response = await fetch(`/files?path=${path}`, { method: "DELETE" });

    if (!response.ok) {
        const data = await response.json();
        throw new Error(data["message"]);
    }

    link.remove();
};
