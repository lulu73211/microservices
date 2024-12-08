const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const paymentRoutes = require('./routes');
const { connectRabbitMQ } = require('./rabbit');

const app = express();

// Middleware
app.use(bodyParser.json());
app.use('/api/payments', paymentRoutes); // Monté sur /api/payments

// Connexion à MongoDB
mongoose.connect('mongodb://mongo:27017/payment_service')
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('MongoDB connection error:', err));

// Connexion à RabbitMQ
connectRabbitMQ();

// Lancer le serveur
const PORT = 5003;
app.listen(PORT, () => {
    console.log(`Payment Service running on port ${PORT}`);
});
