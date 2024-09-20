import React, { useRef, useState } from "react";
import { TextField, Button, Container, Box } from "@mui/material";
import { Link } from "react-router-dom";
import { API_URL, RECAPTCHA_SITE_KEY } from "../config";
import { toast } from 'react-toastify';
import ReCAPTCHA from "react-google-recaptcha";
import 'react-toastify/dist/ReactToastify.css';


const SignUpForm = () => {
    const recaptchaRef = useRef();
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstNameError, setFirstNameError] = useState(false);
    const [lastNameError, setLastNameError] = useState(false);
    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const [recaptchaValue, setRecaptchaValue] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();

        // const recaptchaValue = await recaptchaRef.current.executeAsync();
        // recaptchaRef.current.reset();
        setFirstNameError(false);
        setLastNameError(false);
        setEmailError(false);
        setPasswordError(false);

        if (firstName === '') {
            setFirstNameError(true);
        }
        if (lastName === '') {
            setLastNameError(true);
        }
        if (email === '') {
            setEmailError(true);
        }
        if (password === '') {
            setPasswordError(true);
        }

        if (!recaptchaValue) {
            toast.error("Please complete the reCAPTCHA.");
            return;
        }

        if (firstName && lastName && email && password) {
            fetch(`${API_URL}/user/sign-up`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    "first_name" :firstName, 
                    "last_name": lastName,
                    "email": email,
                    "password" :password,
                    "recaptcha": recaptchaValue,
                }),
                credentials: 'include',
            })
            .then(response => {
                return response.json();
            })
            .then((data) => {
                if (data.status === 200) {
                    toast.success(data.message);
                }
                else {
                    toast.error(data.message);
                }
            })
            .then(data => {
                console.log('Success:', data);
                toast.success(data.message);
            })
            .catch((error) => {
                console.error('Error:', error);
                toast.error(error);
            });
        }
    };

    return (
        <Container maxWidth="sm">
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <h2>Sign Up Form</h2>

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    name="firstName"
                    autoComplete="given-name"
                    autoFocus
                    onChange={e => setFirstName(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={firstName}
                    error={firstNameError}
                    helperText={firstNameError ? "First name is required" : ""}
                />

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="family-name"
                    onChange={e => setLastName(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={lastName}
                    error={lastNameError}
                    helperText={lastNameError ? "Last name is required" : ""}
                />

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email"
                    name="email"
                    autoComplete="email"
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
                    autoComplete="new-password"
                    onChange={e => setPassword(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={password}
                    error={passwordError}
                    helperText={passwordError ? "Password is required" : ""}
                />

                <ReCAPTCHA 
                   sitekey={RECAPTCHA_SITE_KEY}
                   onChange={(value) => setRecaptchaValue(value)}
                />

                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="secondary"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Sign Up
                </Button>
            </Box>
        </Container>
    );
};

export default SignUpForm;
