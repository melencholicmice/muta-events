import React, { useState } from "react";
import { TextField, Button, Container, Box } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { API_URL } from "../config";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        setEmailError(false);
        setPasswordError(false);

        if (email === '') {
            setEmailError(true);
        }
        if (password === '') {
            setPasswordError(true);
        }
        
        if (email && password) {
            fetch(`${API_URL}/user/sign-in`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            })
            .then(response => {
                if (response.status === 200) {
                    return response.json().then(data => ({ status: response.status, data }));
                } else {
                    return response.json().then(data => ({ status: response.status, data }));
                }
            })
            .then(({ status, data }) => {
                if (status === 200) {
                    console.log('Success:', data);
                    toast.success('Login successful!');
                    localStorage.setItem('token', data.token);
                    navigate('/profile');
                } else {
                    console.log(data.message)
                    throw new Error(`Login failed, ${data.message}`);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                toast.error(`${error}`);
            });
        }
    };

    return (
        <Container maxWidth="sm">
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <h2>Login Form</h2>

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email"
                    name="email"
                    autoComplete="email"
                    autoFocus
                    onChange={e => setEmail(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    type="email"
                    value={email}
                    error={emailError}
                    helperText={emailError ? "Email is required" : ""}
                />

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    onChange={e => setPassword(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={password}
                    error={passwordError}
                    helperText={passwordError ? "Password is required" : ""}
                />

                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="secondary"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Login
                </Button>
            </Box>
        </Container>
    );
};

export default Login;