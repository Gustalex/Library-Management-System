function formatCpf(cpf){
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}
class ReservationController{

    static async getActiveReservation(filters={}){
        try{
            const response = await axios.get('http://127.0.0.1:8000/book-services/reservation/reservations/', {params: filters});
            const activeReservations = response.data;
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

    static async listReservations(filters={}){
        try{
            const reservations = await this.getActiveReservation(filters);
            const reservationsTableBody = document.getElementById('active-reservations');
            reservationsTableBody.innerHTML='';
    
            reservations.forEach(reservation =>{
                const row = document.createElement('tr');
    
                const customerCell = document.createElement('td');
                customerCell.textContent = reservation.customer_name;
                row.appendChild(customerCell);

                const cpfCell = document.createElement('td');
                cpfCell.textContent = formatCpf(reservation.customer_cpf);
                row.appendChild(cpfCell);
    
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
                            this.listReservations(filters);
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
document.addEventListener('DOMContentLoaded', async () => {
    const reservationsTableBody = document.getElementById('active-reservations');
    if(reservationsTableBody){
        ReservationController.listReservations();
    }

    const searchForm = document.getElementById('search-form');
    if(searchForm){
        searchForm.addEventListener('submit', async (event) => {
            event.preventDefault();
           
            const customerNameElement = document.getElementById('search-name');
            const cpfElement = document.getElementById('search-cpf');

            if(customerNameElement || cpfElement){
                const customerName = customerNameElement.value.trim();
                const cpf = cpfElement.value.trim();

                const filters = {};
                if(customerName) filters.customer_name = customerName;
                if(cpf) filters.customer_cpf = cpf;

                await ReservationController.listReservations(filters); 
            }
        });
    }
    else{
        console.error('Search form not found');
    }
});