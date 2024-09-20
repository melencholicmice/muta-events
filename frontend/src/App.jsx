import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import Profile from './pages/profile';
import ForgetPassword from './pages/forgetPassword';
import ResetPassword from './pages/resetPassword';
import SendVerificationLink from './pages/sendVerificationLink';
import CreateEventForm from './pages/createEvent';
import EventPage from './pages/event';
import RegisterEvent from './pages/resgisterEvent';
import EditEventForm from './pages/editEvent';


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
        <Route path="/create-event" element={<CreateEventForm/>} />
        <Route path="/event" element={<EventPage />} />
        <Route path="/register-event" element={<RegisterEvent />} />
        <Route path="/edit-event" element={<EditEventForm />} />
      </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
