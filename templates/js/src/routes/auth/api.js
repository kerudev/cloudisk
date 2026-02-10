export const managerUser = async action => {
    const body = {
        email: document.getElementById("mail").value,
        password: document.getElementById("pass").value,
    };

    if (action == "register") {
        body["username"] = document.getElementById("user").value;
    }

    const response = await fetch(`/auth/${action}`, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json",
        }
    });

    const data = await response.json();
    if (!response.ok) {
        const error = document.getElementById("error");

        error.classList.add("visible");
        error.textContent = data["detail"];
        return false;
    };

    if (action == "login") {
        const expire = new Date();
        const oneWeek = 7 * 24 * 60 * 60 * 1000;
        expire.setTime(expire.getTime() + oneWeek);

        document.cookie = `user=${JSON.stringify(data)}; expires=${expire.toUTCString()}`;
    }

    return true;
}
