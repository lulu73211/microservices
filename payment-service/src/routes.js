const express = require('express');
const Payment = require('./models');
const { publishMessage } = require('./rabbit');

const router = express.Router();

// Créer un paiement
router.post('/', async (req, res) => {
    try {
        const payment = new Payment(req.body);

        // Validation des données
        if (!payment.userId || !payment.subscriptionId || !payment.amount || !payment.paymentDate) {
            return res.status(400).json({ error: 'All fields are required.' });
        }

        await payment.save();

        // Publier un message dans RabbitMQ
        await publishMessage('payment_notifications', { action: 'create', data: payment });

        res.status(201).json(payment);
    } catch (error) {
        console.error('Error creating payment:', error.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Récupérer tous les paiements
router.get('/', async (req, res) => {
    try {
        const payments = await Payment.find();
        res.status(200).json(payments);
    } catch (error) {
        console.error('Error fetching payments:', error.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Mettre à jour le statut d'un paiement
router.put('/:id', async (req, res) => {
    try {
        const payment = await Payment.findByIdAndUpdate(req.params.id, req.body, { new: true });

        if (!payment) {
            return res.status(404).json({ error: 'Payment not found' });
        }

        // Publier une mise à jour dans RabbitMQ
        await publishMessage('payment_notifications', { action: 'update', data: payment });

        res.status(200).json(payment);
    } catch (error) {
        console.error('Error updating payment:', error.message);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
