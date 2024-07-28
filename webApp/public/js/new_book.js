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
                const data = {
                    title: formData.get('title'),
                    author: formData.get('author'),
                    genre: formData.get('genre'),
                    edition: formData.get('edition'),
                    synopsis: formData.get('synopsis'),
                };
    
                console.log('Dados do livro:', data);
    
                try {
                    const response = await axios.post('http://127.0.0.1:8000/book/book/', data, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    if (response.status === 201) {
                        const bookId = response.data.id;
                        console.log('Livro criado com id:', bookId);
    
                        const coverFile = formData.get('cover');
                        const resizedFile = await resizeBookCover(coverFile);
    
                        const coverFormData = new FormData();
                        coverFormData.append('cover_image', resizedFile);
    
                        console.log('Capa do livro redimensionada:', resizedFile);
    
                        const coverResponse = await axios.post(`http://127.0.0.1:8000/book/covers/${bookId}/cover/`, coverFormData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        });
                        if (coverResponse.status === 201) {
                            console.log('Capa do livro carregada com sucesso');
                        }
                        alert('Livro criado com sucesso');
                        return response.data;
                    }
                }catch(error){
                    console.error('Erro ao criar livro:', error);
                    alert('Erro ao criar livro');
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
