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
loadingElement.className = "loading-element"
var loadingTextNode = document.createTextNode("Loading songs ...")
loadingElement.appendChild(loadingTextNode)
songPairContainer.appendChild(loadingElement)

// Create div for each song in a pair
var songOneContainer = document.createElement("div")
songOneContainer.className = "song"
var songTwoContainer = document.createElement("div")
songTwoContainer.className = "song"

// SONG ONE:
// Create elements for song one
var imageSongOne = document.createElement("img")
imageSongOne.id = "ImageOne"
imageSongOne.width = "250"
imageSongOne.height = "250"
// Create option to select left song
var optionOneBtn = document.createElement("button")
optionOneBtn.id = "optionOneBtn"
var anchorOne = document.createElement("a")
var anchorOneTexNode = document.createTextNode("Song A")
anchorOne.appendChild(anchorOneTexNode)
optionOneBtn.appendChild(anchorOne)
// Create button to reveal details about left song
var revealOneBtn = document.createElement("button")
revealOneBtn.id = "revealOneBtn"
var revealOneText = document.createTextNode("Details")
revealOneBtn.appendChild(revealOneText)
// Left song details
var songOneDesc = document.createElement("div")
songOneDesc.className = "song-description"
var songOneNameTag = document.createElement("h1")
var songOneArtistTag = document.createElement("h3")
songOneDesc.appendChild(songOneNameTag)
songOneDesc.appendChild(songOneArtistTag)
// Append elements to the container
songOneContainer.appendChild(imageSongOne)
songOneContainer.appendChild(optionOneBtn)
songOneContainer.appendChild(revealOneBtn)
songOneContainer.appendChild(songOneDesc)
songPairContainer.appendChild(songOneContainer)

// SONG TWO
// Create elements for song two
var imageSongTwo = document.createElement("img")
imageSongTwo.id = "ImageTwo"
imageSongTwo.width = "250"
imageSongTwo.height = "250"
// Create option to select right song
var optionTwoBtn = document.createElement("button")
optionTwoBtn.id = "optionTwoBtn"
var anchorTwo = document.createElement("a")
var anchorTwoTexNode = document.createTextNode("Song B")
anchorTwo.appendChild(anchorTwoTexNode)
optionTwoBtn.appendChild(anchorTwo)
// Create button to reveal details about right song
var revealTwoBtn = document.createElement("button")
revealTwoBtn.id = "revealTwoBtn"
var revealTwoText = document.createTextNode("Details")
revealTwoBtn.appendChild(revealTwoText)
// Right osng details
var songTwoDesc = document.createElement("div")
songTwoDesc.className = "song-description"
var songTwoNameTag = document.createElement("h1")
var songTwoArtistTag = document.createElement("h3")
songTwoDesc.appendChild(songTwoNameTag)
songTwoDesc.appendChild(songTwoArtistTag)
// Append elements to the container
songTwoContainer.appendChild(imageSongTwo)
songTwoContainer.appendChild(optionTwoBtn)
songTwoContainer.appendChild(revealTwoBtn)
songTwoContainer.appendChild(songTwoDesc)
songPairContainer.appendChild(songTwoContainer)

// Hide elements until songs load
songOneDesc.style.display = "none"
songOneContainer.style.display = "none"
songTwoDesc.style.display = "none"
songTwoContainer.style.display = "none"

// Display given song pair to window
async function display(pairData){
	songOneDesc.style.display = "none"
	songTwoDesc.style.display = "none"

	// Parse through data

	// SONG ONE:
	songOneName= songPair[0]["name"]
	songOneImage = songPair[0]["cover_image"]
	songOnePreviewURL = songPair[0]["preview_url"
	]
	songOneNameTag.textContent = songOneName
	// Parse through list of artists
	var artistList = ""
	for(let i = 0; i < songPair[0]["artists"].length; i++){
		if(i === 0){
			artistList += songPair[0]["artists"][i]["name"]
		}
		else{
			artistList += ", " + songPair[0]["artists"][i]["name"]
		}
	}
	songOneArtistTag.textContent = artistList

	// SONG TWO
	songTwoName = songPair[1]["name"]
	songTwoImage = songPair[1]["cover_image"]
	songTwoPreviewURL = songPair[1]["preview_url"]
	songTwoNameTag.textContent = songTwoName
	// Parse through list of artists
	var artistList = ""
	for(let i = 0; i < songPair[1]["artists"].length; i++){
		if(i === 0){
			artistList += songPair[1]["artists"][i]["name"]
		}
		else{
			artistList += ", " + songPair[1]["artists"][i]["name"]
		}
	}
	songTwoArtistTag.textContent = artistList
	
	// Update elements 
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
		songOneContainer.style.display = "flex"
		songTwoContainer.style.display = "flex"

		// Display the a pair of songs
		display(songPair)

		// Results
		var results = {}

		// If song on tbe left is selected
		optionOneBtn.addEventListener("click", () => {
			// If there are no more song pairs reload the site
			if(index > total_pairs - 2){
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
			if(index > total_pairs - 2){
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
			imageSongOne.style.border = "3px solid green";
			audio.play()
			imageSongOne.addEventListener("mouseleave", ()=>{
				audio.pause();
				imageSongOne.style.border = "";
			});
		});
		// Plays audio clip for right song on hover
		imageSongTwo.addEventListener("mouseenter", ()=>{
			var audio = new Audio(songPair[1]["preview_url"]);
			imageSongTwo.style.border = "3px solid orange";
			audio.play()
			imageSongTwo.addEventListener("mouseleave", ()=>{
				audio.pause();
				imageSongTwo.style.border = "";
			});
		});

		// Reveal details of left song
		revealOneBtn.addEventListener("click", () => {
			if(songOneDesc.style.display === "none"){
				songOneDesc.style.display = "flex"
			}
			else{
				songOneDesc.style.display = "none"
			}
			
		});
		// Reveal details of right song
		revealTwoBtn.addEventListener("click", () => {
			if(songTwoDesc.style.display === "none"){
				console.log("Asdasd")
				songTwoDesc.style.display = "flex"

			}
			else{
				songTwoDesc.style.display = "none"
			}
		})
	})
	.catch(err => console.log("Rejected", err))