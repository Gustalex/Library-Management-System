class HomeController {
    static async getTrendingBooks() {
        console.log('Getting trending books');
        try {
            const response = await axios.get('http://127.0.0.1:8000/book-services/popular/');
            HomeController.updateTrendingBooks(response.data);
        } catch (error) {
            console.error('Error getting trending books', error);
            alert('Error getting trending books');
        }
    }

    static updateTrendingBooks(books) {
        const trendingBooksList = document.getElementById('trending-books-list');
        trendingBooksList.innerHTML = '';

        books.forEach(book => {
            const bookElement = document.createElement('div');
            bookElement.classList.add('book', 'book-list-item');

            const coverImage = book.covers.length > 0 ? `http://127.0.0.1:8000${book.covers[0].cover_image}` : '';
            const genreName = book.genre ? book.genre.name : '';

            bookElement.innerHTML = `
                <div class="book-cover">
                    <img src="${coverImage}" alt="book-cover">
                </div>
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
                    <footer class="book-footer">
                        <a href="#" class="book-read-more button button-dark button-full-width">
                            <i class="fas fa-book-reader"></i>
                        </a>
                    </footer>
                </div>
            `;

            trendingBooksList.appendChild(bookElement);
        });
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

    observeElement('trending-books-list', async () => {
        await HomeController.getTrendingBooks();
    });
});
