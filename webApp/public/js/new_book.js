class NewBookController {

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
});
