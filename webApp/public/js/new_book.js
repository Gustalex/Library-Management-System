class NewBookController {

    // Genre Actions

    static async listGenres() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book/genre/');
            return response.data;
        } catch (error) {
            console.error('Error fetching genres', error);
        }
    }

    static async populateGenres() {
        const genres = await NewBookController.listGenres();
        const genreSelect = document.getElementById('genre');

        if (genres) {
            genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre.id;
                option.textContent = genre.name; 
                genreSelect.appendChild(option);
            });
        }
    }

    static async createGenre(){
        const genreForm = document.getElementById('new-genre-form');
        if(genreForm){
            genreForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const formData = new FormData(genreForm);
                const data_genre = {
                    name: formData.get('new-genre'),
                };
                console.log('Dados do genero:', data_genre);
                try{
                    const response=await axios.post('http://127.0.0.1:8000/book/genre/', data_genre, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    if(response.status===201){
                        window.location.replace('../views/new_book.html');
                    }
                }
                catch(error){
                    alert('Error creating genre', error);
                }
            });
        }
    }

    // Book Actions
    
    static async createBook() {
        const bookForm = document.getElementById('new-book-form');
        if (bookForm) {
            bookForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const formData = new FormData(bookForm);
                const data_book = {
                    title: formData.get('title'),
                    author: formData.get('author'),
                    genre: formData.get('genre'),
                    edition: formData.get('edition'),
                    synopsis: formData.get('synopsis'),
                };

                const cover = formData.get('cover');
                if(cover){
                    console.log('Cover:', cover);
                }

                try {
                    console.log('Dados do livro:', data_book);
                    const response = await axios.post('http://127.0.0.1:8000/book/book/', data_book, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    if (response.status === 201) {
                        alert('Book created successfully');
                    }
                    return response.data;
                } catch (error) {
                    alert('Error creating book');
                }
            });
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

    observeElement('new-book-form', async () => {
        await NewBookController.populateGenres();
        NewBookController.createBook();
    });

    observeElement('new-genre-form', async () => {
        NewBookController.createGenre();
    });
});
