const express = require('express');
const Subscription = require('./models');
const { publishMessage } = require('./rabbit');

const router = express.Router();

// Créer un abonnement
router.post('/subscriptions', async (req, res) => {
    try {
        const subscription = new Subscription(req.body);
        await subscription.save();
        await publishMessage('subscription_notifications', { action: 'create', data: subscription });
        res.status(201).json(subscription);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Récupérer tous les abonnements
router.get('/subscriptions', async (req, res) => {
    try {
        const subscriptions = await Subscription.find();
        res.status(200).json(subscriptions);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Mettre à jour un abonnement
router.put('/subscriptions/:id', async (req, res) => {
    try {
        const subscription = await Subscription.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!subscription) return res.status(404).json({ error: 'Subscription not found' });
        await publishMessage('subscription_notifications', { action: 'update', data: subscription });
        res.status(200).json(subscription);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
