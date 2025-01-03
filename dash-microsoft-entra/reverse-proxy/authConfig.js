/**
 * Configuration object to be passed to MSAL instance on creation.
 * For a full list of MSAL Node configuration parameters, visit:
 * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-node/docs/configuration.md
 */
const { checkEnvVar } = require("./utils");

const CLIENT_ID = checkEnvVar("AUTH_CLIENT_ID");
const CLIENT_SECRET = checkEnvVar("AUTH_CLIENT_SECRET");
const CLOUD_INSTANCE = checkEnvVar("AUTH_CLOUD_INSTANCE");
const TENANT_ID = checkEnvVar("AUTH_TENANT_ID");
const REDIRECT_URI = checkEnvVar("AUTH_REDIRECT_URI");
const POST_LOGOUT_REDIRECT_URI = checkEnvVar("AUTH_POST_LOGOUT_REDIRECT_URI");
const GRAPH_API_ENDPOINT = checkEnvVar("AUTH_GRAPH_API_ENDPOINT");


const msalConfig = {
    auth: {
        clientId: CLIENT_ID, // 'Application (client) ID' of app registration in Azure portal - this value is a GUID
        authority: CLOUD_INSTANCE + TENANT_ID, // Full directory URL, in the form of https://login.microsoftonline.com/<tenant>
        clientSecret: CLIENT_SECRET // Client secret generated from the app registration in Azure portal
    },
    system: {
        loggerOptions: {
            loggerCallback(loglevel, message, containsPii) {
                console.log(message);
            },
            piiLoggingEnabled: false,
            logLevel: 3,
        }
    }
}

const GRAPH_ME_ENDPOINT = GRAPH_API_ENDPOINT + "v1.0/me";

module.exports = {
    msalConfig,
    REDIRECT_URI,
    POST_LOGOUT_REDIRECT_URI,
    GRAPH_ME_ENDPOINT
};
