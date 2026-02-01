import { auth } from "./routes/auth/ui.js";
import { parseCookies } from "./utils.js";

if (!("user" in parseCookies())) {
    auth();
}
