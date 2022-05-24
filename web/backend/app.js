const express = require('express');
const path = require('path');
const logger = require('morgan');
const bodyParser = require('body-parser');
const cors = require('cors')
const neo4j = require('neo4j-driver')
// const { neo4jConfig } = require('./neo4j-config')

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


let driver;

app.post('/auth', (req, res) => {
    const { username, password } = req.body.credentials;
    const token = neo4j.auth.basic(username, password)
    driver = neo4j.driver(
        "neo4j+s://9242d2ae.databases.neo4j.io:7687",
        token
    )
    driver.verifyConnectivity()
        .then((response) => res.send(response))
        .catch(() => {
            res.status(401).send('Unauthorized!')
        })
})


app.get('/', (req, res) => {
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
