export const managerUser = async action => {
    const response = await fetch(`/auth/${action}`, {
        method: "POST",
        body: JSON.stringify({
            username: document.getElementById("user").value,
            email: document.getElementById("mail").value,
            password: document.getElementById("pass").value,
        }),
        headers: {
            "Content-Type": "application/json",
        }
    });

    const body = await response.json();
    if (!response.ok) {
        const error = document.getElementById("error");

        error.classList.add("visible");
        error.textContent = body["detail"]
    };

    const expire = new Date();
    const oneWeek = 7 * 24 * 60 * 60 * 1000;
    expire.setTime(expire.getTime() + oneWeek);

    document.cookie = `user=${JSON.stringify(body)}; expires=${expire.toUTCString()}`;
}
