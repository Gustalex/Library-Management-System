class FinesController{

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

    static async concludeFine(fineId){
        try{
            const response = await axios.delete(`http://127.0.0.1:8000/fine/fine/${fineId}/conclude/`);
            if(response.status === 204){
                alert('Fine payment concluded successfully');
                return true;
            }
            return false;
        }catch(error){
            console.error('Error concluding fine', error);
        }
    }

    static async listActiveFines(){
        try {
            const fineResponse = await axios.get('http://127.0.0.1:8000/fine/fine/list/');
            const activeFines = fineResponse.data.filter(fine => fine.status === true);
            
            const loansData = await Promise.all(activeFines.map(fine => this.getLoan(fine.borrow)));
    
            const finesData = activeFines.map((fine, index) => {
                const loan = loansData[index];
                if (!loan) {
                    console.error(`Loan not found for borrow_id: ${fine.borrow}`);
                    return null;
                }
                return {
                    customerName: loan.customer_name,
                    bookTitle: loan.book_name,
                    loanDate: loan.initial_date,
                    returnDate: loan.final_date,
                    fineValue: fine.value
                };
            }).filter(fine => fine !== null);
    
            const finesTableBody = document.getElementById('active-fines');
            finesTableBody.innerHTML = '';
            
            finesData.forEach(fine => {
                const row = document.createElement('tr');
    
                const customerCell = document.createElement('td');
                customerCell.textContent = fine.customerName;
                row.appendChild(customerCell);
    
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
                    const fineId = activeFines.find(f => f.borrow_id === fine.borrow_id).id;
                    const concluded = await this.concludeFine(fineId);
                    if(concluded){
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

    observeElement('active-fines', async () => {
        await FinesController.listActiveFines();
    });

});