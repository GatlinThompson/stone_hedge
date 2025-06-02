const searchBar = document.getElementById("search_item_input")
const itemDBRows = document.querySelectorAll(".item-db-row")

const querySearch = (el) => {

    const userSearch = el.target.value.toUpperCase().trim()

    itemDBRows.forEach(itemDBRow => {

        const itemDescription = itemDBRow.children[1].innerText.toUpperCase()
        const partNumber = itemDBRow.dataset.partNumber
        const isFound = (partNumber.includes(userSearch) || itemDescription.includes(userSearch))
        itemDBRow.style.display = isFound ? 'table-row' : 'none'
    })

    let oneSearchFound = false

    itemDBRows.forEach(itemDBRow => {
        if (itemDBRow.style.display === 'table-row') {
            oneSearchFound = true
            return
        }
    })

    const noResults = document.getElementById("no_results_found")
    noResults.style.display = oneSearchFound ? 'none' : 'block'


}

searchBar.addEventListener('keyup', querySearch)
