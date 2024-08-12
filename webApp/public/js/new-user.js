class NewUserController{

    static async createNewUser(){
        const formData = new FormData(document.getElementById('new-user-form')); 
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            cpf: formData.get('cpf'),
        };
        try{
            const response = await axios.post('http://127.0.0.1:8000/user/customers/', data,{
                headers:{
                    'Content-Type': 'application/json'
                }
            });
            if(response.status === 201){
                alert('User created successfully');
            }
        }catch(error){
            console.error('Error creating user', error);
            alert('Error creating user', error);
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

    observeElement('new-user-form', async () => {
        document.getElementById('new-user-form').addEventListener('submit', async (event) => {
            event.preventDefault();
            await NewUserController.createNewUser();
        });
    });

});
