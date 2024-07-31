function resizeBookCover(cover) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        const originalName = cover.name;

        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                const targetWidth = 348;
                const targetHeight = 500;
                canvas.width = targetWidth;
                canvas.height = targetHeight;

                ctx.drawImage(img, 0, 0, targetWidth, targetHeight);

                canvas.toBlob((blob) => {
                    if (blob) {
                        const file = new File([blob], originalName, { type: 'image/jpeg' });
                        resolve(file);
                    } 
                    else {
                        reject(new Error('Failed to create blob from canvas'));
                    }
                }, 'image/jpeg', 1);
            };
            img.src = event.target.result;
        };
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(cover);
    });
}
class NewBookController {

    // Util

    static autofillFields(book) {
        document.getElementById('title').value = book.title || '';
        document.getElementById('author').value = book.author || '';
        document.getElementById('genre').value = book.genre || '';
        document.getElementById('edition').value = book.edition || '';
        document.getElementById('synopsis').value = book.synopsis || '';
    }

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

    static async listBooks() {
        try{
            const response = await axios.get('http://127.0.0.1:8000/book/book/')
            console.log('Books:', response.data);
            return response.data;
        }catch(error){
            console.error('Error fetching books', error);
        }
    }

    static async checkIsbn(isbn) {
        try {
            const checkResponse = await axios.get(`http://127.0.0.1:8000/book/book/check_isbn/?isbn=${isbn}`);
            const bookData = checkResponse.data;

            if (bookData.length > 0) {
                this.autofillFields(bookData[0]);
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error('Error checking ISBN', error);
        }
    }

    static async createBook() {
        const bookForm = document.getElementById('new-book-form');
        if (bookForm) {
            bookForm.addEventListener('submit', async (event) => {
                event.preventDefault();
    
                const formData = new FormData(bookForm);
                const isbn = formData.get('isbn');
                const data = {
                    isbn: isbn,
                    title: formData.get('title'),
                    author: formData.get('author'),
                    genre: formData.get('genre'),
                    edition: formData.get('edition'),
                    synopsis: formData.get('synopsis'),
                };
    
                try {
                    const isbnExists = await this.checkIsbn(isbn);
    
                    const response = await axios.post('http://127.0.0.1:8000/book/book/', data, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
    
                    if (response.status === 201){
                        const bookId = response.data.id;
    
                        if (!isbnExists){
                            const coverFile = formData.get('cover');
                            const resizedFile = await resizeBookCover(coverFile);
    
                            const coverFormData = new FormData();
                            coverFormData.append('cover_image', resizedFile);
    
                            const coverResponse = await axios.post(`http://127.0.0.1:8000/book/covers/${bookId}/cover/`, coverFormData, {
                                headers: {
                                    'Content-Type': 'multipart/form-data'
                                }
                            });
    
                            if (coverResponse.status === 201){
                                console.log('Cover added successfully');
                            }
                        }
                        else{
                            console.log('This book already has a cover');
                        }
    
                        alert('Book added successfully');
                        return response.data;
                    }
                } catch (error) {
                    console.error('Error creating book', error);
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
        const isbnField = document.getElementById('isbn');
        isbnField.addEventListener('blur', async ()=>{
            const isbn = isbnField.value;
            if(isbn){
                const isbnExists = await NewBookController.checkIsbn(isbn);
                if(!isbnExists){
                    NewBookController.autofillFields({});
                }
            }
        })
    });

    observeElement('new-genre-form', async () => {
        NewBookController.createGenre();
    });

});
