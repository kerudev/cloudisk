import { download } from "./api.js";

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
export const newLink = path => {
    const a = document.createElement("a");
    a.textContent = path;

    a.addEventListener('click', async () => download(path));

    const trash = document.createElement("span");
    trash.classList.add("trash-icon");

    trash.addEventListener('click', e => rmLink(e.target.closest("li")));

    fetch("/static/src/assets/trash.svg")
        .then(res => res.text())
        .then(svg => trash.innerHTML = svg);

    const li = document.createElement("li");
    li.replaceChildren(trash, a);

    return li;
};

/**
 * Removes a link and its associated file on the backend.
 *
 * @param {HTMLLIElement} link - A list element.
 */
export const rmLink = async link => {
    const text = link.querySelector("a").textContent;
    const path = resolvePath(text);

    const response = await fetch(`/files?path=${path}`, { method: "DELETE" });

    if (!response.ok) {
        const data = await response.json();
        throw new Error(data["message"]);
    }

    link.remove();
};
