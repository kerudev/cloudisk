import { managerUser } from "./api.js";

export const auth = () => {
    const root = document.getElementById("root");
    root.classList.add(
        "grid",
        "place-content-center",
        "m-8",
    );

    root.innerHTML = `
        <div class="grid gap-y-8 rounded-lg bg-white p-8">
            <a id="register" class="font-bold text-2xl">Register</a>
            <a id="login" class="font-bold text-2xl">Login</a>
        </div>
    `;

    document.querySelector("#register").addEventListener("click", _register);
    document.querySelector("#login").addEventListener("click", _login);
};

const _register = async () => {
    const root = document.getElementById("root");
    root.classList.add(
        "grid",
        "place-content-center",
        "m-8",
    );

    root.innerHTML = `
    <div class="rounded-lg bg-white p-8">
        <div class="flex place-content-between mb-4">
            <h1 class="font-bold text-2xl">Register</h1>
            <div id="error" class="bg-red-400 font-bold px-2 py-1 rounded-md invisible"></div>
        </div>

        <form id="register-form" class="grid grid-cols-2 gap-4 w-md" method="POST" target="_blank"></form>
    </div>
    `;

    const submit = document.createElement("button");
    submit.id = "register";
    submit.className = "focus:border-indigo-600 focus:outline-2 rounded-lg px-2 py-1 outline outline-offset-4 outline-solid col-span-2 mt-4";
    submit.type = "submit";
    submit.textContent = "Register";

    const form = document.getElementById("register-form");
    form.replaceChildren(
        input({
            id: "user",
            placeholder: "myuser",
            label: "Username",
        }),
        input({
            id: "mail",
            placeholder: "example@email.com",
            type: "email",
            label: "Email",
        }),
        input({
            id: "pass",
            type: "password",
            placeholder: "Super secret password!",
            label: "Password",
        }),
        submit,
    );

    document.getElementById("pass").parentElement.classList.add("col-span-2");

    form.addEventListener("submit", async e => {
        e.preventDefault();

        for (const id of ["user", "mail", "pass"]) {
            if (!document.getElementById(id).value) {
                const error = document.getElementById("error");

                error.classList.add("visible");
                error.textContent = "Please fill all inputs";
                return;
            }
        }

        await managerUser("register");
    });
};

const _login = async () => {
    document.getElementById("root").innerHTML = `
        <form id="login-form">
            <input type="text" placeholder="user" id="user" value="user">
            <input type="text" placeholder="mail" id="mail" value="mail">
            <input type="password" placeholder="pass" id="pass" value="pass">
            <input type="submit" value="Login" id="login" value="login">
        </form>
    `;

    document.getElementById("login-form").addEventListener("submit", async e => {
        e.preventDefault();
        await managerUser("login");
    });
};

const input = (params = {}) => {
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
