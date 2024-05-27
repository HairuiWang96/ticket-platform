import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import TicketList from './components/TicketList';
import TicketDetails from './components/TicketDetails'; // Assuming you create a TicketDetails component
import TicketUpdateForm from './components/TicketUpdateForm'; // Assuming you create a TicketUpdateForm component

const App: React.FC = () => {
    return (
        <Router>
            <Container maxWidth='sm'>
                <Typography variant='h4' component='h1' sx={{ mb: 2 }}>
                    Ticket Support Platform
                </Typography>
                <Routes>
                    <Route path='/' element={<TicketList />} />
                    <Route path='/tickets' element={<TicketList />} />
                    <Route path='/tickets/:id' element={<TicketDetails />} />
                    <Route path='/tickets/:id/edit' element={<TicketUpdateForm />} />
                </Routes>
            </Container>
        </Router>
    );
};

export default App;
