function formatCpf(cpf){
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

class CustomersController{

    static async getCustomers(){
        try{
            const response = await axios.get('http://127.0.0.1:8000/user/customers/');
            console.log(response.data);
            return response.data;
        }catch(error){
            console.error('Error fetching customers', error);
            alert('Error fetching customers');
        }
    }
    
    static async deleteCustomer(customerId){
        try{
            const response = await axios.delete(`http://127.0.0.1:8000/user/customers/${customerId}/`);
            if(response.status === 204){
                alert('Customer deleted successfully');
                return true;
            }
        }catch(error){
            console.error('Error deleting customer', error);
            alert('Error deleting customer');
        }
    }

    static async listCustomers(){

        try{

            const customers = await this.getCustomers();
            const customersTableBody = document.getElementById('customers-list');
            customersTableBody.innerHTML = '';
    
            customers.forEach(customer => {
                const row = document.createElement('tr');
    
                const customerCell = document.createElement('td');
                customerCell.textContent = customer.name;
                row.appendChild(customerCell);
    
                const emailCell = document.createElement('td');
                emailCell.textContent = customer.email;
                row.appendChild(emailCell);
    
                const cpfCell = document.createElement('td');
                cpfCell.textContent = formatCpf(customer.cpf);
                row.appendChild(cpfCell);
    
                const actionCell = document.createElement('td');

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.className = 'delete-button btn btn-danger';
                deleteButton.style.marginRight = '10px';
                deleteButton.onclick = async () => {
                    if(confirm('Are you sure you want to delete this customer?')){
                        if(await this.deleteCustomer(customer.id)){
                            this.listCustomers();
                        }
                    }
                }

                const editButton = document.createElement('a');
                editButton.textContent = 'Edit';
                editButton.className = 'return-button btn btn-primary';
                editButton.href = 'update-user.html?id='+customer.id;

                actionCell.appendChild(deleteButton);
                actionCell.appendChild(editButton);

                row.appendChild(actionCell);

    
                customersTableBody.appendChild(row);
                
            });
        }catch(error){
            console.error('Error listing customers', error);
            alert('Error listing customers');
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

    observeElement('customers-list', async () => {
        await CustomersController.listCustomers();
    });

});