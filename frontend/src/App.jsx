import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import Profile from './pages/profile';
import ForgetPassword from './pages/forgetPassword';
import ResetPassword from './pages/resetPassword';
import SendVerificationLink from './pages/sendVerificationLink';


function App() {

  return (
    <>
      <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/forget-password" element={<ForgetPassword />} />
        <Route path="/reset-password" element={<ResetPassword/>} />
        <Route path="/send-verification-link" element={<SendVerificationLink/>} />
        {/* <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} /> */}
      </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
