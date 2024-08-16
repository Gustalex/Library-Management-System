class BorrowController{

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

    static async createBorrow(event){
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

        const initialDate = document.getElementById('initial-date').value;
        const finalDate = document.getElementById('final-date').value

        const borrowData = {
            book_id: bookId,
            customer_id: userData.id,
            initial_date: initialDate,
            final_date: finalDate
        };
        
        try{
            const response = await axios.post('http://127.0.0.1:8000/book-services/borrow/', borrowData,{
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if(response.status === 201){
                alert('Book borrowed successfully');
            }
        }catch(error) {
            if (error.response && error.response.status === 404) {
                alert('Book is not available for borrow');
            }
            else if (error.response && error.response.status === 400) {
                alert('User has a fine and cannot borrow books');
            }
            else {
                console.error('Error creating borrow', error);
                alert('Failed to create borrow.');
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

    observeElement('new-borrow-form', async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const urlCpf = urlParams.get('cpf');
        const cpfField = document.getElementById('cpf');

        if (urlCpf && cpfField) {
            cpfField.value = urlCpf;
            await BorrowController.checkCpf(urlCpf);
        }

        cpfField.addEventListener('blur', async () => {
            if (!urlCpf) {  // Só executa se não houver um CPF na URL
                const cpf = cpfField.value;
                if (cpf) {
                    const user = await BorrowController.checkCpf(cpf);
                    if (!user) {
                        BorrowController.autoFillForm({});
                    }
                }
            }
        });

        const borrowForm = document.getElementById('new-borrow-form');
        borrowForm.addEventListener('submit', (event) => {
            BorrowController.createBorrow(event);
        });
    });
});
