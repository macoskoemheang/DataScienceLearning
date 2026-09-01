// Paste this into the "Tests" tab of your POST /api/auth/refresh request in Postman.
// Its Authorization should be set to Bearer {{refresh_token}}.
// On success, it overwrites the environment's access_token with the new one.

const status = pm.response.code;

pm.test("Refresh succeeded", function () {
    pm.expect(status).to.equal(200);
});

if (status === 200) {
    const body = pm.response.json();
    pm.environment.set("access_token", body.access_token);
    console.log("Refreshed access_token saved to environment");
} else {
    console.warn("Refresh failed:", pm.response.text());
}
