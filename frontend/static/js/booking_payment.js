async function payBooking(booking_id) {
    event.preventDefault()

    response = await fetch("/api/pay-booking", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "bookingID": Number(booking_id),
        })
    })

    response_json = await response.json()
    console.log(response_json)

    if (response_json.code == 200) {
        console.log("Information correct, redirecting.")
        window.location.replace(`/`) // TODO: Make redirect to a thank you, profile, or your booking page
    } else {
        console.log("Information incorrect, flashing error.")
        flashMessage(response_json.message)
    }
}