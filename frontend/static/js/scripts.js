const airline_types = ["support", "admin", "operations"]
const airport_types = ["gate", "check-in"]

async function flashMessage(message) { // Displays a flash message
    console.log(`Flashing message ${message}`)
    const container = document.getElementById("flash-container");

    const msg = document.createElement("div");
    msg.className = "flash-message";
    msg.textContent = message;

    container.appendChild(msg);

    setTimeout(() => {
        msg.remove();
    }, 3000);
}

async function toggleModal(modal_id) { // Toggles the visibility of the given modal
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

async function adminAddStaffTypeChange() { // Toggles if the phone or airport ICAO entry is visible
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

async function addStaffUser() {
    event.preventDefault()

    var first_name = document.querySelector("#add-staff-first-name").value
    var email = document.querySelector("#add-staff-email").value
    var staff_type = document.querySelector("#add-staff-type").value
    var last_name = document.querySelector("#add-staff-last-name").value
    var password = document.querySelector("#add-staff-password").value
    var phone = document.querySelector("#add-staff-phone").value
    var airport_icao = document.querySelector("#add-staff-airport").value

    if (airline_types.includes(staff_type)) { // Send request to add airline employee endpoint
        response = await fetch("/api/add-airline-employee", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "password": password,
                "staff_type": staff_type
            })
        })
    } else if (airport_types.includes(staff_type)) { // Send request to add airport staff endpoint
        response = await fetch("/api/add-airport-staff", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "airport_icao": airport_icao,
                "password": password,
                "staff_type": staff_type
            })
        })
    } else {
        console.log("Invalid staff type has been given")
        flashMessage("Something went wrong adding the staff user. Please contact support.")
    }

    response_json = await response.json()
    console.log(response)

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace("/employee/admin")
    }
    else {
        console.log("Information incorrect, flashing error.")

        flashMessage(response_json.message)
    }
}