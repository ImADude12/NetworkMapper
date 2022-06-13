
const neo4j = require('neo4j-driver');

class DriverConnection {
    constructor(credentials) {
        const { username, password } = credentials;
        const token = neo4j.auth.basic(username, password)
        this.driver = neo4j.driver(
            "neo4j+s://9242d2ae.databases.neo4j.io",
            token
        )
    }

    static isConnected() {
        return new Promise((resolve, reject) => {
            if (this.instance.driver) {
                this.instance.driver.verifyConnectivity()
                    .then(() => resolve())
                    .catch(() => {
                        delete this.instance
                        reject(new Error("unauthorized"))
                    })
            }
            else {
                return reject(new Error("unauthorized"))
            };
        })
    }

    static getInstance(credentials) {
        if (!this.instance) {
            if (!credentials) return null;
            this.instance = new DriverConnection(credentials);
        }
        return this.instance;
    }
}

module.exports = DriverConnection;