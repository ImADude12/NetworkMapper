const DriverConnection = require('../db-driver');

const checkAuth = (req, res, next) => {
    const connection = DriverConnection.getInstance();
    if (connection) {
        DriverConnection.isConnected().then(() => {
            next()
        }).catch((err) => res.status(401).send(err.message))
    } else {
        res.status(401).send("Not Auth")
    }
}
module.exports = checkAuth;