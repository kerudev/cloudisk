const newLink = text => {
    const a = document.createElement("a");
    a.textContent = text;
    a.href = text;

    const li = document.createElement("li");
    li.appendChild(a);

    return li;
};

document.addEventListener("DOMContentLoaded", async () => {
    const res = await fetch("/files");
    const data = JSON.parse(await res.text());

    const ul = document.createElement("ul");
    data.forEach(a => ul.appendChild(newLink(a)));

    const body = document.querySelector("body");
    body.appendChild(ul);
});
