import logo from './logo.svg';
// import './App.css';
// import React, {useState} from "react";
//
// function App() {
//   return (
//       <div className="App">
//           <header className="App-header">
//               <img src={logo} className="App-logo" alt="logo"/>
//           </header>
//
//           <p>Adres e-mail</p>
//           <input type="text" name="adress-email" placeholder="Podaj e-mail"/>
//
//     </div>
//   );
// }
//
// export default App;

import React, { useState } from 'react';
import './App.css';

function App() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', username);
        formData.append('email', email);
        formData.append('password', password);

        try {
            const response = await fetch('http://localhost:8000/register', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const responseData = await response.json();
                console.log(responseData);
                // Handle success, e.g., show a success message to the user
            } else {
                // Handle error, e.g., show an error message to the user
                console.error('Registration failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" height={'10px'} />
            </header>
            <form onSubmit={handleSubmit}>
                <p>Username</p>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)}/>
                <p>Email Address</p>
                <input type="text" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <p>Password</p>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
                <br/><br/>
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default App;

