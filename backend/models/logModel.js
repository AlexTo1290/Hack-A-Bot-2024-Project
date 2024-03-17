import { model, Schema } from "mongoose";

const logSchema = new Schema({
    item_name: {
        type: String,
        required: true
    },
    message: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        default: Date.now
    },
    image: {
        type: Buffer,
    }
});

logSchema.prependListener('save', function (next) {
    // set date
    this.date = new Date();
    next();
});

export const Log = model('Log', logSchema);
