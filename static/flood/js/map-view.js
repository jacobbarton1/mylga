function initMap() {
    const mapOptions = {
        zoom: 8,
        center: { lat: -26.2, lng: 146.6 }, // Centre on Charleville
        mapId: "DEMO_MAP_ID",
        gestureHandling: "greedy",
    };

    const map = new google.maps.Map(document.getElementById("map"), mapOptions);
    const infoWindow = new google.maps.InfoWindow();

    fetch("/flood/api/uplinks/", {
        method: "GET",
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (json_data) {
            for (const [key, item] of Object.entries(json_data)) {
                let background;
                let glyphColor;
                let glyphScale = 1.25;
                let textScale = "12px";
                let minutes_since_last_uplink = parseInt(
                    item.minutes_since_last_uplink
                );

                if (minutes_since_last_uplink > 60 * 12) {
                    background = "#a6a6a6";
                    glyphColor = "#000000";
                } else if (item.level_state === "high_high") {
                    background = "#FF0000";
                    glyphColor = "#FFFFFF";
                    glyphScale = 2.0;
                    textScale = "18px";
                } else if (item.level_state === "high") {
                    background = "#E28743";
                    glyphColor = "#000000";
                    glyphScale = 2.0;
                    textScale = "18px";
                } else if (item.level_state === "low") {
                    background = "#ffff99";
                    glyphColor = "#000000";
                } else if (item.level_state === "low_low") {
                    background = "#ffffe6";
                    glyphColor = "#000000";
                } else {
                    background = "#616569";
                    glyphColor = "#000000";
                }

                const label = document.createElement("div");
                label.innerHTML = parseFloat(item.distance).toFixed(0);
                label.style.fontSize = textScale;
                label.style.fontWeight = "bold";

                const pinGlyph = new google.maps.marker.PinElement({
                    glyph: label,
                    glyphColor: glyphColor,
                    scale: glyphScale,
                    background: background,
                });

                const marker = new google.maps.marker.AdvancedMarkerElement({
                    position: {
                        lat: parseFloat(item.lat),
                        lng: parseFloat(item.lng),
                    },
                    map: map,
                    title: `${key}`,
                    content: pinGlyph.element,
                    gmpClickable: true,
                });

                marker.addListener("click", ({ domEvent }) => {
                    infoWindow.close();

                    const localDate = new Date(item.timestamp);

                    let info =
                        "<p>" +
                        item.location +
                        "  [" +
                        key +
                        "]<br>" +
                        "Location: (" +
                        parseFloat(item.lat).toFixed(6) +
                        "," +
                        parseFloat(item.lng).toFixed(6) +
                        ")<br>" +
                        "Height: " +
                        parseFloat(item.distance) +
                        "mm<br>" +
                        "Battery:  " +
                        (item.battery ?? "") +
                        "v<br>" +
                        "Signal:  " +
                        (item.signal ?? "") +
                        "<br>" +
                        "Last Update: " +
                        localDate.toLocaleString() +
                        "<br>" +
                        "<a href='/flood/plot/" +
                        key +
                        "'>Plot 7 Day History</a>" +
                        "</p>";
                    infoWindow.setContent(info);
                    infoWindow.open(marker.map, marker);
                });
            }
        });
}

window.initMap = initMap;

