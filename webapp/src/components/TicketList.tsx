// src/components/TicketList.tsx
import * as React from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/apiService';
import { List, ListItem, ListItemText, Typography } from '@mui/material';

const TicketList: React.FC = () => {
    const [tickets, setTickets] = React.useState<any[]>([]);

    React.useEffect(() => {
        const fetchTickets = async () => {
            try {
                const response = await apiService.get('/tickets');
                setTickets(response.data);
            } catch (error) {
                console.error('Error fetching tickets:', error);
            }
        };

        fetchTickets();
    }, []);

    return (
        <div>
            <Typography variant='h5' gutterBottom>
                Tickets
            </Typography>
            <List>
                {tickets.map((ticket: any) => (
                    <ListItem key={ticket.id} component={Link} to={`/tickets/${ticket.id}`} button>
                        <ListItemText primary={ticket.title} secondary={`Status: ${ticket.status}, Assignee: ${ticket.assignee}, Priority: ${ticket.priority}`} />
                    </ListItem>
                ))}
            </List>
        </div>
    );
};

export default TicketList;
