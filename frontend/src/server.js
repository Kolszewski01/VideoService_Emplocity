const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

// Handle user registration
app.post('/register', (req, res) => {
    const { username, email, password } = req.body;
    // Implement user registration logic here (e.g., save to a database)
    res.json({ message: 'User registered successfully' });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});