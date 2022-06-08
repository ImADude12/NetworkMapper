const express = require('express');
const path = require('path');
const logger = require('morgan');
const bodyParser = require('body-parser');
const cors = require('cors')
const checkAuth = require('./middleware/checkAuth');
const DriverConnection = require('./db-driver');
//Express instance
const app = express();
const http = require('http').createServer(app)

// Express App Config   
app.use(bodyParser.json())
app.use(logger('dev'))

if (process.env.NODE_ENV === 'production') {
    //Static folder for assets
    app.use(express.static('public'))
} else {
    //Allow Cors
    const corsOptions = {
        origin: ['http://127.0.0.1:8080', 'http://localhost:8080', 'http://127.0.0.1:3000', 'http://localhost:3000', 'http://localhost:3030'],
        credentials: true

    }
    app.use(cors(corsOptions))
}



app.post('/auth', (req, res) => {
    const { credentials } = req.body;
    DriverConnection.getInstance(credentials);
    DriverConnection.isConnected()
        .then(() => res.send())
        .catch((err) => {
            res.status(401).end()
        })
})

app.post('/logout', (req, res) => {
    const DriverInstance = DriverConnection.getInstance();
    if (!DriverInstance) res.end();
    const driver = DriverInstance.driver;
    if (driver)
        driver.close().then(() => {
            res.end()
        });
    else
        res.end()
})



app.get('/scan', checkAuth, (req, res) => {
    const DriverInstance = DriverConnection.getInstance();
    const driver = DriverInstance.driver
    const session = driver.session()
    const nodes = [];
    const links = [];
    session.run("MATCH (n) RETURN n LIMIT 25")
        .then(({ records }) => {
            records.map((node) => {
                const { properties, labels, identity } = node.get('n')
                const nodeToInsert = {
                    id: identity['low'],
                    os: properties.os,
                    ip: properties.ip,
                    //     // mac: properties.mac,
                    type: labels[0]
                }
                nodes.unshift(nodeToInsert)
            })
            const session = driver.session()
            session.run(`MATCH (m)-->(n) RETURN id(m),id(n)`).then(({ records }) => {
                const source = records[0].get('id(m)')['low'];
                const target = records[0].get('id(n)')['low'];
                links.push({
                    source, target
                })
                res.send({ nodes, links })
            }).then(() => session.close())
        }).then(() => session.close())
})



const port = process.env.PORT || 3030
http.listen(port, () => {
    console.log('Server is running on port: ' + port)
})