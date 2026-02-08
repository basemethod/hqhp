// JavaScript to generate and animate text sequence with looping
const textLoader = document.getElementById('myTextLoader'); // Target your loader element
const text = "Loading..."; // The text to animate
const charDelay = 0.1; // Delay between each character animation (seconds)
const animationDuration = 0.5; // Duration of each character's animation (seconds)
const loopInterval = 1; // Interval AFTER animation finishes before looping (seconds)
let loopTimeoutId = null;

function runTextSequenceAnimation() {
    if (!textLoader) return;
    textLoader.innerHTML = ''; // Clear previous content

    text.split('').forEach((char, index) => {
        const span = document.createElement('span');
        span.textContent = char === ' ' ? '\u00A0' : char; // Handle spaces
        span.style.animationName = 'text-appear-animation'; // Ensure CSS defines this keyframe
        span.style.animationDuration = `${animationDuration}s`;
        span.style.animationDelay = `${index * charDelay}s`;
        span.style.animationFillMode = 'forwards'; // Keep final state
        textLoader.appendChild(span);
    });

    // Clear previous loop timeout if any
    if (loopTimeoutId) {
        clearTimeout(loopTimeoutId);
    }

    // Calculate total time for one full sequence to complete
    const totalSequenceTime = (text.length * charDelay) + animationDuration;

    // Set timeout for the next loop
    loopTimeoutId = setTimeout(() => {
        runTextSequenceAnimation(); // Re-run the animation
    }, (totalSequenceTime + loopInterval) * 1000);
}

if (textLoader) {
    // Initial call
    runTextSequenceAnimation();
}

// CSS needed:
// .text-sequence-loader-preview span { /* Initial styles like opacity: 0, transform, display: inline-block */ }
// @keyframes text-appear-animation { /* Animation from initial to final state */ }
