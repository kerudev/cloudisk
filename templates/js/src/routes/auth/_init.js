import { managerUser } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("user-form").addEventListener("submit", e => {
        e.preventDefault();
        managerUser(e.submitter.id);
    })
});
