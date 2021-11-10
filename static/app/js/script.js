ROOT_URL = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port

// Get song pairs 
const getSongPairs = async () => {
	const response = await fetch(ROOT_URL + "/find/")
	if(response.status !== 200){
		throw new Error("Cannot fetch requested resource");
	}
	const data = await response.json()
	return data
};

let songPairContainer = document.querySelector(".song-pair-container")
const loadingElement = document.createElement("h1")
var textnode = document.createTextNode("Loading songs ...")
loadingElement.appendChild(textnode)

songPairContainer.appendChild(loadingElement)

// while (true){
// 	getSongPairs()
// 		.then(data => console.log("Resolved", data))
// 		.catch(err => console.log("Rejected", err));

	
// }
