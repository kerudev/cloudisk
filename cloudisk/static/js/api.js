import { downloadResponseBlob, processFiles } from "./utils.js";

export const getFiles = async () => {
    const response = await fetch(`/files${window.location.search}`);
    const data = await response.json();

    if (!response.ok) console.error(data.message);

    processFiles(data["files"]);
}

/**
 * Uploads files to the server.
 *
 * @param {File[]} files - Files to upload.
 * @returns {Response} Response received from the backend.
 */
export const upload = async files => {
    const body = new FormData();
    files.forEach(file => body.append("files", file));

    const response = await fetch("/files", { method: "POST", body });
    const data = await response.json();

    if (!response.ok) console.error(data.message);

    processFiles(data["files"]);
}

export const download = async path => {
    const current = new URLSearchParams(window.location.search);
    const search = Object.fromEntries(current.entries());

    const pathParam = (search?.path)
        ? search.path + "/" + path
        : path;

    const params = new URLSearchParams({ path: pathParam });

    const response = await fetch(`/files?${params.toString()}`);

    if (response.headers.has("content-disposition")) {
        await downloadResponseBlob(response);
        return;
    }

    const data = await response.json();
    processFiles(data["files"]);

    history.pushState({ path }, '', `/?${params.toString()}`);
}
