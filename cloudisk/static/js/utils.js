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

    const li = document.createElement("li");
    li.appendChild(a);

    return li;
};

/**
 * Updates the contents of `body` by generating a new `ul` with the contents of
 * `files`, calling `newLink` on each iteration.
 *
 * @param {string[]} files - List of file names.
 */
export const processFiles = files => {
    const ul = document.createElement("ul");
    files.forEach(file => ul.appendChild(newLink(file)));

    const body = document.querySelector("body");
    body.replaceChildren(ul);
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

    const reader = response.body.getReader();

    const stream = new ReadableStream({
        async start(controller) {
            while (true) {
                const { done, value } = await reader.read();

                if (done) break;

                controller.enqueue(value);
            }

            controller.close();
        },
    });

    const responseStream = new Response(stream);
    const blob = await responseStream.blob();
    const blobUrl = window.URL.createObjectURL(blob);

    const downloader = Object.assign(document.createElement("a"), {
        href: blobUrl,
        download: name,
    });

    downloader.click();

    window.URL.revokeObjectURL(blobUrl);
    downloader.remove();
};

export const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const streamStart = async (controller) => {
    while (true) {
        const { done, value } = await reader.read();
        await delay(200);

        if (done) break;

        controller.enqueue(value);
    }

    controller.close();
}
