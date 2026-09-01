// Paste this into the "Tests" tab of your POST /api/auth/login request in Postman.
// It reads access_token / refresh_token from the response body and saves them
// into the current Postman environment so other requests can reuse them.

const status = pm.response.code;

pm.test("Login succeeded", function () {
    pm.expect(status).to.equal(200);
});

if (status === 200) {
    const body = pm.response.json();

    pm.environment.set("access_token", body.access_token);
    pm.environment.set("refresh_token", body.refresh_token);

    console.log("Saved access_token and refresh_token to environment");
} else {
    console.warn("Login failed, tokens not saved:", pm.response.text());
}
