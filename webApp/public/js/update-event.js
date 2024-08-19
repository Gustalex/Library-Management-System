function fillEventData(eventData){
    console.log(eventData);
    document.getElementById('event-name').value = eventData.name;
    document.getElementById('event-description').value = eventData.description;
    document.getElementById('event-date').value = eventData.date;
}
class UpdateEventController{

    static getEventData(event){
        return {
            name: event.name,
            description: event.description,
            date: event.date
        };
    }

    static async getEventById(eventId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/event/event/${eventId}/`);
            return this.getEventData(response.data);
        } catch (error) {
            console.error('Error getting event detail', error);
        }
    }

    static async updateEvent(event){
        event.preventDefault();

        const urlParams = new URLSearchParams(window.location.search);
        const eventId = urlParams.get('id');

        const formData = new FormData(document.getElementById('update-event-form'));

        const data = {
            name: formData.get('event-name'),
            description: formData.get('event-description'),
            date: formData.get('event-date')
        };

        console.log('patching event', data);

        try{
            const response = await axios.patch(`http://127.0.0.1:8000/event/event/${eventId}/`, data,{
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if(response.status === 200){
                alert('Event updated successfully');
            }
            return response.data;
        }catch(error){
            console.error('Error updating event', error);
            alert('Error updating event');
        }
    }


}
document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = urlParams.get('id');

    if (eventId) {
        const eventData = await UpdateEventController.getEventById(eventId);
        fillEventData(eventData);
    }

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

    observeElement('update-event-form', async () => {
        const updateForm = document.getElementById('update-event-form');
        updateForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await UpdateEventController.updateEvent(event);
        });
    });
});
