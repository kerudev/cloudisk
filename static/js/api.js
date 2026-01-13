import { downloadResponseBlob, processFiles, resolvePath } from "./utils.js";

export const getFiles = async () => {
    const params = new URLSearchParams(window.location.search);

    if (params.get("path") == "..") {
        params.delete("path");

        const query = params.size ? "?" + params.toString() : "";
        history.replaceState(null, "", location.pathname + query);
    }

    const response = await fetch(`/files${params.toString()}`);
    const data = await response.json();

    if (!response.ok) console.error(data.message);

    processFiles(data["files"], data["isRoot"]);
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

    processFiles(data["files"], data["isRoot"]);
}

export const download = async path => {
    const pathParam = resolvePath(path);
    const params = pathParam ? { path: pathParam } : null;

    const urlParams = new URLSearchParams(params);

    const queryParams = params
        ? `?${urlParams.toString()}`
        : '';

    const response = await fetch(`/files${queryParams}`);

    if (response.headers.has("content-disposition")) {
        await downloadResponseBlob(response);
        return;
    }

    const data = await response.json();
    processFiles(data["files"], data["isRoot"]);

    const state = params ? { path } : {};
    history.pushState(state, '', `/${queryParams}`);
    history.pushState(state, '', '/' + queryParams);
}
