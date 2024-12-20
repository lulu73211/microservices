const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const subscriptionRoutes = require('./routes');
const { connectRabbitMQ } = require('./rabbit');

const app = express();

// Middleware
app.use(bodyParser.json());
app.use('/api', subscriptionRoutes);

// Connexion à MongoDB
mongoose.connect('mongodb://mongo:27017/subscription_service', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('MongoDB connection error:', err));

// Connexion à RabbitMQ
connectRabbitMQ();

// Lancer le serveur
const PORT = 5002;
app.listen(PORT, () => {
    console.log(`Subscription Service running on port ${PORT}`);
});
