class BookDetailController {

    static async getBookById(bookId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/book/book/${bookId}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching book', error);
        }
    }

    static getCover(book) {
        try {
            const coverImage = book.covers.length > 0 ? book.covers[0].cover_image : '';
            const coverUrl = coverImage.startsWith('http://') || coverImage.startsWith('https://') ? coverImage : `http://127.0.0.1:8000${coverImage}`;
            return coverUrl;
        } catch (error) {
            console.error('Error fetching cover', error);
        }
    }

    static async getGenre(genreId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/book/genre/${genreId}/`);
            return response.data.name;
        } catch (error) {
            console.error('Error fetching genre', error);
            return 'Unknown';
        }
    }

    static async showBookDetail() {
        const urlParams = new URLSearchParams(window.location.search);
        const bookId = urlParams.get('id');

        if (bookId) {
            try {
                const book = await this.getBookById(bookId);
                const bookCover = this.getCover(book);
                const genreName = await this.getGenre(book.genre);
                const bookDetailContainer = document.getElementById('book-detail');

                bookDetailContainer.innerHTML = `
                    <div class="book-detail-container">
                        <div class="book book-list-item">
                            <div class="book-cover">
                                <img src="${bookCover}" alt="book-cover">
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
                            </div>
                        </div>
                        <div class="book-synopsis">
                            <h3>Synopsis</h3>
                            <p>${book.synopsis}</p>
                        </div>
                        <div class="book-actions">
                            <button class="reserve-button" id="reserve-button">Reserve</button>
                            <button class="borrow-button" id="borrow-button">Borrow</button>
                        </div>
                    </div>
                `;

                document.getElementById('reserve-button').addEventListener('click', () => {
                    window.location.href = `../views/reserve.html?id=${book.id}`;
                });

                document.getElementById('borrow-button').addEventListener('click', () => {
                    window.location.href = `../views/borrow.html?id=${book.id}`;
                });

            } catch (error) {
                console.error('Error getting book detail', error);
                alert('Error getting book detail');
            }
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

    observeElement('book-detail', async () => {
        await BookDetailController.showBookDetail();
    });
});