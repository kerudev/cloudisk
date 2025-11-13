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

document.addEventListener("DOMContentLoaded", async () => {
    const res = await fetch(`/files/${window.location.search}`);
    const data = await res.json();

    const ul = document.createElement("ul");
    data['files'].forEach(file => ul.appendChild(newLink(file)));

    const body = document.querySelector("body");
    body.appendChild(ul);
});
