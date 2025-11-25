const newLink = text => {
    const current = new URLSearchParams(window.location.search);
    const search = Object.fromEntries(current.entries());

    const path = (search?.path)
        ? search.path + "/" + text
        : text;

    const params = new URLSearchParams({ path });

    const a = document.createElement("a");
    a.textContent = text;
    a.addEventListener('click', async e => {
        e.preventDefault();

        const res = await fetch(`/files?${params.toString()}`);
        await downloadResponseBlob(res);
    })

    const li = document.createElement("li");
    li.appendChild(a);

    return li;
};

/**
 * Processes the value of the `Content-Disposition` header and returns an UTF-8
 * encoded string.
 *
 * More info: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Disposition
 *
 * @param {string} header - Value of the `Content-Disposition` header.
 * @returns {string} UTF-8 encoded string.
 */
const processContentDisposition = header => {
    if (header.includes("filename="))
        return header.split('filename=')[1].replaceAll('"', '');

    if (header.includes("filename*=utf-8''"))
        return decodeURIComponent(header.split("filename*=utf-8''")[1]);
}

const downloadResponseBlob = async response => {
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);

    const headers = Object.fromEntries(response.headers);
    const name = processContentDisposition(headers['content-disposition']);

    const downloader = Object.assign(document.createElement('a'), {
        href: blobUrl,
        download: name,
    });

    downloader.click();

    window.URL.revokeObjectURL(blobUrl);
};

window.addEventListener("dragenter", e => e.preventDefault());

window.addEventListener("dragover", e => {
    e.preventDefault();
    if (e.dataTransfer) e.dataTransfer.dropEffect = 'copy';
});

window.addEventListener("drop", async e => {
    e.preventDefault();

    const files = [...e.dataTransfer.items].filter(item => item.kind === "file").map(file => file.getAsFile());

    const data = new FormData();
    files.forEach(file => data.append("files", file));

    const response = await fetch("/files", { method: "POST", body: data });
    const result = await response.json();

    if (!result.ok) console.error(result.message);

    window.location.reload();
});

document.addEventListener("DOMContentLoaded", async () => {
    const res = await fetch(`/files${window.location.search}`);
    const data = await res.json();

    const ul = document.createElement("ul");
    data['files'].forEach(file => ul.appendChild(newLink(file)));

    const body = document.querySelector("body");
    body.appendChild(ul);
});
