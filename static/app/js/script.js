const ROOT_URL = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port

// Request lsit of song pairs from the find api endpoint
var getSongPairs = async () => {
	const response = await fetch(ROOT_URL + "/find/")
	if(response.status !== 200){
		throw new Error("Cannot fetch requested resource");
	}
	const data = await response.json()
	return data
};

var songPairContainer = document.querySelector(".song-pair-container")

// Create a loading element which displays before the songPairs are loaded in
const loadingElement = document.createElement("h1")
var loadingTextNode = document.createTextNode("Loading songs ...")
loadingElement.appendChild(loadingTextNode)
songPairContainer.appendChild(loadingElement)

// Create div for each song in a pair
var songOneContainer = document.createElement("div")
var songTwoContainer = document.createElement("div")

// Create elements for song one
var imageSongOne = document.createElement("img")
imageSongOne.id = "ImageOne"
imageSongOne.width = "200"
imageSongOne.width = "200"
var optionOneBtn = document.createElement("button")
optionOneBtn.id = "optionOneBtn"
var anchorOne = document.createElement("a")
var anchorOneTexNode = document.createTextNode("Choice 1")
anchorOne.appendChild(anchorOneTexNode)
optionOneBtn.appendChild(anchorOne)
songOneContainer.appendChild(imageSongOne)
songOneContainer.appendChild(optionOneBtn)
songPairContainer.appendChild(songOneContainer)

// Create elements for song two
var imageSongTwo = document.createElement("img")
imageSongTwo.id = "ImageTwo"
imageSongTwo.width = "200"
imageSongTwo.width = "200"
var optionTwoBtn = document.createElement("button")
optionTwoBtn.id = "optionTwoBtn"
var anchorTwo = document.createElement("a")
var anchorTwoTexNode = document.createTextNode("Choice 2")
anchorTwo.appendChild(anchorTwoTexNode)
optionTwoBtn.appendChild(anchorTwo)
songTwoContainer.appendChild(imageSongTwo)
songTwoContainer.appendChild(optionTwoBtn)

// Hide the options buttons
optionOneBtn.style.display = "none"
optionTwoBtn.style.display = "none"

songPairContainer.style.display = "flex"
songPairContainer.appendChild(songTwoContainer)

// Display given song pair
async function display(pairData){
	// Parse through data
	// Song one:
	songOneName= songPair[0]["name"]
	songOneImage = songPair[0]["cover_image"]
	songOnePreviewURL = songPair[0]["preview_url"]
	// Song Two:
	songTwoName= songPair[1]["name"]
	songTwoImage = songPair[1]["cover_image"]
	songTwoPreviewURL = songPair[1]["preview_url"]

	imageSongOne.src = songOneImage 
	imageSongTwo.src = songTwoImage
};

// On page load request the run:
// TODO: Remove choice buttons. ALlow users to select a song by clicking the cover image
window.onLoad = getSongPairs()
	.then(data => {

		// Total no of pairs
		var total_pairs = data["total_pairs"]

		// Get first song pair in data
		var index = 0
		songPair = data["pair_list"][index]

		// Hide loading element
		loadingElement.style.display = "none"

		// Display the option buttons
		optionOneBtn.style.display = "block"
		optionTwoBtn.style.display = "block"

		// Display the a pair of songs
		display(songPair)

		// Results
		var results = {}

		// If song on tbe left is selected
		optionOneBtn.addEventListener("click", () => {
			// If there are no more song pairs reload the site
			if(index > 23){
				location.reload();
			}
			else{
				index = index + 1
				songPair = data["pair_list"][index]
				display(songPair)
			}
		});

		// If song on the right is selected
		optionTwoBtn.addEventListener("click", () => {
			// If there are no more song pairs reload the site
			if(index > 23){
				location.reload();
			}
			else{
				index = index + 1
				songPair = data["pair_list"][index]
				display(songPair)
			}		
		})

		// Plays audio clip for left osng on hover 
		imageSongOne.addEventListener("mouseenter", ()=>{
			var audio = new Audio(songPair[0]["preview_url"]);
			// img.style.border = "2px solid green";
			audio.play()
			imageSongOne.addEventListener("mouseleave", ()=>{
				audio.pause();
				// img.style.border = "";
			});
		});

		// Plays audio clip for right song on hover
		imageSongTwo.addEventListener("mouseenter", ()=>{
			var audio = new Audio(songPair[1]["preview_url"]);
			// img.style.border = "2px solid green";
			audio.play()
			imageSongTwo.addEventListener("mouseleave", ()=>{
				audio.pause();
				// img.style.border = "";
			});
		});
	})
	.catch(err => console.log("Rejected", err))