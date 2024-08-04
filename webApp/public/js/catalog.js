class CatalogController {
    static async listBooks(filters = {}) {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book/book/', { params: filters });
            return response.data;
        } catch (error) {
            console.error('Error fetching books', error);
        }
    }

    static async getGenre(genreId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/book/genre/${genreId}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching genre', error);
        }
    }

    static async getStock(bookId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/book/estoque/by-book/${bookId}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching stock', error);
        }
    }

    static async populateCatalog(filters = {}) {
        try {
            const books = await this.listBooks(filters);
            const bookList = document.getElementById('book-list');
            bookList.innerHTML = '';

            const booksToShow = books.slice(0, 12);

            for (const book of booksToShow) {
                const bookElement = document.createElement('div');
                bookElement.classList.add('book', 'book-list-item');

                let genreName = 'Unknown';
                if (book.genre) {
                    const genre = await this.getGenre(book.genre);
                    genreName = genre.name;
                }

                let stockQuantity = 'Unknown';
                const stock = await this.getStock(book.id);
                if (stock) {
                    stockQuantity = stock.quantity;
                }

                bookElement.innerHTML = `
                    <div class="book-title-container">
                        <h2 class="book-title">${book.title}</h2>
                    </div>
                    <div class="book-author">
                        <span class="book-author-item">
                            <i class="fas fa-user"></i> ${book.author}
                        </span>
                        <span class="book-author-item">
                            <i class="fas fa-edit"></i> ${book.edition}
                        </span>
                        <span class="book-author-item">
                            <i class="fas fa-layer-group"></i> ${genreName}
                        </span>
                        <span class="book-author-item">
                            <i class="fas fa-box"></i> Estoque: ${stockQuantity}
                        </span>
                    </div>
                    <div class="book-isbn">
                        <span class="book-isbn-item">
                            <i class="fas fa-barcode"></i> ISBN: ${book.isbn}
                        </span>
                    </div>
                    <footer class="book-footer">
                        <a href="../views/book-detail.html?id=${book.id}" class="book-read-more button button-dark button-full-width">
                            <i class="fas fa-eye"></i>
                        </a>
                    </footer>
                `;

                bookList.appendChild(bookElement);
            }
        } catch (error) {
            console.error('Error populating catalog', error);
        }
    }
    
    

    static async loadGenres() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book/genre/');
            const genres = response.data;
            const genreSelect = document.getElementById('search-genre');
            genreSelect.innerHTML = '<option value="">Todos os Gêneros</option>';

            genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre.id;
                option.textContent = genre.name;
                genreSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading genres', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    CatalogController.loadGenres();

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

    observeElement('book-list', async () => {
        await CatalogController.populateCatalog();
    });

    document.getElementById('search-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const title = document.getElementById('search-title').value.trim();
        const author = document.getElementById('search-author').value.trim();
        const edition = document.getElementById('search-edition').value.trim();
        const genre = document.getElementById('search-genre').value.trim();

        const filters = {};
        if (title) filters.title = title;
        if (author) filters.author = author;
        if (edition) filters.edition = edition;
        if (genre) filters.genre = genre;

        console.log('Search form submitted with filters:', filters);
        await CatalogController.populateCatalog(filters);
    });
});
