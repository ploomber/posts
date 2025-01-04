/*
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License.
 */

const { checkEnvVar } = require("./utils");

var path = require('path');
var express = require('express');
var session = require('express-session');
var createError = require('http-errors');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var usersRouter = require('./routes/users');
var authRouter = require('./routes/auth');

// initialize express
var app = express();

/**
 * Using express-session middleware for persistent user session. Be sure to
 * familiarize yourself with available options. Visit: https://www.npmjs.com/package/express-session
 */
app.use(session({
    secret: checkEnvVar("AUTH_SESSION_SECRET"),
    resave: false,
    saveUninitialized: false,
    cookie: {
        httpOnly: true, // true: Prevents client-side access to cookie
        secure: false, // TODO: set this to true on production
    }
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.use(logger('dev'));
app.use(express.json());
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));


app.use('/users', usersRouter);
app.use('/auth', authRouter);


/* PROXY SETUP */

// setting secure to false since this will proxy to http
const httpProxy = require("http-proxy");
const targetURL = checkEnvVar("DASH_APP_URL");
const proxy = httpProxy.createProxyServer({
    secure: false,
    target: targetURL,
});



app.all('*', async function (req, res, next) {
    if (!req.session.isAuthenticated) {
        return res.redirect('/auth/signin');
    } else {
        proxy.web(req, res);
    }
});


/* END PROXY SETUP */

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

module.exports = { app, proxy };

