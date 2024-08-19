class EventDetailController {

    static async getEventById(eventId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/event/event/${eventId}/`);
            return response.data;
        } catch (error) {
            console.error('Error getting event detail', error);
        }
    }

    static async deleteEvent(eventId) {
        try{
            const response = await axios.delete(`http://127.0.0.1:8000/event/event/${eventId}/`);
            if(response.status === 204){
                alert('Event deleted successfully');
            }
        }catch(error){
            console.error('Error deleting event', error);
        }
    }

    static async showEventDetail() {
        const urlParams = new URLSearchParams(window.location.search);
        const eventId = urlParams.get('id');

        if (eventId) {
            try {
                const event = await this.getEventById(eventId);
                const eventDetailContainer = document.getElementById('event-detail');

                const eventDate = new Date(event.date + 'T00:00:00');
                const formatedDate = eventDate.toLocaleDateString();

                if (event) {
                    eventDetailContainer.innerHTML = `
                        <div class="event-detail-container">
                            <h3>${event.name}</h3>
                                <div class="book-synopsis">
                                    <p>${event.description ? event.description : 'No description available'}</p>
                                </div>
                                <br>
                                    <p><strong>Date:</strong> ${formatedDate}</p>
                                <div class="book-actions" style="text-align: right;">
                                    <button class="update-button" id="edit-button" style="margin-left: 900px;margin-top: -300px;">Edit</button>
                                    <button class="delete-button" id="delete-button" style="margin-left: 900px;">Delete</button>
                                </div>
                        </div>
                    `;

                    document.getElementById('edit-button').addEventListener('click', () => {
                        window.location.href = `../views/update-event.html?id=${eventId}`;
                    });

                    document.getElementById('delete-button').addEventListener('click', async () => {
                        if (confirm('Are you sure you want to delete this event?')) {
                            const success = await this.deleteEvent(eventId);
                            if (success) {
                                window.location.href = '../views/events.html';
                            }
                        }
                    });
                } 
            } catch (error) {
                console.error('Error displaying event detail', error);
                document.getElementById('event-detail').innerHTML = `<p>Error loading event details.</p>`;
            }
        } else {
            document.getElementById('event-detail').innerHTML = `<p>No event ID provided.</p>`;
        }
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

    observeElement('event-detail', async () => {
        await EventDetailController.showEventDetail();
    });
});