// ! Global functions
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


// ! Page specific functions

// Admin Portal

async function showStaffTable() {
    // TODO: make switch the add use modal
    response = await fetch("/api/get-staff-users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })

    response_json = await response.json()
    console.log(response_json)

    let table_container = document.querySelector("#admin-users-list-container")
    table_container.innerHTML = ""

    for (let i = 0; i < response_json.content.length; i++) {
        user = response_json.content[i]

        new_user_card = document.createElement("div")
        new_user_card.className = "admin-user-item"

        name_label = document.createElement("label")
        name_label.textContent = `${user[3]} ${user[4]}`
        new_user_card.appendChild(name_label)

        email_label = document.createElement("label")
        email_label.textContent = `${user[5]}`
        new_user_card.appendChild(email_label)

        type_label = document.createElement("label")
        type_label.textContent = `${user[0]}`
        new_user_card.appendChild(type_label)

        id_label = document.createElement("label")
        id_label.textContent = `${user[2]}`
        new_user_card.appendChild(id_label)

        button_div = document.createElement("div") // TODO: Add functionality to admin table buttons in JS as well as HTML
        edit_button = document.createElement("button")
        edit_button.textContent = "Edit"
        button_div.appendChild(edit_button)
        delete_button = document.createElement("button")
        delete_button.textContent = "Delete"
        button_div.appendChild(delete_button)
        new_user_card.appendChild(button_div)

        table_container.appendChild(new_user_card)
    }
}

async function showGuestTable() {
    // TODO: make switch the add use modal
    response = await fetch("/api/get-guest-users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })

    response_json = await response.json()
    console.log(response_json)

    let table_container = document.querySelector("#admin-users-list-container")
    table_container.innerHTML = ""

    for (let i = 0; i < response_json.content.length; i++) {
        user = response_json.content[i]

        new_user_card = document.createElement("div")
        new_user_card.className = "admin-user-item"

        id_label = document.createElement("label")
        id_label.textContent = `${user[0]}`
        new_user_card.appendChild(id_label)

        name_label = document.createElement("label")
        name_label.textContent = `${user[1]} ${user[2]}`
        new_user_card.appendChild(name_label)

        email = document.createElement("label")
        email.textContent = `${user[3]}`
        new_user_card.appendChild(email)

        button_div = document.createElement("div") // TODO: Add functionality to admin table buttons in JS as well as HTML
        edit_button = document.createElement("button")
        edit_button.textContent = "Edit"
        button_div.appendChild(edit_button)

        delete_button = document.createElement("button")
        delete_button.textContent = "Delete"
        delete_button.addEventListener("click", function () { deleteGuest(user[0]); })

        button_div.appendChild(delete_button)
        new_user_card.appendChild(button_div)

        table_container.appendChild(new_user_card)
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

async function deleteGuest(guest_id) {
    console.log(`Deleting guest ${guest_id}`)

    response = await fetch("/api/delete-guest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "id": guest_id
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        showGuestTable() // Clear and redraw table with user deleted
    } else {
        console.log("Delete failed, flashing error.")
        flashMessage(response_json.message)
    }
}

async function deleteStaff(table, id) {
    console.log(`Deleting guest ${guest_id}`)

    response = await fetch("/api/delete-staff", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "table": table,
            "id": id
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        showStaffTable() // Clear and redraw table with user deleted
    } else {
        console.log("Delete failed, flashing error.")
        flashMessage(response_json.message)
    }
}

// Login
async function login() {
    event.preventDefault()

    let email = document.querySelector("#email").value
    let password = document.querySelector("#password").value

    let response = await fetch("/api/check-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "email": email,
            "password": password
        })
    })

    let response_json = await response.json()

    if (response_json.code == 200) {
        if (response_json.page == "guest") {
            console.log("Redirecting to guest page") // TODO: Make login redirect to guest page
            window.location.replace("/")
        } else if (response_json.page == "support") {
            console.log("Redirecting to customer support page") // TODO: Make login redirect to customer support page
        } else if (response_json.page == "operations") {
            console.log("Redirecting to flight operations manager portal") // TODO: Make login redirect to flight operations page
        } else if (response_json.page == "admin") {
            console.log("Redirecting to admin portal")
            window.location.replace("/employee/admin")
        } else if (response_json.page == "gate") {
            console.log("Redirecting to gate agent portal") // TODO: Make login redirect to gate agent page
        } else if (response_json.page == "check-in") {
            console.log("Redirecting to check-in agent portal") // TODO: Make login redirect to check-in agent page
        }
    }
    else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}

// Create account
async function createGuestAccount() { // Create a guest account can be used in the create account page or admin add guest
    // TODO: Use this function to add guests from admin portal
    event.preventDefault()

    var first_name = document.querySelector("#first-name").value
    var last_name = document.querySelector("#last-name").value
    var email = document.querySelector("#email").value
    var phone = document.querySelector("#phone").value
    var password = document.querySelector("#password").value
    var repeat_password = document.querySelector("#repeat-password").value

    if (password !== repeat_password) {
        flashMessage("Your password do not match")
    } else {
        response = await fetch("/api/add-guest", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "password": password
            })
        })

        response_json = await response.json()
        console.log(response)

        if (response_json.code == 200) {
            console.log("Information correct, redirecting.")
            window.location.replace("/login")
        }
        else {
            console.log("Information incorrect, flashing error.")

            flashMessage(response_json.message)
        }
    }
}


// Flight Operations Routes
async function addRoute() {
    event.preventDefault()

    var origin = document.querySelector("#add-route-origin").value
    var destination = document.querySelector("#add-route-destination").value
    var price = document.querySelector("#add-route-price").value

    response = await fetch("/api/add-route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "origin": origin,
            "destination": destination,
            "price": price
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace("/employee/operations")
    } else {
        console.log("Information incorrect, flashing error.")

        flashMessage(response_json.message)
    }
}

// Flight operations details
async function addOneOffFLight(routeID) {
    event.preventDefault()

    var date_time = document.querySelector("#add-flight-datetime").value

    response = await fetch("/api/add-one-off-flight", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "routeID": routeID,
            "departureDatetime": date_time
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace(`/employee/operations/route-details/${routeID}`)
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}

async function operationsChangeScheduleRepeatType() {
    var repeat_type = document.querySelector("#add-schedule-repeat-type").value
    let weekly_repeat_on = document.querySelector("#add-schedule-repeat-on-week")
    let monthly_repeat_on = document.querySelector("#add-schedule-repeat-on-month")

    if (repeat_type == "daily") {
        weekly_repeat_on.disabled = true
        monthly_repeat_on.disabled = true

    } else if (repeat_type == "weekly") {
        weekly_repeat_on.disabled = false
        monthly_repeat_on.classList = ["hidden"]
        weekly_repeat_on.classList = []

    } else if (repeat_type == "monthly") {
        monthly_repeat_on.disabled = false
        weekly_repeat_on.display = "none"
        monthly_repeat_on.classList = []
        weekly_repeat_on.classList = ["hidden"]
    }
}

async function addSchedule(routeID) {
    event.preventDefault()

    var start_date = document.querySelector("#add-schedule-start").value
    var end_date = document.querySelector("#add-schedule-end").value
    var schedule_time = document.querySelector("#add-schedule-time").value
    var repeat_type = document.querySelector("#add-schedule-repeat-type").value
    var repeat_frequency = document.querySelector("#add-schedule-frequency").value

    if (repeat_type == "weekly") {
        var repeat_on = document.querySelector("#add-schedule-repeat-on-week").value
    } else if (repeat_type == "monthly") {
        var repeat_on = document.querySelector("#add-schedule-repeat-on-month").value
    } else {
        repeat_on = null
    }

    response = await fetch("/api/add-schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "routeID": routeID,
            "startDate": start_date,
            "endDate": end_date,
            "repeatType": repeat_type,
            "frequency": repeat_frequency,
            "repeatTime": schedule_time,
            "repeatsOn": repeat_on
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace(`/employee/operations/route-details/${routeID}`)
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}