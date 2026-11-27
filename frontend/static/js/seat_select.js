let companions = [] // used to store all the companions and associated seats that are to be added on move to next page
let current_assigning_companion = 0 // used to dictate which index in the companions list is being updated next
let companion_index = 0 // The ID identifier for companions added to the flight, does not decrement when companion removed. Used to solve the issue of a companion being allowed to hold multiple seats, sort of like a temporary PK for booking seat.

async function toggleAddCompanionSelect() { // Toggles the visibility of the select companion menu
    let modal = document.querySelector("#add-companion-select")
    if (modal.style.display != "flex") {
        modal.style.display = "flex"
    } else {
        modal.style.display = "none"
    }
}

async function addCompanion(companion_id, already_in_list = false,) { // adds the given companion to the companions list with no assigned seat
    companions.push([companion_index, Number(companion_id), null])
    companion_index += 1
    console.log(companions)

    if (already_in_list == false) { // Show in GUI with DOM
        response = await fetch("/api/get-companion-details", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "companionID": companion_id
            })
        })

        response_json = await response.json()

        console.log(response_json)

        let companion_list_container = document.querySelector("#companions-list-container")

        let new_companion_card = document.createElement("div")
        new_companion_card.classList = "seat-select-companion-card"

        new_companion_card.innerHTML = `
        <div>
            <h4>${response_json.content[2]}</h4>
            <label>${response_json.content[4]}</label>
        </div>
        <div class="seat-select-companion-card-right-details">
            <div class="inline">
                <svg class="hidden" id="companion-seat-indicator-${companion_index - 1}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                height="24px" width="24px"
                    fill="#000000">
                    <path d="M10,17V7l5,5l-5,5Z" />
                </svg>
                <label id="companion-seat-${companion_index - 1}">-</label>
            </div>
            <button class="remove-companion-seat-select-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" height="48px" width="48px"
                    fill="#FFFFFF">
                    <path
                        d="M12.45,37.65l-2.1-2.1L21.9,24L10.35,12.45l2.1-2.1L24,21.9L35.55,10.35l2.1,2.1L26.1,24L37.65,35.55l-2.1,2.1L24,26.1L12.45,37.65Z" />
                </svg>
            </button>
        </div>
        `

        companion_list_container.appendChild(new_companion_card)
    }

    // TODO: Update price on adding a companion
}

async function assignSeat(seatID) { // Assigns the clicked seat to the index of the companions list currently being edited
    if (companions[current_assigning_companion][2] !== null) {
        let old_seat = document.querySelector(`#seat-${companions[current_assigning_companion][2]}`)
        old_seat.classList = "seat-button-available"
        old_seat.disabled = false
    }

    let companion_card_seat_label = document.querySelector(`#companion-seat-${companions[current_assigning_companion][0]}`)
    companion_card_seat_label.textContent = seatID

    console.log(`Seat identifier to turn off: ${companions[current_assigning_companion][0]}`)
    let companion_card_seat_arrow = document.querySelector(`#companion-seat-indicator-${companions[current_assigning_companion][0]}`)
    companion_card_seat_arrow.classList = "hidden"


    companions[current_assigning_companion][2] = seatID
    current_assigning_companion += 1

    if (current_assigning_companion > companions.length - 1) {
        current_assigning_companion = 0
    }

    console.log(`Seat identifier to turn on: ${companions[current_assigning_companion][0]}`)
    companion_card_seat_arrow = document.querySelector(`#companion-seat-indicator-${companions[current_assigning_companion][0]}`)
    companion_card_seat_arrow.classList = ""

    console.log(companions)
    console.log(`Current Assigning Companion (New): ${current_assigning_companion}`)

    let new_seat = document.querySelector(`#seat-${seatID}`)

    new_seat.classList = "seat-button-selected"
    new_seat.disabled = true

    // TODO: Update the items in the display DOM
}

async function newCompanion() { // Sends a create companion call to the API then adds companion to available companion list without refreshing page
    event.preventDefault()

    let name = document.querySelector("#add-companion-passport-name").value
    let pass_no = document.querySelector("#add-companion-passport-number").value
    let nationality = document.querySelector("#add-companion-passport-nationality").value
    let authority = document.querySelector("#add-companion-passport-authority").value
    let pass_exp = document.querySelector("#add-companion-passport-expiry").value
    let dob = document.querySelector("#add-companion-passport-dob").value
    let pass_sex = document.querySelector("#add-companion-passport-sex").value

    console.log(`INOP new companion ${name} ${pass_no} ${nationality} ${authority} ${pass_exp} ${dob} ${pass_sex}`)

    response = await fetch("/api/create-companion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "passport_name": name,
            "passport_expiry": pass_exp,
            "passport_number": pass_no,
            "dob": dob,
            "nationality": nationality,
            "passport_sex": pass_sex,
            "passport_authority": authority
        })
    })

    response_json = await response.json()

    console.log(response_json)

    if (response_json.code == 200) {
        let companion_selection = document.querySelector("#add-companion-select")

        let new_companion_avail = document.createElement("button")
        new_companion_avail.classList = "columns existing-companions-list-button"
        new_companion_avail.addEventListener("click", function () { addCompanion(`${response_json.content}`); })
        new_companion_avail.innerHTML = `< label > ${name}</label ><label>DOB: ${dob}</label><label>Expiry: ${pass_exp}</label>`

        companion_selection.appendChild(new_companion_avail)

        toggleModal('#new-companion-modal')
    } else {
        console.log("Information incorrect, flashing error")
        flashMessage(response_json.message)
    }
}

async function goToPayment(bookingID) { // Triggered on pressing the next button - sends an API request to add all of the companions to the booking then redirects window location
    response = await fetch("/api/add-initial-companions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "bookingID": Number(bookingID),
            "companions_list": companions
        })
    })

    response_json = await response.json()

    console.log(response_json)

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace(`/pay-booking/${bookingID}`)
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}