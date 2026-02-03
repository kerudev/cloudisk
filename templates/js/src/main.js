import { loginForm } from "./routes/auth/ui.js";
import { files } from "./routes/files/ui.js";
import { parseCookies } from "./utils.js";

if (!("user" in parseCookies())) {
    loginForm();
} else {
    files();
}
