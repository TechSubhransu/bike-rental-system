document.addEventListener("DOMContentLoaded", function () {
    const bookingsContainer = document.getElementById("bookings");

    fetch("http://127.0.0.1:8000/api/bookings/")   // your API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            bookingsContainer.innerHTML = ""; // clear before showing
            data.forEach(booking => {
                const div = document.createElement("div");
                div.classList.add("booking-card");
                div.innerHTML = `
                    <h3>🚲 ${booking.bike_details.bike_name}</h3>
                    <img src="${booking.bike_details.photo}" alt="${booking.bike_details.bike_name}" width="200">
                    <p><b>Company:</b> ${booking.bike_details.company}</p>
                    <p><b>Pickup:</b> ${booking.pickup_date} ${booking.pickup_time}</p>
                    <p><b>Drop:</b> ${booking.drop_date} ${booking.drop_time}</p>
                    <p><b>Status:</b> ${booking.status}</p>
                `;
                bookingsContainer.appendChild(div);
            });
        })
        .catch(error => {
            console.error("Error fetching bookings:", error);
            bookingsContainer.innerHTML = "<p style='color:red;'>❌ Failed to load bookings</p>";
        });
});
