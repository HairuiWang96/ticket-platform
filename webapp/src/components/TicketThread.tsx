// TicketThread.tsx
import * as React from 'react';
import { useParams } from 'react-router-dom';
import apiService from '../services/apiService';
import { Typography } from '@mui/material';

const TicketThread: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [messages, setMessages] = React.useState<any[]>([]);

    const fetchTicketMessages = async () => {
        try {
            const response = await apiService.get(`/tickets/${id}/messages`);
            setMessages(response.data);
        } catch (error) {
            console.error('Error fetching ticket messages:', error);
        }
    };

    React.useEffect(() => {
        fetchTicketMessages();
    }, [id]);

    return (
        <div>
            <Typography variant='h5' gutterBottom>
                Ticket Thread
            </Typography>
            {messages.map((message: any) => (
                <div key={message.id}>
                    <Typography variant='subtitle1'>From: {message.sender}</Typography>
                    <Typography variant='body1'>Content: {message.content}</Typography>
                    <hr />
                </div>
            ))}
        </div>
    );
};

export default TicketThread;
