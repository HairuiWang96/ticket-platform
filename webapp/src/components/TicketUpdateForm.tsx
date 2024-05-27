// src/components/TicketUpdateForm.tsx
import * as React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom';
import { Button, TextField, Box } from '@mui/material';
import apiService from '../services/apiService';

interface FormData {
    status: string;
    assignee: string;
    priority: string;
}

const TicketUpdateForm: React.FC = () => {
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
            // Redirect to ticket details page after updating
            navigate(`/tickets/${id}`); // Use navigate function
        } catch (error) {
            console.error('Error updating ticket:', error);
        }
    };

    return (
        <Box mt={2}>
            <form onSubmit={handleSubmit(onSubmit)}>
                <TextField {...register('status')} label='Status' variant='outlined' fullWidth margin='normal' />
                <TextField {...register('assignee')} label='Assignee' variant='outlined' fullWidth margin='normal' />
                <TextField {...register('priority')} label='Priority' variant='outlined' fullWidth margin='normal' />
                <Button type='submit' variant='contained' color='primary'>
                    Update Ticket
                </Button>
            </form>
        </Box>
    );
};

export default TicketUpdateForm;
