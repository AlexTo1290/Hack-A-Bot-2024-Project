const express = require('express')
const app = express()
const port = 3000

var bodyParser = require('body-parser');

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Tool registering server on port ${port}`)
})

app.post("/checkInItem",
 bodyParser.raw({ type: ["image/jpeg", "image/png"], limit: "100mb" }),
 (req, res) => {
 console.log(req.body);
 res.sendStatus(200);
 });