const express = require('express');
const path = require('path');
const logger = require('morgan');
const bodyParser = require('body-parser');
const cors = require('cors')
const neo4j = require('neo4j-driver')
const { neo4jConfig } = require('./neo4j-config')

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


const driver = neo4j.driver(
    neo4jConfig.uri,
    neo4j.auth.basic(neo4jConfig.credentials.username, neo4jConfig.credentials.password)
)
const session = driver.session()


app.get('/', (req, res) => {
    res.send('Hello world')
    session.run("CREATE (n:Person {name: 'Dudi', title: 'Developer'})")
        .then((res) => {
            console.log(res);
            session.close
        })
        .catch((res) => {
            console.log(res);
            session.close
        })
})

const port = process.env.PORT || 3030
http.listen(port, () => {
    console.log('Server is running on port: ' + port)
})
