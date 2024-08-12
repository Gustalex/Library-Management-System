class UpdateUserController {

    static autoFillForm(user) {
        const nameField = document.getElementById('name');
        const emailField = document.getElementById('email');
        const cpfField = document.getElementById('cpf');

        if (nameField && !nameField.value) nameField.value = user.name || '';
        if (emailField && !emailField.value) emailField.value = user.email || '';
        if (cpfField && !cpfField.value) cpfField.value = user.cpf || '';
    }

    static removeCpfFormatting(cpf) {
        return cpf.replace(/[.-]/g, '');
    }

    static async checkCpf(cpf) {
        try {
            const cleanedCpf = this.removeCpfFormatting(cpf);
            const checkResponse = await axios.get(`http://127.0.0.1:8000/user/customers/check-cpf/?cpf=${cleanedCpf}`);
            const cpfData = checkResponse.data;
            if (cpfData.length > 0) {
                this.autoFillForm(cpfData[0]);
                return cpfData[0];
            }
            return false;
        } catch (error) {
            console.error('Error checking CPF', error);
            throw new Error('Error checking CPF');
        }
    }

    static async updateUser(event) {
        event.preventDefault();

        const cpf = document.getElementById('cpf').value;

        const userData = await this.checkCpf(cpf);

        if (!userData) {
            alert("CPF not found or invalid.");
            return;
        }

        const formData = new FormData(document.getElementById('update-user-form'));
        const user_id = userData.id;

        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            cpf: cpf,
        };

        try {
            const response = await axios.patch(`http://127.0.0.1:8000/user/customers/${user_id}/`, data, {
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

    observeElement('update-user-form', async () => {
        const cpfField = document.getElementById('cpf');
        cpfField.addEventListener('blur', async () => {
            const cpf = cpfField.value;
            if (cpf) {
                const cpfExists = await UpdateUserController.checkCpf(cpf);
                if (!cpfExists) {
                    UpdateUserController.autoFillForm({});
                }
            }
        });

        const updateForm = document.getElementById('update-user-form');
        updateForm.addEventListener('submit', async (event) => {
            await UpdateUserController.updateUser(event);
        });
    });

});
