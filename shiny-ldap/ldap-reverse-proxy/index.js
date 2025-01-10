const express = require('express');
const session = require('express-session');
const passport = require('passport');
const LdapStrategy = require('passport-ldapauth');
const httpProxy = require('http-proxy');
const flash = require('connect-flash');
const path = require('path');

// Create Express app
const app = express();

// Create a proxy server instance
const proxy = httpProxy.createProxyServer({});

// Target URL to proxy requests to
const targetUrl = 'http://localhost:8501';

// Configure view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: false
}));
app.use(flash());
app.use(passport.initialize());
app.use(passport.session());

// LDAP configuration
const LDAP_CONFIG = {
    server: {
        url: 'ldap://localhost:389',
        bindDN: 'cn=admin,dc=example,dc=com',
        bindCredentials: 'admin',
        searchBase: 'dc=example,dc=com',
        searchFilter: '(uid={{username}})'
    }
};

// Configure passport
passport.use(new LdapStrategy(LDAP_CONFIG));

passport.serializeUser((user, done) => {
    done(null, user.uid);
});

passport.deserializeUser((id, done) => {
    done(null, { uid: id });
});

// Routes
app.get('/login', (req, res) => {
    res.render('login', { messages: req.flash() });
});

app.post('/login', passport.authenticate('ldapauth', {
    successRedirect: '/',
    failureRedirect: '/login',
    failureFlash: 'Invalid username or password.'
}));

app.get('/logout', (req, res) => {
    req.logout(() => {
        res.redirect('/login');
    });
});

// Middleware to check if user is authenticated
const isAuthenticated = (req, res, next) => {
    if (req.isAuthenticated()) {
        return next();
    }
    res.redirect('/login');
};

// Handle WebSocket upgrade requests
const server = app.listen(3000, () => {
    console.log('Reverse proxy listening on port 3000');
});

server.on('upgrade', (req, socket, head) => {
    proxy.ws(req, socket, head, { target: targetUrl });
    // if (req.session && req.session.passport && req.session.passport.user) {
    //     proxy.ws(req, socket, head, { target: targetUrl });
    // } else {
    //     socket.end();
    // }
});

// proxy.on('connect', (req, socket) => {
//     socket.on('error', (err) => {
//         console.error('WebSocket connection error:', err);
//     });
// });

// Proxy all authenticated requests
app.use('/', isAuthenticated, (req, res) => {
    proxy.web(req, res, { target: targetUrl });
});

// Error handling
proxy.on('error', (err, req, res) => {
    console.error('Proxy error:', err);
    res.writeHead(500, {
        'Content-Type': 'text/plain'
    });
    res.end('Proxy error');
});

// Handle proxy events
proxy.on('proxyReq', (proxyReq, req, res) => {
    // You can modify headers here if needed
    proxyReq.setHeader('X-Authenticated-User', req.user.uid);
});
