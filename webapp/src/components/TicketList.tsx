import * as React from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/apiService';
import { List, ListItem, ListItemText, Typography } from '@mui/material';

const TicketList: React.FC = () => {
    const [tickets, setTickets] = React.useState<any[]>([]);
    const [showDoneTickets, setShowDoneTickets] = React.useState<boolean>(false);

    React.useEffect(() => {
        const fetchTickets = async () => {
            try {
                const response = await apiService.get('/tickets', {
                    params: { done: showDoneTickets },
                });
                setTickets(response.data);
            } catch (error) {
                console.error('Error fetching tickets:', error);
            }
        };

        fetchTickets();
    }, [showDoneTickets]);

    return (
        <div>
            <Typography variant='h5' gutterBottom>
                Tickets
            </Typography>
            <div>
                <label>
                    Show Open Tickets:
                    <input type='checkbox' checked={showDoneTickets} onChange={e => setShowDoneTickets(e.target.checked)} />
                </label>
            </div>
            <List>
                {tickets.map((ticket: any) => (
                    <ListItem key={ticket.id} component={Link} to={`/tickets/${ticket.id}`} button sx={{ marginBottom: 2 }}>
                        <ListItemText primary={ticket.title} secondary={`Status: ${ticket.status}, Assignee: ${ticket.assignee}, Priority: ${ticket.priority}`} />
                    </ListItem>
                ))}
            </List>
        </div>
    );
};

export default TicketList;
