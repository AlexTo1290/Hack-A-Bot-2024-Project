import { Schema, model } from 'mongoose';

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
    }
});

export const Log = model('Log', logSchema);