class ReserveController {

    static autoFillForm(user) {
        const nameField = document.getElementById('name');
        const emailField = document.getElementById('email');
        const cpfField = document.getElementById('cpf');

        if (nameField) nameField.value = user.name || '';
        if (emailField) emailField.value = user.email || '';
        if (cpfField) cpfField.value = user.cpf || '';
    }

    static removeCpfFormatting(cpf) {
        return cpf.replace(/[.-]/g, '');
    }

    static async checkCpf(cpf) {
        try {
            const cleanedCpf = this.removeCpfFormatting(cpf);
            const checkResponse = await axios.get(`http://127.0.0.1:8000/user/customers/check-cpf/?cpf=${cleanedCpf}`);
            const cpfData = checkResponse.data;
            if (cpfData.length > 0){
                this.autoFillForm(cpfData[0]);
                return cpfData[0];
            }
            return false;
        } catch (error) {
            console.error('Error checking CPF', error);
            throw new Error('Error checking CPF');
        }
    }

    static async createReservation(event){
        event.preventDefault();

        const urlParams = new URLSearchParams(window.location.search);
        const bookId = urlParams.get('id');

        const cpfField = document.getElementById('cpf');
        const cpf = cpfField.value;

        const userData = await this.checkCpf(cpf);

        if (!userData) {
            alert("CPF não encontrado ou inválido.");
            return;
        }

        const reservationData = {
            book_id: bookId,
            customer_id: userData.id,
        };
    
        try {
            const response = await axios.post('http://127.0.0.1:8000/book-services/reserve/', reservationData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            }); 
            if(response.status === 201){
                alert('Book reserved successfully');
            }
        } catch(error) {
            if (error.response && error.response.status === 404) {
                alert('Book is not available for reservation');
            }
            else if (error.response && error.response.status === 409) {
                alert('User has a fine and cannot reserve books');
            }
            else {
                console.error('Error creating reservation', error.response);
                alert('Failed to create reservation.');
            }
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

    observeElement('new-reservation-form', async () => {
        const cpfField = document.getElementById('cpf');
        cpfField.addEventListener('blur', async () => {
            const cpf = cpfField.value;
            if (cpf) {
                const cpfExists = await ReserveController.checkCpf(cpf);
                if (!cpfExists) {
                    ReserveController.autoFillForm({});
                }
            }
        });

        const reservationForm = document.getElementById('new-reservation-form');
        reservationForm.addEventListener('submit', (event) => {
            ReserveController.createReservation(event);
        });
    });
});
