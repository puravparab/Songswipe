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
var loadingContainer = document.querySelector(".loading-container")
// Create a loading element which displays before the songPairs are loaded in
const loadingElement = document.createElement("h1")
loadingElement.className = "loading-element"
var loadingTextNode = document.createTextNode("Loading songs ...")
loadingElement.appendChild(loadingTextNode)
loadingContainer.appendChild(loadingElement)

// Create div for each song in a pair
var songOneContainer = document.createElement("div")
songOneContainer.className = "song"
var songTwoContainer = document.createElement("div")
songTwoContainer.className = "song"

///////////////
// SONG ONE: //
///////////////
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
// Create left song menu bar
var songOneBar = document.createElement("div")
songOneBar.className = "song-bar"
var saveL = document.createElement("img")
saveL.src = "/static/app/assets/images/svg/heart_black_outline.svg"
var saveLClicked = false
saveL.width = "30"
saveL.height = "30"
var plusIconL = document.createElement("img")
plusIconL.src = "/static/app/assets/images/svg/plus_black.svg"
plusIconL.width = "30"
plusIconL.height = "30"
var spotIconL = document.createElement("img")
spotIconL.src = "/static/app/assets/images/svg/spotify_green.svg"
spotIconL.width = "30"
spotIconL.height = "30"
var detailsBtnL = document.createElement("img")
detailsBtnL.src = "/static/app/assets/images/svg/chevron_black_down.svg"
detailsBtnL.width = "30"
detailsBtnL.height = "30"
songOneBar.appendChild(saveL)
songOneBar.appendChild(plusIconL)
songOneBar.appendChild(spotIconL)
songOneBar.appendChild(detailsBtnL)
// Left song details
var songOneDesc = document.createElement("div")
songOneDesc.className = "song-description"
var songOneNameTag = document.createElement("h1")
var songOneArtistTag = document.createElement("h3")
songOneDesc.appendChild(songOneNameTag)
songOneDesc.appendChild(songOneArtistTag)

// Append elements of the left song to the container
songOneContainer.appendChild(imageSongOne)
songOneContainer.appendChild(optionOneBtn)
songOneContainer.appendChild(songOneBar)
songOneContainer.appendChild(songOneDesc)
songPairContainer.appendChild(songOneContainer)

var orDiv = document.createElement("div")
orDiv.className = "divider-or"
var orheader = document.createElement("h1")
var orText = document.createTextNode("or")
orheader.appendChild(orText)
orDiv.appendChild(orheader)
songPairContainer.appendChild(orDiv)

///////////////
// SONG TWO: //
///////////////
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
// Create the right song menu bar
var songTwoBar = document.createElement("div")
songTwoBar.className = "song-bar"
var saveR = document.createElement("img")
saveR.src = "/static/app/assets/images/svg/heart_black_outline.svg"
saveR.width = "30"
saveR.height = "30"
var saveRClicked = false
var plusIconR = document.createElement("img")
plusIconR.src = "/static/app/assets/images/svg/plus_black.svg"
plusIconR.width = "30"
plusIconR.height = "30"
var spotIconR = document.createElement("img")
spotIconR.src = "/static/app/assets/images/svg/spotify_green.svg"
spotIconR.width = "30"
spotIconR.height = "30"
var detailsBtnR = document.createElement("img")
detailsBtnR.src = "/static/app/assets/images/svg/chevron_black_down.svg"
detailsBtnR.width = "30"
detailsBtnR.height = "30"
songTwoBar.appendChild(saveR)
songTwoBar.appendChild(plusIconR)
songTwoBar.appendChild(spotIconR)
songTwoBar.appendChild(detailsBtnR)
// Right song details
var songTwoDesc = document.createElement("div")
songTwoDesc.className = "song-description"
var songTwoNameTag = document.createElement("h1")
var songTwoArtistTag = document.createElement("h3")
songTwoDesc.appendChild(songTwoNameTag)
songTwoDesc.appendChild(songTwoArtistTag)

// Append elements of the right song to the container
songTwoContainer.appendChild(imageSongTwo)
songTwoContainer.appendChild(optionTwoBtn)
songTwoContainer.appendChild(songTwoBar)
songTwoContainer.appendChild(songTwoDesc)
songPairContainer.appendChild(songTwoContainer)

// Hide elements until songs load
songOneDesc.style.display = "none"
songTwoDesc.style.display = "none"
songPairContainer.style.display = "none"

// Display given song pair to window
async function display(pairData){
	// Reset details button
	detailsBtnL.src = "/static/app/assets/images/svg/chevron_black_down.svg"
	detailsBtnR.src = "/static/app/assets/images/svg/chevron_black_down.svg"
	// Hide song details
	songOneDesc.style.display = "none"
	songTwoDesc.style.display = "none"
	// Check if a song is in the user's library and update the save icon accordingly
	if(songPair[0]["in_library"] == true){
		saveL.src = "/static/app/assets/images/svg/heart_red.svg"
		saveLClicked = true
	}else{
		saveL.src = "/static/app/assets/images/svg/heart_black_outline.svg"
		saveLClicked = false
	}
	if(songPair[1]["in_library"] == true){
		saveR.src = "/static/app/assets/images/svg/heart_red.svg"
		saveRClicked = true
	}else{
		saveR.src = "/static/app/assets/images/svg/heart_black_outline.svg"
		saveRClicked = false
	}

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
		loadingContainer.style.display = "none"

		// Display the a pair of songs
		display(songPair)

		// Display the songs
		songPairContainer.style.display = "flex"

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

		// Save left song when icon is clicked
		saveL.addEventListener("click", () => {
			if(saveLClicked === false){
				saveL.src = "/static/app/assets/images/svg/heart_red.svg"
				saveLClicked = true
			}
			else{
				saveL.src = "/static/app/assets/images/svg/heart_black_outline.svg"
				saveLClicked = false
			}
		});
		// Save right song when icon is clicked
		saveR.addEventListener("click", () => {
			if(saveRClicked === false){
				saveR.src = "/static/app/assets/images/svg/heart_red.svg"
				saveRClicked = true
			}
			else{
				saveR.src = "/static/app/assets/images/svg/heart_black_outline.svg"
				saveRClicked = false
			}
		});

		// Open left song in spotify
		spotIconL.addEventListener("click", () => {
			window.open(songPair[0]["uri"])
		});
		// Open right song in spotify
		spotIconR.addEventListener("click", () => {
			window.open(songPair[1]["uri"])
		})

		// Reveal details of left song
		detailsBtnL.addEventListener("click", () => {
			if(songOneDesc.style.display === "none"){
				detailsBtnL.src = "/static/app/assets/images/svg/chevron_black_up.svg"
				songOneDesc.style.display = "flex"
			}
			else{
				songOneDesc.style.display = "none"
				detailsBtnL.src = "/static/app/assets/images/svg/chevron_black_down.svg"
			}
			
		});
		// Reveal details of right song
		detailsBtnR.addEventListener("click", () => {
			if(songTwoDesc.style.display === "none"){
				detailsBtnR.src = "/static/app/assets/images/svg/chevron_black_up.svg"
				songTwoDesc.style.display = "flex"
			}
			else{
				songTwoDesc.style.display = "none"
				detailsBtnR.src = "/static/app/assets/images/svg/chevron_black_down.svg"
			}
		})
	})
	.catch(err => console.log("Rejected", err))