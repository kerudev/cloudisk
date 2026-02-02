export const input = (params = {}) => {
    const {
        id = "",
        className = "focus:border-indigo-600 focus:outline-2 rounded-lg px-2 py-1 outline outline-offset-4 outline-solid",
        type = "",
        value = "",
        placeholder = "",
        label = "",
    } = params;

    const div = document.createElement("div");
    div.classList.add("grid");

    if (label) {
        const _label = document.createElement("label");
        _label.textContent = label;
        _label.className = "mb-2 font-bold"

        div.appendChild(_label);
    }

    const input = document.createElement("input");

    if (id) input.id = id;
    if (className) input.className = className;
    if (type) input.type = type;
    if (placeholder) input.placeholder = placeholder;
    if (value) input.value = value;

    div.appendChild(input);

    return div;
};
