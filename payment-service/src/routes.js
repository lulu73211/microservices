const express = require('express');
const Payment = require('./models');
const { publishMessage } = require('./rabbit');

const router = express.Router();

// Créer un paiement
router.post('/payments', async (req, res) => {
    try {
        const payment = new Payment(req.body);
        await payment.save();
        await publishMessage('payment_notifications', { action: 'create', data: payment });
        res.status(201).json(payment);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Récupérer tous les paiements
router.get('/payments', async (req, res) => {
    try {
        const payments = await Payment.find();
        res.status(200).json(payments);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Mettre à jour le statut d'un paiement
router.put('/payments/:id', async (req, res) => {
    try {
        const payment = await Payment.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!payment) return res.status(404).json({ error: 'Payment not found' });
        await publishMessage('payment_notifications', { action: 'update', data: payment });
        res.status(200).json(payment);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
