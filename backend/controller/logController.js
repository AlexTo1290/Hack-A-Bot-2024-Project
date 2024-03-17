import { Router } from "express";
import { Log } from "../models/log.js";

export const logRouter = Router();

logRouter.get("/", (req, res) => {
    Log.find({}, (err, logs) => {
        if (err) {
            res.status(500).send
            return;
        }
        res.send(logs);
    });
});

logRouter.post("/Taken", (req, res) => {
    const { item_name, message } = req.body;
    const log = new Log(
        {
            item_name: item_name,
            message: message
        });
    log.save((err, log) => {
        if (err) {
            res.status(500).send();
            return;
        }
        res.send(log);
    });
});