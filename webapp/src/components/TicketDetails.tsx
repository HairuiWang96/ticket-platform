import * as React from 'react';
import { useParams, Link } from 'react-router-dom';
import apiService from '../services/apiService';
import { Typography, Paper, Box, Button } from '@mui/material';

interface Ticket {
    id: number;
    subject: string;
    status: string;
    priority: string;
    assignee: string;
    description: string;
}

const TicketDetails: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [ticket, setTicket] = React.useState<Ticket | null>(null);

    const fetchTicketDetails = async () => {
        try {
            const response = await apiService.get(`/tickets/${id}`);
            setTicket(response.data);
        } catch (error) {
            console.error('Error fetching ticket details:', error);
        }
    };

    React.useEffect(() => {
        fetchTicketDetails();
    }, [id]);

    if (!ticket) {
        return <Typography variant='body1'>Loading...</Typography>;
    }

    return (
        <Box mt={2}>
            <Typography variant='h5' gutterBottom>
                Ticket Details
            </Typography>
            <Paper elevation={3} variant='outlined'>
                <Box p={2}>
                    <Typography variant='h6' gutterBottom>
                        Subject: {ticket.subject}
                    </Typography>
                    <Typography variant='body1'>Status: {ticket.status}</Typography>
                    <Typography variant='body1'>Assignee: {ticket.assignee}</Typography>
                    <Typography variant='body1'>Priority: {ticket.priority}</Typography>
                    <Typography variant='body1'>Description: {ticket.description}</Typography>
                </Box>
            </Paper>
            <Box mt={2} display='flex' justifyContent='space-between'>
                <Button variant='contained' color='primary' component={Link} to={`/tickets/${id}/thread`}>
                    View Thread
                </Button>
                <Button variant='contained' color='primary' component={Link} to={`/tickets/${ticket.id}/edit`}>
                    Edit Ticket
                </Button>
            </Box>
        </Box>
    );
};

export default TicketDetails;
