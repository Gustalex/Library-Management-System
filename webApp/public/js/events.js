class EventsController{
    static async listEvents(filters={}){
        try{
            const response = await axios.get('http://127.0.0.1:8000/event/event/', {params: filters});
            return response.data;
        }catch(error){
            console.error('Error fetching events', error);
        }
    }

    static async populateEvents(filters={}){
        try{
            const events = await this.listEvents(filters);
            const eventList = document.getElementById('event-list');
            eventList.innerHTML = '';

            const eventsToShow = events.slice(0, 12);

            for(const event of eventsToShow){
                const eventElement = document.createElement('div');
                eventElement.classList.add('book', 'book-list-item');

                const eventDate = new Date(event.date + 'T00:00:00');
                const formatedDate = eventDate.toLocaleDateString();

                eventElement.innerHTML = `
                    <div class="book-title-container">
                        <h2 class="book-title">${event.name}</h2>
                    </div>
                    <div class="book-author">
                        <span class="book-author-item">
                            <i class="fas fa-calendar"></i> ${formatedDate}
                        </span>
                    </div>
                    <footer class="book-footer">
                        <a href="../views/event-detail.html?id=${event.id}" class="book-read-more button button-dark button-full-width">
                            <i class="fas fa-eye"></i>
                        </a>
                    </footer>
                `;
                eventList.appendChild(eventElement);
            }

        }catch(error){
            console.error('Error populating events', error);
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

    observeElement('event-list', async () => {
        await EventsController.populateEvents();
    });

    document.getElementById('search-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const name = document.getElementById('search-name').value.trim();
        const date = document.getElementById('search-date').value.trim();

        const filters = {};
        if(name) filters.name = name;
        if(date) filters.date = date;

        await EventsController.populateEvents(filters);
    });

});