class EventController {
    static async getCustomers() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/user/customers/');
            return response.data;
        } catch (error) {
            console.error('Error fetching customers', error);
            alert('Error fetching customers');
        }
    }

    static async listEmails() {
        try {
            const customers = await this.getCustomers();
            const emailList = customers.map(customer => customer.email);
            console.log('emailList', emailList);
            return emailList;
        } catch (error) {
            console.error('Error listing emails', error);
            alert('Error listing emails');
        }
    }

    static async sendEmail(emailData) {
        try {
            await axios.post('http://127.0.0.1:8000/sendmail/', emailData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            });
            console.log(`Email sent to ${emailData.get('to_email')}`);
        } catch (error) {
            console.error(`Error sending email to ${emailData.get('to_email')}`, error);
            throw error; 
        }
    }

    static async retrySendEmail(emailData, maxRetries = 3) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                await this.sendEmail(emailData);
                return; 
            } catch (error) {
                console.error(`Attempt ${attempt} failed for email ${emailData.get('to_email')}`);
                if (attempt === maxRetries) {
                    alert(`Failed to send email to ${emailData.get('to_email')} after ${maxRetries} attempts.`);
                }
            }
        }
    }

    static async handleEmail(eventData) {
        try {
            const emailList = await this.listEmails();

            for (const email of emailList) {
                const emailData = new URLSearchParams();
                emailData.append('subject', `New Event: ${eventData.name}`);
                emailData.append('message', `
                    <p>Dear Customer,</p>
                    <p>We are excited to announce a new event!</p>
                    <p><strong>Event Name:</strong> ${eventData.name}</p>
                    <p><strong>Description:</strong> ${eventData.description}</p>
                    <p><strong>Date:</strong> ${eventData.date}</p>
                    <p>We hope to see you there!</p>
                    <p>Best regards,</p>
                    <p>Your Library Team</p>
                `);
                emailData.append('to_email', email);

                await this.retrySendEmail(emailData); 
            }

            alert('Emails sent successfully');
        } catch (error) {
            console.error('Error sending event notifications', error);
            alert('Error sending event notifications');
        }
    }

    static async handlePostEvent(eventData) {
        try {
            console.log('eventData', eventData);
            const response = await axios.post('http://127.0.0.1:8000/event/event/', eventData, {
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (response.status === 201) {
                await this.handleEmail(eventData);
                alert('Event created successfully');
            }
        } catch (error) {
            console.log('Error creating event', error);
            alert('Error creating event');
        }
    }

    static async createEvent() {
        const formData = new FormData(document.getElementById('new-event-form'));
        const data = {
            name: formData.get('event-name'),
            description: formData.get('event-description'),
            date: formData.get('event-date'),
        };
        console.log('data', data);
        await this.handlePostEvent(data);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const observeElement = (elementId, callback) => {
        const observer = new MutationObserver((_, observer) => {
            const element = document.getElementById(elementId);
            if (element) {
                callback(element);
                observer.disconnect();
            }
        });
        observer.observe(document, { childList: true, subtree: true });
    };

    observeElement('new-event-form', () => {
        document.getElementById('new-event-form').addEventListener('submit', async (event) => {
            event.preventDefault();
            await EventController.createEvent();
        });
    });
});
