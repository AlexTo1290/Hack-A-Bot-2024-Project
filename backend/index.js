// Importing required modules
import express from 'express';
import { apiRouter } from './routes/api.js';
import { run } from './config/db.js';
import dotenv from 'dotenv';
dotenv.config(); 

// Connecting to the database
run().catch(console.dir);

// Creating an Express application
const app = express();

app.use(express.json());

// api router
app.use('/api', apiRouter);


// Starting the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
