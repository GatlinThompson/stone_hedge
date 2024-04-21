const setPosition= () => {
    let scrollPosition = sessionStorage.getItem('scrollPosition');
    console.log(scrollPosition)
    if (scrollPosition !== null) {
        window.scrollTo({
            top: parseInt(scrollPosition),
            behavior: 'instant'
        });
        sessionStorage.removeItem('scrollPosition');
    }
};

setPosition()

const forms = document.querySelectorAll('form')

forms.forEach(form = (el) => {

    el.addEventListener('submit', ()=> {
        sessionStorage.setItem('scrollPosition', window.scrollY);

    })
})

const deleteButtons = document.querySelectorAll('.delete_btn_static')

deleteButtons.forEach(deleteButton = (el) => {
    el.addEventListener('click', () => {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    })
})

