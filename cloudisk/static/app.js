const newLink = text => {
    const current = new URLSearchParams(window.location.search);
    const search = Object.fromEntries(current.entries());

    const path = (search?.path)
        ? search.path + "/" + text
        : text;

    const params = new URLSearchParams({ path });

    const a = document.createElement("a");
    a.textContent = text;
    a.href = `?${params.toString()}`;

    const li = document.createElement("li");
    li.appendChild(a);

    return li;
};

window.addEventListener("dragenter", e => e.preventDefault());

window.addEventListener("dragover", e => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
});

window.addEventListener("drop", async e => {
    e.preventDefault();

    const files = [...e.dataTransfer.items].filter(item => item.kind === "file");
    const file = files[0].getAsFile();

    const data = new FormData();
    data.append("file", file);

    const response = await fetch("/files", {
        method: "POST",
        body: data,
        headers: {
            "X-File-Type": file.type,
            "X-File-Name": file.name
        }
    });

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
