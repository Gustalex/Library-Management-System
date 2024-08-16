function removeCpfFormatting(cpf) {
    return cpf.replace(/[.-]/g, '');
}

function fillCustomerData(customerData) {
    document.getElementById('name').value = customerData.name;
    document.getElementById('email').value = customerData.email;
    document.getElementById('cpf').value = customerData.cpf;
}

class UpdateUserController {

    static getCustomerData(customer) {
        return {
            name: customer.name,
            email: customer.email,
            cpf: customer.cpf
        };
    }

    static async getCustomerById(customerId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/user/customers/${customerId}/`);
            return this.getCustomerData(response.data);
        } catch (error) {
            console.error('Error fetching customer', error);
            alert('Error fetching customer');
        }
    }

    static async updateUser(event) {
        event.preventDefault();

        const urlParams = new URLSearchParams(window.location.search);
        const customerId = urlParams.get('id');
        

        const formData = new FormData(document.getElementById('update-user-form'));

        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            cpf: formData.get('cpf')
        };

        try {
            const response = await axios.patch(`http://127.0.0.1:8000/user/customers/${customerId}/`, data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.status === 200) {
                alert('User updated successfully');
            }
            return response.data;
        } catch (error) {
            console.error('Error updating user', error);
            alert('Error updating user');
        }
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const customerId = urlParams.get('id');

    if (customerId) {
        const userData = await UpdateUserController.getCustomerById(customerId);
        fillCustomerData(userData);
    }

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

    observeElement('update-user-form', async () => {
        const updateForm = document.getElementById('update-user-form');
        updateForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await UpdateUserController.updateUser(event);
        });
    });
});
