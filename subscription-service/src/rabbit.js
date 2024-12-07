const amqplib = require('amqplib');

let channel;

const connectRabbitMQ = async () => {
    try {
        const connection = await amqplib.connect('amqp://rabbitmq');
        channel = await connection.createChannel();
        console.log('Connected to RabbitMQ');
    } catch (error) {
        console.error('RabbitMQ connection error:', error);
    }
};

const publishMessage = async (queue, message) => {
    try {
        if (!channel) throw new Error('RabbitMQ channel not initialized');
        await channel.assertQueue(queue);
        channel.sendToQueue(queue, Buffer.from(JSON.stringify(message)));
        console.log(`Message sent to queue ${queue}:`, message);
    } catch (error) {
        console.error('Error publishing message:', error);
    }
};

module.exports = { connectRabbitMQ, publishMessage };
