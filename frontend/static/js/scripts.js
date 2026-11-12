const airline_types = ["support", "admin", "operations"]
const airport_types = ["gate", "check-in"]

async function toggleModal(modal_id) {
    event.preventDefault()

    let opacity_cover = document.querySelector(".modal-cover")
    let modal = document.querySelector(modal_id)

    if (opacity_cover.style.display !== "flex") { // The modal is currently hidden
        opacity_cover.style.display = "flex"
        modal.style.display = "flex"
    } else { // The modal is currently displayed
        opacity_cover.style.display = "none"
        modal.style.display = "none"
    }

}

async function adminAddStaffTypeChange() {
    event.preventDefault()

    let staff_type = document.querySelector("#add-staff-type").value

    let phone_entry = document.querySelector("#add-staff-phone-label")
    let airport_entry = document.querySelector("#add-staff-airport-label")

    if (airline_types.includes(staff_type)) {
        airport_entry.style.display = "none"
        phone_entry.style.display = "block"
    } else if (airport_types.includes(staff_type)) {
        airport_entry.style.display = "block"
        phone_entry.style.display = "none"
    } else {
        console.log("Invalid staff type has been given")
    }
}