import express from 'express';
import connectDB from './config/db.js';
import { config } from 'dotenv';
import {Log} from './models/logModel.js';
import bodyParser from 'body-parser';

config();

connectDB().catch(err=>console.log(err)); // Connect to the database

const app = express()
const port = 3000

app.use(bodyParser.raw({ type: ["image/jpeg", "image/png"], limit: "100mb" }));

app.listen(port, () => {
  console.log(`Tool registering server on port ${port}`)
});

app.get('/', async (req, res) => {
    const log = Log({
        item_name: "TBD",
        message: "checked In",
    });
    await log.save();
    res.send('Hello World!')
    }
);

app.post("/checkIn", async (req, res) => {
    try {
        const image = req.body;
        const log = Log({
            item_name: "TBD",
            message: "Checked In",
            image: image,
        });
        await log.save();
        res.sendStatus(200);
    } catch (error) {
        console.log(error)
    }
});

app.post("/checkOut", async (req, res) => {
    try {
        const image = req.body;
        const log = Log({
            item_name: "TBD",
            message: "Checked Out",
            image: image,
        });
        await log.save();
        res.sendStatus(200);
    } catch (error) {
        console.log(error)
    }
});