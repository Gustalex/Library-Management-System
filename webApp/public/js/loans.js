class LoansController {

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

    static async handleFine(loanId, customerId, bookId) {
        try {
            const fineData = { customer_id: customerId, borrow_id: loanId };
            const fineResponse = await axios.post('http://127.0.0.1:8000/fine/fine/', fineData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (fineResponse.status === 201) {
                const fineValue = fineResponse.data.value;

                const { customerName, customerEmail } = await this.getCustomerData(loanId);
                
                await this.handleDevolution(customerId, bookId);
                await this.handleEmail(customerName, customerEmail, fineValue);
                return true;
            }
            await this.handleDevolution(customerId, bookId);
            return false;
        } catch (error) {
            console.error('Error handling fine', error);
            alert('Error handling fine');
            return false;
        }
    }

    static async handleEmail(customerName, customerEmail, fineValue) {
        try {
            console.log('Sending fine notification email:', customerName, customerEmail, fineValue);
            const pixKey = '06220161483'
            const emailData = {
                subject: `Library Fine Notification for ${customerName}`,
                message: `
                    <p>Dear ${customerName},</p>
                    <p>You have incurred a fine of R$${fineValue} for the late return of your borrowed book. Please ensure that you pay this fine as soon as possible.</p>
                    <p>To make the payment, please use the following PIX key:</p>
                    <p><strong>${pixKey}</strong></p>
                    <p>Once the payment is completed, kindly reply to this email with the payment confirmation. This will help us update our records accordingly.</p>
                    <p>Thank you for your prompt attention to this matter.</p>
                    <p>Best regards,</p>
                    <p>Your Library Team</p>
                `,
                to_email: customerEmail
            };
    
            const emailResponse = await axios.post('http://127.0.0.1:8000/sendmail/', emailData, {
                headers:{
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            });
    
            if (emailResponse.status === 200) {
                alert('Book returned and mail with fine notification sent successfully');
            }
        } catch (error) {
            console.error('Error sending fine notification email', error);
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
                alert('Book returned successfully');
            }
        }catch(error){
            console.error('Error returning book', error);
        }
    }

    static async returnBook(loanId, customerId, bookId){
        try{
            await this.handleFine(loanId, customerId, bookId);
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

