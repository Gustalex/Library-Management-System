function formatCpf(cpf){
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

class FinesController {
    static async getLoan(loanId) {
        try {
            const loanResponse = await axios.get(`http://127.0.0.1:8000/book-services/borrow/${loanId}/get_loan/`);
            return loanResponse.data;            
        } catch (error) {
            console.error('Error fetching loan', error);
        }
    }

    static async getCustomerData(loanId) {
        try {
            const loan = await this.getLoan(loanId);
            const customerName = loan.customer_name;
            const customerEmail = loan.customer_email;
            return { customerName, customerEmail };
        } catch (error) {
            console.error('Error fetching customer data', error);
        }
    }

    static async concludeFine(fineId) {
        try {
            const response = await axios.delete(`http://127.0.0.1:8000/fine/fine/${fineId}/conclude/`);
            if (response.status === 204) {
                alert('Fine payment concluded successfully');
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error concluding fine', error);
        }
    }

    static async getFines(filters = {}) {
        try {
            const response = await axios.get('http://127.0.0.1:8000/fine/fine/list/', { params: filters });
            return response.data;
        } catch (error) {
            console.error('Error fetching fines', error);
        }
    }
    

    static async listActiveFines(filters = {}) {
        try {
            const activeFines = await this.getFines(filters);

            const loansData = await Promise.all(activeFines.map(fine => this.getLoan(fine.borrow)));

            const finesData = activeFines.map((fine, index) => {
                const loan = loansData[index];
                if (!loan) {
                    console.error(`Loan not found for borrow_id: ${fine.borrow}`);
                    return null;
                }
                return {
                    customerName: loan.customer_name,
                    customerCpf: loan.customer_cpf,
                    bookTitle: loan.book_name,
                    loanDate: loan.initial_date,
                    returnDate: loan.final_date,
                    fineValue: fine.value,
                    fineId: fine.id
                };
            }).filter(fine => fine !== null);

            const finesTableBody = document.getElementById('active-fines');
            finesTableBody.innerHTML = '';

            finesData.forEach(fine => {
                const row = document.createElement('tr');

                const customerCell = document.createElement('td');
                customerCell.textContent = fine.customerName;
                row.appendChild(customerCell);

                const cpfCell = document.createElement('td');
                cpfCell.textContent = formatCpf(fine.customerCpf);
                row.appendChild(cpfCell);

                const bookCell = document.createElement('td');
                bookCell.textContent = fine.bookTitle;
                row.appendChild(bookCell);

                const loanDateCell = document.createElement('td');
                const loanDate = new Date(fine.loanDate + 'T00:00:00');
                loanDateCell.textContent = loanDate.toLocaleDateString();
                row.appendChild(loanDateCell);

                const returnDateCell = document.createElement('td');
                const returnDate = new Date(fine.returnDate + 'T00:00:00');
                returnDateCell.textContent = returnDate.toLocaleDateString() || 'Open';
                row.appendChild(returnDateCell);

                const fineValueCell = document.createElement('td');
                fineValueCell.textContent = fine.fineValue;
                row.appendChild(fineValueCell);

                const concludeButtonCell = document.createElement('td');
                const concludeButton = document.createElement('button');
                concludeButton.textContent = 'Conclude Payment';
                concludeButton.className = 'conclude-button';
                concludeButton.addEventListener('click', async () => {
                    const concluded = await this.concludeFine(fine.fineId);
                    if (concluded) {
                        row.remove();
                    }
                });

                concludeButtonCell.appendChild(concludeButton);
                row.appendChild(concludeButtonCell);

                finesTableBody.appendChild(row);
            });

        } catch (error) {
            console.error('Error fetching active fines', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const activeFinesTable = document.getElementById('active-fines');
    if (activeFinesTable) {
        FinesController.listActiveFines();
    }

    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', async (event) => {
            event.preventDefault();
        
            const customerNameElement = document.getElementById('search-name');
            const cpfElement = document.getElementById('search-cpf');
        
            if (customerNameElement || cpfElement) {
                const customerName = customerNameElement.value.trim();
                const cpf = cpfElement.value.trim();
        
                const filters = {};
                if (customerName) filters.customer_name = customerName;
                if (cpf) filters.customer_cpf = cpf;
        
                await FinesController.listActiveFines(filters);
            }
        });        
    } else {
        console.error('Search form not found');
    }
});
