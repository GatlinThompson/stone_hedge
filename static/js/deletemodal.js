const deleteModal = document.getElementById("confirmation_delete_modal")
const closeModalButton = document.getElementById("close_delete_modal")
const closeModalBtn = document.getElementById("close_delete_modal_btn")
const deleteLink = document.getElementById("delete_link")
const deleteModalItem = document.getElementById("delete_modal_item")


        const deleteItem = (id, name, el) => {
            console.log(el)
            const deleteURL = el.dataset.submitLink
            console.log(deleteURL)
            deleteModal.classList.add("show")
            deleteLink.href = `${deleteURL}`
            deleteModalItem.innerText = `${name}`
        }

        const closeDelete = () => {
             deleteLink.href = "#"
            deleteModal.classList.remove("show")
            deleteModalItem.innerText = `No Item Selected`
        }

        closeModalButton.addEventListener("click", closeDelete)
        closeModalBtn.addEventListener("click", closeDelete)