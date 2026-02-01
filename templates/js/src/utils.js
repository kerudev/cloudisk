/**
 * Parses the cookies from `document.cookie` into an Object.
 *
 * @returns {Object<string, string>}
 */
export const parseCookies = () => {
    return document.cookie.split("; ").reduce((cookies, cookie) => {
        const [name, value] = cookie.split("=");

        cookies[name] = decodeURIComponent(value);
        return cookies;
    }, {});
};
