import { managerUser } from "./api.js";
import { input } from "../../components.js";
import { files } from "../files/ui.js";

const registerForm = async () => {
    _initAuthForm();

    document.getElementById("auth-form-title").textContent = "Register";

    const submit = document.createElement("button");
    submit.id = "register";
    submit.className = "focus:border-indigo-600 focus:outline-2 rounded-lg px-2 py-1 outline outline-offset-4 outline-solid col-span-2 mt-4";
    submit.type = "submit";
    submit.textContent = "Register";

    const loginFormBtn = submit.cloneNode(true);
    loginFormBtn.id = "login-form-button";
    loginFormBtn.textContent = "Log into an existing account";
    loginFormBtn.addEventListener("click", loginForm);

    const form = document.getElementById("auth-form");
    form.classList.add("grid-cols-2");
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
        loginFormBtn,
    );

    document.getElementById("pass").parentElement.classList.add("col-span-2");

    form.addEventListener("submit", async e => {
        e.preventDefault();

        if (!_validateAuthForm(["user", "mail", "pass"])) return;

        if (await managerUser("register")) loginForm();
    });
};

export const loginForm = async () => {
    _initAuthForm();

    document.getElementById("auth-form-title").textContent = "Login";

    const submit = document.createElement("button");
    submit.id = "login";
    submit.className = "focus:border-indigo-600 focus:outline-2 rounded-lg px-2 py-1 outline outline-offset-4 outline-solid col-span-2 mt-4";
    submit.type = "submit";
    submit.textContent = "Login";

    const registerFormBtn = submit.cloneNode(true);
    registerFormBtn.id = "register-form-button";
    registerFormBtn.textContent = "Create an account";
    registerFormBtn.addEventListener("click", registerForm);

    const form = document.getElementById("auth-form");
    form.classList.add("grid-cols-1");
    form.replaceChildren(
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
        registerFormBtn,
    );

    document.getElementById("mail").parentElement.classList.add("col-span-2");
    document.getElementById("pass").parentElement.classList.add("col-span-2");

    form.addEventListener("submit", async e => {
        e.preventDefault();

        if (!_validateAuthForm(["mail", "pass"])) return;

        await managerUser("verify");
        if (await managerUser("login")) await files();
    });
};

const _initAuthForm = () => {
    const root = document.getElementById("root");
    root.classList.add(
        "grid",
        "place-content-center",
        "h-screen",
        "p-8",
    );

    root.innerHTML = `
    <div class="rounded-lg bg-white p-8">
        <div class="flex place-content-between mb-4">
            <h1 id="auth-form-title" class="font-bold text-2xl"></h1>
            <div id="error" class="bg-red-400 font-bold px-2 py-1 rounded-md invisible"></div>
        </div>

        <form id="auth-form" class="grid gap-4 w-md" method="POST" target="_blank"></form>
    </div>
    `;
};

const _validateAuthForm = (fields) => {
    for (const id of fields) {
        if (!document.getElementById(id).value) {
            const error = document.getElementById("error");

            error.classList.add("visible");
            error.textContent = "Please fill all inputs";
            return false;
        }
    }

    return true;
};
