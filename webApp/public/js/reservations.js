class ReservationController{

    static async getActiveReservation(){
        try{
            const response = await axios.get('http://127.0.0.1:8000/book-services/reservation/reservations/')
            const activeReservations = response.data.filter(reservation => reservation.active === true );
            console.log('active reservations', activeReservations);
            return activeReservations;
        }catch(error){
            console.error('Error fetching reservations', error);
        }
    }

    static async handleCancelReservation(reservationId){
        try{
            const response = await axios.delete(`http://127.0.0.1:8000/book-services/reserve/${reservationId}/delete/`);
            if(response.status == 204){
                alert('Reservation canceled successfully');
            }
        }catch(error){
            console.log('Error cancelling reservation', error)
            alert('Error cancelling reservation')
        }
    }

    static async listReservations(){
        try{
            const reservations = await this.getActiveReservation();
            const reservationsTableBody = document.getElementById('active-reservations');
            reservationsTableBody.innerHTML='';
    
            reservations.forEach(reservation =>{
                const row = document.createElement('tr');
    
                const customerCell = document.createElement('td');
                customerCell.textContent = reservation.customer_name;
                row.appendChild(customerCell);
    
                const bookCell = document.createElement('td');
                bookCell.textContent = reservation.book_name;
                row.appendChild(bookCell);


    
                const actionCell = document.createElement('td');
                const cancelButton = document.createElement('button');
                cancelButton.textContent = 'Cancel';
                cancelButton.className = 'delete-button';
                cancelButton.style.marginRight = '10px';
                cancelButton.onclick = async () => {
                    if(confirm('Are you sure you want to cancel this reservation?')){
                        if(await this.handleCancelReservation(reservation.id)){
                            this.listReservations();
                        }
                    }
                }

                const borrowButton = document.createElement('a');
                borrowButton.textContent = 'Borrow';
                borrowButton.className = 'conclude-button';
                borrowButton.href = 'borrow.html?cpf=' + reservation.customer_cpf + '&id=' + reservation.book;                

                actionCell.appendChild(cancelButton);
                actionCell.appendChild(borrowButton);
                row.appendChild(actionCell)
    
                reservationsTableBody.appendChild(row);
            });
        }catch(error){
            console.log('Error listing reservations', error)
            alert('Error listing reservations')
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

    observeElement('active-reservations', async () => {
        await ReservationController.listReservations();
    });

});