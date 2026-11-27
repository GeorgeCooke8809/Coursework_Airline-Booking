async function departAircraft(flight_id) { // Sends an API request to mark the flight as departed
    response = await fetch("/api/depart-aircraft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "flightID": flight_id
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace("/employee/gate-check-flights")
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}

async function markBoarded(booking_seat_id) { // Used by gate agents to mark a passenger as having boarded the aircraft
    response = await fetch("/api/board-seat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "bookingSeatID": booking_seat_id
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.reload()
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}

async function markArrived(booking_seat_id) { // Used by check-in agents to mark a passenger as arrived / checked in
    response = await fetch("/api/arrive-seat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "bookingSeatID": booking_seat_id
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.reload()
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}