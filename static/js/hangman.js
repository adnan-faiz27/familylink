
const container = document.getElementById("alphabetButtons");
var answerDisplay = document.getElementById("hold");
var answer = "";
var hint = "";
var life = 10;
var score = 0;
var wordDisplay = [];
var winningCheck = "";
const containerHint = document.getElementById("clue");
const buttonHint = document.getElementById("hint");
const buttonReset = document.getElementById("reset");
const livesDisplay = document.getElementById("mylives");
var myStickman = document.getElementById("stickman");
var context = myStickman.getContext("2d");

//generate alphabet button
function generateButton() {
    var buttonsHTML = "abcdefghijklmnopqrstuvwxyz"
        .split("")
        .map(
            (letter) =>
                `<button
         class = "alphabetButtonJS" 
         id="${letter}"
         >
        ${letter}
        </button>`
        )
        .join("");

    return buttonsHTML;
}

function handleClick(event) {
    const isButton = event.target.nodeName === "BUTTON";
    if (isButton) {
        //console.dir(event.target.id);
        //console.log(isButton);
        const buttonId = document.getElementById(event.target.id);
        buttonId.classList.add("selected");
    }
    return;
}

const wordList = [
    {
        word: "guitar",
        hint: "A musical instrument with strings."
    },
    {
        word: "oxygen",
        hint: "A colorless, odorless gas essential for life."
    },
    {
        word: "mountain",
        hint: "A large natural elevation of the Earth's surface."
    },
    {
        word: "painting",
        hint: "An art form using colors on a surface to create images or expression."
    },
    {
        word: "astronomy",
        hint: "The scientific study of celestial objects and phenomena."
    },
    {
        word: "football",
        hint: "A popular sport played with a spherical ball."
    },
    {
        word: "chocolate",
        hint: "A sweet treat made from cocoa beans."
    },
    {
        word: "butterfly",
        hint: "An insect with colorful wings and a slender body."
    },
    {
        word: "history",
        hint: "The study of past events and human civilization."
    },
    {
        word: "pizza",
        hint: "A savory dish consisting of a round, flattened base with toppings."
    },
    {
        word: "jazz",
        hint: "A genre of music characterized by improvisation and syncopation."
    },
    {
        word: "camera",
        hint: "A device used to capture and record images or videos."
    },
    {
        word: "diamond",
        hint: "A precious gemstone known for its brilliance and hardness."
    },
    {
        word: "adventure",
        hint: "An exciting or daring experience."
    },
    {
        word: "science",
        hint: "The systematic study of the structure and behavior of the physical and natural world."
    },
    {
        word: "bicycle",
        hint: "A human-powered vehicle with two wheels."
    },
    {
        word: "sunset",
        hint: "The daily disappearance of the sun below the horizon."
    },
    {
        word: "coffee",
        hint: "A popular caffeinated beverage made from roasted coffee beans."
    },
    {
        word: "dance",
        hint: "A rhythmic movement of the body often performed to music."
    },
    {
        word: "galaxy",
        hint: "A vast system of stars, gas, and dust held together by gravity."
    },
    {
        word: "orchestra",
        hint: "A large ensemble of musicians playing various instruments."
    },
    {
        word: "volcano",
        hint: "A mountain or hill with a vent through which lava, rock fragments, hot vapor, and gas are ejected."
    },
    {
        word: "novel",
        hint: "A long work of fiction, typically with a complex plot and characters."
    },
    {
        word: "sculpture",
        hint: "A three-dimensional art form created by shaping or combining materials."
    },
    {
        word: "symphony",
        hint: "A long musical composition for a full orchestra, typically in multiple movements."
    },
    {
        word: "architecture",
        hint: "The art and science of designing and constructing buildings."
    },
    {
        word: "ballet",
        hint: "A classical dance form characterized by precise and graceful movements."
    },
    {
        word: "waterfall",
        hint: "A cascade of water falling from a height."
    },
    {
        word: "technology",
        hint: "The application of scientific knowledge for practical purposes."
    },
    {
        word: "rainbow",
        hint: "A meteorological phenomenon that is caused by reflection, refraction, and dispersion of light."
    },
    {
        word: "universe",
        hint: "All existing matter, space, and time as a whole."
    },
    {
        word: "piano",
        hint: "A musical instrument played by pressing keys that cause hammers to strike strings."
    },
    {
        word: "vacation",
        hint: "A period of time devoted to pleasure, rest, or relaxation."
    },
    {
        word: "rainforest",
        hint: "A dense forest characterized by high rainfall and biodiversity."
    },
    {
        word: "theater",
        hint: "A building or outdoor area in which plays, movies, or other performances are staged."
    },
    {
        word: "telephone",
        hint: "A device used to transmit sound over long distances."
    },
    {
        word: "language",
        hint: "A system of communication consisting of words, gestures, and syntax."
    },
    {
        word: "desert",
        hint: "A barren or arid land with little or no precipitation."
    },
    {
        word: "sunflower",
        hint: "A tall plant with a large yellow flower head."
    },
    {
        word: "fantasy",
        hint: "A genre of imaginative fiction involving magic and supernatural elements."
    },
    {
        word: "telescope",
        hint: "An optical instrument used to view distant objects in space."
    },
    {
        word: "breeze",
        hint: "A gentle wind."
    },
    {
        word: "oasis",
        hint: "A fertile spot in a desert where water is found."
    },
    {
        word: "photography",
        hint: "The art, process, or practice of creating images by recording light or other electromagnetic radiation."
    },
    {
        word: "safari",
        hint: "An expedition or journey, typically to observe wildlife in their natural habitat."
    },
    {
        word: "planet",
        hint: "A celestial body that orbits a star and does not produce light of its own."
    },
    {
        word: "river",
        hint: "A large natural stream of water flowing in a channel to the sea, a lake, or another such stream."
    },
    {
        word: "tropical",
        hint: "Relating to or situated in the region between the Tropic of Cancer and the Tropic of Capricorn."
    },
    {
        word: "mysterious",
        hint: "Difficult or impossible to understand, explain, or identify."
    },
    {
        word: "enigma",
        hint: "Something that is mysterious, puzzling, or difficult to understand."
    },
    {
        word: "paradox",
        hint: "A statement or situation that contradicts itself or defies intuition."
    },
    {
        word: "puzzle",
        hint: "A game, toy, or problem designed to test ingenuity or knowledge."
    },
    {
        word: "whisper",
        hint: "To speak very softly or quietly, often in a secretive manner."
    },
    {
        word: "shadow",
        hint: "A dark area or shape produced by an object blocking the light."
    },
    {
        word: "secret",
        hint: "Something kept hidden or unknown to others."
    },
    {
        word: "curiosity",
        hint: "A strong desire to know or learn something."
    },
    {
        word: "unpredictable",
        hint: "Not able to be foreseen or known beforehand; uncertain."
    },
    {
        word: "unveil",
        hint: "To make known or reveal something previously secret or unknown."
    },
    {
        word: "illusion",
        hint: "A false perception or belief; a deceptive appearance or impression."
    },
    {
        word: "moonlight",
        hint: "The light from the moon."
    },
    {
        word: "vibrant",
        hint: "Full of energy, brightness, and life."
    },
    {
        word: "nostalgia",
        hint: "A sentimental longing or wistful affection for the past."
    },
    {
        word: "brilliant",
        hint: "Exceptionally clever, talented, or impressive."
    },
    {
        word: "incorrectly",
        hint: "What word is spelled incorrectly in every single dictionary?"
    },
    {
        word: "incorrectly",
        hint: "What word is spelled incorrectly in every single dictionary?"
    },
    {
        word: "clock",
        hint: "What has a face and two hands, but no arms or legs?"
    },
    {
        word: "clock",
        hint: "What has a face and two hands, but no arms or legs?"
    },
    {
        word: "short",
        hint: "What 5-letter word becomes shorter when you add two letters to it?"
    },
    {
        word: "silence",
        hint: "I m so fragile that if you say my name, you will break me. What am I?"
    },
    {
        word: "mounteverest",
        hint: "Before Mount Everest was discovered, what was the tallest mountain on Earth?"
    },
];

//set question,answer and hint

function setAnswer() {
    const { word, hint } = wordList[Math.floor(Math.random() * wordList.length)];

    const categoryNameJS = document.getElementById("categoryName");
    categoryNameJS.innerHTML = `Question - ${hint}`;

    answer = word;
    containerHint.innerHTML = `Score - ${score}`;
    answerDisplay.innerHTML = generateAnswerDisplay(word);
}

function generateAnswerDisplay(word) {
    var wordArray = word.split("");
    //console.log(wordArray);
    for (var i = 0; i < answer.length; i++) {
        if (wordArray[i] !== "-") {
            wordDisplay.push("_");
        } else {
            wordDisplay.push("-");
        }
    }
    return wordDisplay.join(" ");
}

function newquestion() {
    answer = "";
    wordDisplay = [];
    winningCheck = "";
    setAnswer();
    container.innerHTML = generateButton();
    container.addEventListener("click", handleClick);
}


function init() {
    answer = "";
    life = 10;
    score = 0;
    wordDisplay = [];
    winningCheck = "";
    context.clearRect(0, 0, 400, 400);
    canvas();
    containerHint.innerHTML = `Score -${score}`;
    livesDisplay.innerHTML = `You have ${life} lives!`;
    setAnswer();
    container.innerHTML = generateButton();
    container.addEventListener("click", handleClick);
    //console.log(hint);
}

window.onload = init();

//reset (play again)
buttonReset.addEventListener("click", init);

//guess click
function guess(event) {
    containerHint.innerHTML = `Score - ${score}`;
    const guessWord = event.target.id;
    const answerArray = answer.split("");
    var counter = 0;
    if (answer === winningCheck) {
        score++;
        newquestion();
        return;
    } else {
        if (life > 0) {
            for (var j = 0; j < answer.length; j++) {
                if (guessWord === answerArray[j]) {
                    wordDisplay[j] = guessWord;
                    answerDisplay.innerHTML = wordDisplay.join(" ");
                    winningCheck = wordDisplay.join("");
                    //console.log(winningCheck)
                    counter += 1;
                }
            }
            if (counter === 0) {
                life -= 1;
                counter = 0;
                animate();
            } else {
                counter = 0;
            }
            if (life > 1) {
                livesDisplay.innerHTML = `You have ${life} lives!`;
            } else if (life === 1) {
                livesDisplay.innerHTML = `You have ${life} life!`;
            } else {
                $.ajax({
                    url: '/gamehouse/hangman',
                    type: "GET",
                    data: {count : score},
    
                })
                livesDisplay.innerHTML = `GAME OVER! Your word was ${answer}`;
                categoryNameJS.innerHTML = ``;
                // ajax
            }
        } else {
            return;
        }

        if (answer === winningCheck) {
            score++;
            newquestion();
            return;
        }
    }
}

container.addEventListener("click", guess);

// Hangman
function animate() {
    drawArray[life]();
    //console.log(drawArray[life]);
}

function canvas() {
    myStickman = document.getElementById("stickman");
    context = myStickman.getContext("2d");
    context.beginPath();
    context.strokeStyle = "#fff";
    context.lineWidth = 2;
}

function head() {
    myStickman = document.getElementById("stickman");
    context = myStickman.getContext("2d");
    context.beginPath();
    context.arc(60, 25, 10, 0, Math.PI * 2, true);
    context.stroke();
}

function draw($pathFromx, $pathFromy, $pathTox, $pathToy) {
    context.moveTo($pathFromx, $pathFromy);
    context.lineTo($pathTox, $pathToy);
    context.stroke();
}

function frame1() {
    draw(0, 150, 150, 150);
}

function frame2() {
    draw(10, 0, 10, 600);
}

function frame3() {
    draw(0, 5, 70, 5);
}

function frame4() {
    draw(60, 5, 60, 15);
}

function torso() {
    draw(60, 36, 60, 70);
}

function rightArm() {
    draw(60, 46, 100, 50);
}

function leftArm() {
    draw(60, 46, 20, 50);
}

function rightLeg() {
    draw(60, 70, 100, 100);
}

function leftLeg() {
    draw(60, 70, 20, 100);
}

var drawArray = [
    rightLeg,
    leftLeg,
    rightArm,
    leftArm,
    torso,
    head,
    frame4,
    frame3,
    frame2,
    frame1
];
