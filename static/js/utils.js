import { newLink } from "./ui.js";

/**
 * Updates the contents of `body` by generating a new `ul` with the contents of
 * `files`, calling `newLink` on each iteration.
 *
 * @param {string[]} files - List of file names.
 * @param {boolean} isRoot - Defines if the listed directory is the server root.
 */
export const processFiles = (files, isRoot) => {
    const ul = document.createElement("ul");
    files.forEach(file => ul.appendChild(newLink(file)));

    if (!isRoot) ul.prepend(newLink(".."));

    document.getElementById("root").replaceChildren(ul);
}

/**
 * Processes the `path` query param.
 *
 * @param {string} path - If it's a regular path, it's appended at the end of
 * the previous one. If it's `..`, we take a slug out of the previous path.
 * @returns {string} Resolved path.
 */
export const resolvePath = path => {
    const current = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(current.entries());

    if (!params?.path) return path;

    if (path != "..") return params.path + "/" + path;

    const splitted = params.path.split("/");
    if (splitted.length == 1) return "";

    return splitted.slice(0, -1).join("/");
}

/**
 * Processes the value of the `Content-Disposition` header and returns an UTF-8
 * encoded string.
 *
 * More info: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Disposition
 *
 * @param {string} header - Value of the `Content-Disposition` header.
 * @returns {string} UTF-8 encoded string.
 */
export const processContentDisposition = header => {
    if (header.includes("filename="))
        return header.split("filename=")[1].replaceAll('"', '');

    if (header.includes("filename*=utf-8''"))
        return decodeURIComponent(header.split("filename*=utf-8''")[1]);
}

/**
 * Downloads a file to the client's `downloads` folder.
 *
 * @param {Response} response
 */
export const downloadResponseBlob = async response => {
    const headers = Object.fromEntries(response.headers);
    const name = processContentDisposition(headers["content-disposition"]);

    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);

    const downloader = Object.assign(document.createElement("a"), {
        href: blobUrl,
        download: name,
    });

    downloader.click();

    window.URL.revokeObjectURL(blobUrl);
    downloader.remove();
};
