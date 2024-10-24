'use strict';

function imagePreviewHandler(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let img = document.querySelector('.background-preview > img') as HTMLImageElement;
            if (typeof e.target?.result == "string") {
                img.src = e.target?.result;
            }
            if (img.classList.contains('d-none')) {
                let label = document.querySelector('.background-preview > label');
                label?.classList.add('d-none');
                img.classList.remove('d-none');
            }
        }
        reader.readAsDataURL(target.files[0]);
    }
}

window.onload = function () {
    let background_img_field = document.getElementById('background_img');
    if (background_img_field) {
        background_img_field.addEventListener('change', imagePreviewHandler);
    }

    // @ts-ignore // md for book description textarea  
    const bookDescriptionEasyMDE = new EasyMDE({
        element: document.getElementById('description'),
        minHeight: "100px"
    });

    // @ts-ignore // md for review textarea 
    const reviewTextareaEasyMDE = new EasyMDE({
        element: document.getElementById('review-textarea'),
        minHeight: "100px"
    });

    // delete book button handler
    const btnDeleteBook = document.querySelectorAll(".btn-delete-book") as NodeListOf<HTMLButtonElement>;
    if (btnDeleteBook) {
        btnDeleteBook.forEach(btn => {
            btn.addEventListener("click", (event: MouseEvent) => {
                const deleteBookModalLabel = document.querySelector("#delete-book-modal-label") as HTMLLabelElement;
                const btnElement = event.target as Element;

                if (deleteBookModalLabel) {
                    const classList = btnElement.classList.toString().split(" ");
                    const bookClass = classList[classList.length - 1];
                    deleteBookModalLabel.textContent = `Вы уверены, что хотите удалить книгу «${bookClass.split("-").join(" ")}»?`;

                    const btnDeleteBookConfirm = document.querySelector(".btn-delete-book-confirm") as HTMLAnchorElement;
                    const bookId = classList[classList.length - 2].split("-")[1];
                    btnDeleteBookConfirm.href = `/book/delete/${bookId}`
                }
            });
        });
    }
}
