const map = L.map('map').setView([58.40384776751319, 15.578484535217285], 15);
const form = document.querySelector('#path-form')
const markerIsStart = document.querySelector("#marker-point-start")
const markerIsEnd = document.querySelector("#marker-point-end")
form.addEventListener('submit', postShortestPath, false)


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

async function postShortestPath(event){
    event.preventDefault()
    var lat1 = parseFloat(document.querySelector('#lat1').value)
    var lng1 = parseFloat(document.querySelector('#lng1').value)
    var lat2 = parseFloat(document.querySelector('#lat2').value)
    var lng2 = parseFloat(document.querySelector('#lng2').value)

    // Check that they're not Nan (stops function if one is Nan)
    if(!lat1 || !lng1  || !lat2 || !lng2)
        return alert('Formatting Error: Coordinates are not float values.')

    req = {lat1, lng1, lat2, lng2} // Dictionary auto-keys

    res = await fetch('/shortest-path', {
        method:'POST',
        credentials: 'same-origin',
        body: JSON.stringify(req)
    })

    res = await res.json()
    console.log(res.path)
    var poly = L.polyline(res.path).addTo(map)
}

function handleMapClick ({latlng}){
    var {lat, lng} = latlng
    var marker = L.marker([lat, lng]).addTo(map)
    var posNumber = markerIsStart.checked ? '1' : '2'
    document.querySelector('#lat' + posNumber).value = lat
    document.querySelector('#lng' + posNumber).value = lng
    if(markerIsStart.checked)
        markerIsEnd.checked = true
}

map.on('click', handleMapClick)
