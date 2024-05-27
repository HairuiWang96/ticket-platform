import * as React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom';
import { Button, TextField, Box, InputLabel } from '@mui/material';
import apiService from '../services/apiService';

interface FormData {
    status: string;
    assignee: string;
    priority: string;
}

interface Props {
    onTicketUpdated: () => void; // Define the prop for onTicketUpdated function
}

const TicketUpdateForm: React.FC<Props> = ({ onTicketUpdated }) => {
    const { id } = useParams<{ id: string }>();
    const { register, handleSubmit, setValue } = useForm<FormData>();
    const navigate = useNavigate(); // Use useNavigate hook

    React.useEffect(() => {
        const fetchTicket = async () => {
            try {
                const response = await apiService.get(`/tickets/${id}`);
                const ticket = response.data;
                setValue('status', ticket.status);
                setValue('assignee', ticket.assignee);
                setValue('priority', ticket.priority);
            } catch (error) {
                console.error('Error fetching ticket:', error);
            }
        };

        fetchTicket();
    }, [id, setValue]);

    const onSubmit = async (data: FormData) => {
        try {
            console.log('data ', data);
            await apiService.put(`/tickets/${id}`, data);
            // Call the onTicketUpdated function provided by the parent component
            if (typeof onTicketUpdated === 'function') {
                onTicketUpdated();
            }
            // Redirect to ticket details page after updating
            navigate(`/tickets/${id}`); // Use navigate function
        } catch (error) {
            console.error('Error updating ticket:', error);
        }
    };

    return (
        <Box mt={2}>
            <form onSubmit={handleSubmit(onSubmit)}>
                <InputLabel>Status</InputLabel>
                <TextField
                    {...register('status')}
                    variant='outlined'
                    fullWidth
                    margin='normal'
                    sx={{ mb: 2 }} // Add margin-bottom to create space between this TextField and the next one
                />

                <InputLabel>Assignee</InputLabel>
                <TextField
                    {...register('assignee')}
                    variant='outlined'
                    fullWidth
                    margin='normal'
                    sx={{ mb: 2 }} // Add margin-bottom to create space between this TextField and the next one
                />

                <InputLabel>Priority</InputLabel>
                <TextField
                    {...register('priority')}
                    variant='outlined'
                    fullWidth
                    margin='normal'
                    sx={{ mb: 2 }} // Add margin-bottom to create space between this TextField and the Button
                />

                <Button type='submit' variant='contained' color='primary'>
                    Update Ticket
                </Button>
            </form>
        </Box>
    );
};

export default TicketUpdateForm;
