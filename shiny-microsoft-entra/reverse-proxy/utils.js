const cookie = require("cookie");

function checkEnvVar(varName) {
    const envVar = process.env[varName];
    if (!envVar) {
        throw new Error(`Missing environment variable ${varName}`);
    }
    return envVar;
}


module.exports = { checkEnvVar };