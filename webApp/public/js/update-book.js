function fillBookData(bookData, genreData) {
    document.getElementById('isbn').value = bookData.isbn || '';
    document.getElementById('title').value = bookData.title || '';
    document.getElementById('author').value = bookData.author || '';
    document.getElementById('edition').value = bookData.edition || '';
    document.getElementById('synopsis').value = bookData.synopsis || '';

    const genreSelect = document.getElementById('genre');

    genreSelect.innerHTML = '';

    if (genreData && genreData.length > 0) {
        genreData.forEach(genre => {
            const option = new Option(genre.name, genre.id);
            genreSelect.add(option);
        });

        genreSelect.value = bookData.genre;
    }
}

function resizeBookCover(cover) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = 348;
                canvas.height = 500;

                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                canvas.toBlob((blob) => {
                    if (blob) {
                        resolve(new File([blob], cover.name, { type: 'image/jpeg' }));
                    } else {
                        reject(new Error('Failed to create blob from canvas'));
                    }
                }, 'image/jpeg');
            };
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(cover);
    });
}
class UpdateBookController {
    static async fetchData(url) {
        try {
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            console.error(`Error fetching data from ${url}`, error);
            alert('Error fetching data');
        }
    }

    static async getBookById(bookId) {
        return this.fetchData(`http://127.0.0.1:8000/book/book/${bookId}/`);
    }

    static async listGenres() {
        return this.fetchData('http://127.0.0.1:8000/book/genre/');
    }

    static async populateGenres() {
        return this.listGenres();
    }

    static async updateBook() {
        const urlParams = new URLSearchParams(window.location.search);
        const bookId = urlParams.get('id');
        const formData = new FormData(document.getElementById('update-book-form'));

        const bookData = {
            isbn: formData.get('isbn'),
            title: formData.get('title'),
            genre: formData.get('genre'),
            author: formData.get('author'),
            edition: formData.get('edition'),
            synopsis: formData.get('synopsis')
        };

        try {
            await axios.patch(`http://127.0.0.1:8000/book/book/${bookId}/`, bookData);

            const coverFile = formData.get('cover');
            if (coverFile && coverFile.size > 0) {
                const resizedFile = await resizeBookCover(coverFile);

                const coverFormData = new FormData();
                coverFormData.append('cover_image', resizedFile);

                await axios.post(`http://127.0.0.1:8000/book/covers/${bookId}/update_cover/`, coverFormData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            }
            alert('Book updated successfully');
        } catch (error) {
            console.error('Error updating book', error);
            alert('Error updating book');
        }
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const bookId = urlParams.get('id');

    if (bookId) {
        const genres = await UpdateBookController.populateGenres();
        const bookData = await UpdateBookController.getBookById(bookId);
        fillBookData(bookData, genres);
    }

    document.getElementById('update-book-form')?.addEventListener('submit', async (event) => {
        event.preventDefault();
        await UpdateBookController.updateBook();
    });
});