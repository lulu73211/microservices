const mongoose = require('mongoose');

const PaymentSchema = new mongoose.Schema({
    userId: { type: String, required: true },
    subscriptionId: { type: String, required: true },
    amount: { type: Number, required: true },
    paymentDate: { type: Date, required: true },
}, { timestamps: true });

module.exports = mongoose.model('Payment', PaymentSchema);
