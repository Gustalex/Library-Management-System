class LoansController {

    static async handleFine(loanId, customerId) {
        try {
            const fineData = { customer_id: customerId, borrow_id: loanId };
    
            const fineResponse = await axios.post('http://127.0.0.1:8000/fine/fine/', fineData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
                
            if (fineResponse.status === 201) {
                alert('Book returned and fine created successfully');
                return true;
            }
            alert('Book returned successfully');
            return false;
        } catch (error) {
            console.error('Error handling fine', error);
            alert('Error handling fine');
            return false;
        }
    }
    
    

    static async handleDevolution(customerId, bookId){
        try{
            const devolutionData = {customer_id: customerId, book_id: bookId};
            const devolutionResponse = await axios.patch('http://127.0.0.1:8000/book-services/devolution/', devolutionData,{
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            if(devolutionResponse.status == 200){
                console.log('Devolution successful');
            }
        }catch(error){
            console.error('Error returning book', error);
        }
    }

    static async returnBook(loanId, customerId, bookId){
        try{
            await this.handleFine(loanId, customerId);
            await this.handleDevolution(customerId, bookId);
        }catch(error){
            console.error('Error returning book', error);
        }
    }


    static async listActiveLoans() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book-services/borrow/loans/');
            const activeLoans = response.data.filter(loan => loan.active === true);
            console.log('Active loans:', activeLoans);
            const loansTableBody = document.getElementById('active-loans');
            loansTableBody.innerHTML = ''; 

            activeLoans.forEach(loan => {
                const row = document.createElement('tr');

                const customerCell = document.createElement('td');
                customerCell.textContent = loan.customer_name;
                row.appendChild(customerCell);

                const bookCell = document.createElement('td');
                bookCell.textContent = loan.book_name;
                row.appendChild(bookCell);

                const loanDateCell = document.createElement('td');
                const loanDate = new Date(loan.initial_date + 'T00:00:00');
                loanDateCell.textContent = loanDate.toLocaleDateString();
                row.appendChild(loanDateCell);

                const returnDateCell = document.createElement('td');
                const returnDate = new Date(loan.final_date + 'T00:00:00');
                returnDateCell.textContent = returnDate.toLocaleDateString() || 'Open';
                row.appendChild(returnDateCell);

                const returnButtonCell = document.createElement('td');
                const returnButton = document.createElement('button');
                returnButton.textContent = 'Return';
                returnButton.className = 'return-button'; 
                returnButton.addEventListener('click', () => {
                    this.returnBook(loan.id, loan.customer, loan.book);
                });

                returnButtonCell.appendChild(returnButton);
                row.appendChild(returnButtonCell);

                loansTableBody.appendChild(row);
            });

        } catch (error) {
            console.error('Error fetching active loans', error);
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

    observeElement('active-loans', async () => {
        await LoansController.listActiveLoans();
    });

});

