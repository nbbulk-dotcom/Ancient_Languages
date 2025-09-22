/**
 * Proto-Elamite Decipherment Website Application
 * Revolutionary Angular Frequency Analysis by Nicolas of the Family Brett
 * Third Historic Breakthrough in Ancient Script Decipherment
 */

// Audio Context for frequency generation
let audioContext;
let currentOscillator = null;

// Proto-Elamite sign data with angular frequency analysis
const protoElamiteSigns = {
    'M1': {
        angles: [180],
        frequency: 880.0,
        note: 'A5',
        category: 'Ultimate Authority',
        meaning: 'Highest administrative level',
        pattern: 'Straight Line (Expansive)'
    },
    'M36': {
        angles: [90],
        frequency: 440.0,
        note: 'A4',
        category: 'Administrative Standard',
        meaning: 'Standard administrative functions',
        pattern: 'Right Angle (Standard)'
    },
    'M387': {
        angles: [150, 30],
        frequency: 382.8,
        note: 'G3',
        category: 'Common Commodities',
        meaning: 'General trade goods',
        pattern: 'Obtuse + Acute (Mixed)'
    },
    'M371': {
        angles: [135, 45],
        frequency: 369.0,
        note: 'F#3',
        category: 'Common Commodities',
        meaning: 'Standard commodities',
        pattern: 'Wide Obtuse + Diagonal'
    },
    'M388': {
        angles: [120, 60],
        frequency: 328.0,
        note: 'E3',
        category: 'Common Commodities',
        meaning: 'Basic trade items',
        pattern: 'Obtuse + Acute (Balanced)'
    }
};

// Angular frequency mapping system
const angularFrequencies = {
    30: 220.0,   // A3 - Sharp acute
    45: 330.0,   // E4 - Diagonal
    60: 293.33,  // D4 - Acute
    90: 440.0,   // A4 - Right angle (universal standard)
    120: 586.67, // D5 - Obtuse
    135: 660.0,  // E5 - Wide obtuse
    150: 733.33, // F#5 - Very obtuse
    180: 880.0   // A5 - Straight line (double octave)
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeAudioContext();
    initializeAngularDemo();
    initializeFrequencyChart();
    initializeInteractiveTools();
    initializeAnimations();
    initializeFrequencyVisualization();
});

// Initialize Web Audio API
function initializeAudioContext() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    } catch (error) {
        console.log('Web Audio API not supported');
    }
}

// Initialize angular demonstration
function initializeAngularDemo() {
    const angleSlider = document.getElementById('angleSlider');
    const angleValue = document.getElementById('angleValue');
    const frequencyValue = document.getElementById('frequencyValue');
    const noteValue = document.getElementById('noteValue');
    
    if (angleSlider && angleValue && frequencyValue && noteValue) {
        angleSlider.addEventListener('input', function() {
            const angle = parseInt(this.value);
            angleValue.textContent = angle;
            
            const frequency = calculateAngleFrequency(angle);
            frequencyValue.textContent = frequency.toFixed(1);
            noteValue.textContent = frequencyToNote(frequency);
            
            drawAngleVisualization(angle);
        });
        
        // Initialize with default value
        const initialAngle = parseInt(angleSlider.value);
        angleValue.textContent = initialAngle;
        frequencyValue.textContent = calculateAngleFrequency(initialAngle).toFixed(1);
        noteValue.textContent = frequencyToNote(calculateAngleFrequency(initialAngle));
        drawAngleVisualization(initialAngle);
    }
}

// Calculate frequency for a given angle
function calculateAngleFrequency(angle) {
    if (angularFrequencies[angle]) {
        return angularFrequencies[angle];
    }
    
    // Linear interpolation for angles not in base set
    const angles = Object.keys(angularFrequencies).map(Number).sort((a, b) => a - b);
    const frequencies = angles.map(a => angularFrequencies[a]);
    
    return linearInterpolate(angle, angles, frequencies);
}

// Linear interpolation function
function linearInterpolate(x, xArray, yArray) {
    if (x <= xArray[0]) return yArray[0];
    if (x >= xArray[xArray.length - 1]) return yArray[yArray.length - 1];
    
    for (let i = 0; i < xArray.length - 1; i++) {
        if (x >= xArray[i] && x <= xArray[i + 1]) {
            const t = (x - xArray[i]) / (xArray[i + 1] - xArray[i]);
            return yArray[i] + t * (yArray[i + 1] - yArray[i]);
        }
    }
    return yArray[0];
}

// Convert frequency to musical note
function frequencyToNote(frequency) {
    const A4 = 440.0;
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    
    const semitones = 12 * Math.log2(frequency / A4);
    const octave = 4 + Math.floor(semitones / 12);
    const noteIndex = Math.round(semitones % 12);
    
    return `${notes[noteIndex < 0 ? noteIndex + 12 : noteIndex]}${octave}`;
}

// Draw angle visualization
function drawAngleVisualization(angle) {
    const canvas = document.getElementById('angleCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw angle
    const angleRad = (angle * Math.PI) / 180;
    
    // Draw first line (horizontal reference)
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + radius, centerY);
    ctx.strokeStyle = '#2c5aa0';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Draw second line (angle line)
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + radius * Math.cos(-angleRad), centerY + radius * Math.sin(-angleRad));
    ctx.strokeStyle = '#e76f51';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Draw arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.3, 0, -angleRad, true);
    ctx.strokeStyle = '#f4a261';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw angle text
    ctx.font = '16px Inter';
    ctx.fillStyle = '#2c5aa0';
    ctx.textAlign = 'center';
    ctx.fillText(`${angle}°`, centerX, centerY - 10);
}

// Initialize frequency chart
function initializeFrequencyChart() {
    const canvas = document.getElementById('frequencyChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const signs = Object.keys(protoElamiteSigns);
    const frequencies = signs.map(sign => protoElamiteSigns[sign].frequency);
    
    // Chart dimensions
    const padding = 60;
    const chartWidth = canvas.width - 2 * padding;
    const chartHeight = canvas.height - 2 * padding;
    const barWidth = chartWidth / signs.length * 0.8;
    const maxFreq = Math.max(...frequencies);
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw bars
    signs.forEach((sign, index) => {
        const freq = protoElamiteSigns[sign].frequency;
        const barHeight = (freq / maxFreq) * chartHeight;
        const x = padding + index * (chartWidth / signs.length) + (chartWidth / signs.length - barWidth) / 2;
        const y = canvas.height - padding - barHeight;
        
        // Determine color based on frequency category
        let color;
        if (freq >= 600) color = '#e76f51'; // High authority
        else if (freq >= 400) color = '#f4a261'; // Standard admin
        else color = '#2a9d8f'; // Common commodities
        
        // Draw bar
        ctx.fillStyle = color;
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // Draw sign label
        ctx.font = '12px Inter';
        ctx.fillStyle = '#264653';
        ctx.textAlign = 'center';
        ctx.fillText(sign, x + barWidth / 2, canvas.height - padding + 20);
        
        // Draw frequency label
        ctx.font = '10px Inter';
        ctx.fillText(`${freq.toFixed(0)} Hz`, x + barWidth / 2, y - 5);
    });
    
    // Draw axes
    ctx.strokeStyle = '#264653';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // Y-axis labels
    ctx.font = '12px Inter';
    ctx.fillStyle = '#264653';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 5; i++) {
        const freq = (maxFreq / 5) * i;
        const y = canvas.height - padding - (freq / maxFreq) * chartHeight;
        ctx.fillText(`${freq.toFixed(0)} Hz`, padding - 10, y + 4);
    }
    
    // Title
    ctx.font = 'bold 16px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('Proto-Elamite Sign Frequency Distribution', canvas.width / 2, 30);
}

// Initialize frequency visualization in hero section
function initializeFrequencyVisualization() {
    const canvas = document.getElementById('frequencyCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Animate frequency waves
    function drawFrequencyWaves() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const time = Date.now() * 0.001;
        const centerY = canvas.height / 2;
        
        // Draw multiple frequency waves
        const frequencies = [880, 440, 293];
        const colors = ['#e76f51', '#f4a261', '#2a9d8f'];
        
        frequencies.forEach((freq, index) => {
            ctx.beginPath();
            ctx.strokeStyle = colors[index];
            ctx.lineWidth = 2;
            
            for (let x = 0; x < canvas.width; x++) {
                const normalizedFreq = freq / 1000; // Normalize for visualization
                const y = centerY + Math.sin((x * 0.02) + (time * normalizedFreq * 2)) * (20 - index * 5);
                
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
        });
        
        // Draw frequency labels
        ctx.font = '12px Inter';
        ctx.textAlign = 'left';
        frequencies.forEach((freq, index) => {
            ctx.fillStyle = colors[index];
            ctx.fillText(`${freq} Hz`, 10, 20 + index * 20);
        });
    }
    
    // Start animation
    setInterval(drawFrequencyWaves, 50);
}

// Initialize interactive tools
function initializeInteractiveTools() {
    // Sign selector change handler
    const signSelector = document.getElementById('signSelector');
    if (signSelector) {
        signSelector.addEventListener('change', function() {
            updateAudioVisualization();
        });
    }
}

// Play selected Proto-Elamite sign
function playSelectedSign() {
    const signSelector = document.getElementById('signSelector');
    if (!signSelector || !audioContext) return;
    
    const signId = signSelector.value;
    const sign = protoElamiteSigns[signId];
    
    if (sign) {
        playFrequency(sign.frequency, 1000); // Play for 1 second
        updateAudioVisualization();
    }
}

// Play frequency sequence
function playSequence() {
    if (!audioContext) return;
    
    const signs = Object.keys(protoElamiteSigns);
    let delay = 0;
    
    signs.forEach(signId => {
        setTimeout(() => {
            const sign = protoElamiteSigns[signId];
            playFrequency(sign.frequency, 800);
        }, delay);
        delay += 1000;
    });
}

// Play Proto-Elamite demo
function playProtoElamiteDemo() {
    if (!audioContext) {
        initializeAudioContext();
    }
    
    // Play a sequence of the most significant frequencies
    const demoSequence = [880, 440, 383, 369, 328]; // M1, M36, M387, M371, M388
    let delay = 0;
    
    demoSequence.forEach(freq => {
        setTimeout(() => {
            playFrequency(freq, 800);
        }, delay);
        delay += 1000;
    });
}

// Play angle tone
function playAngleTone() {
    const angleSlider = document.getElementById('angleSlider');
    if (!angleSlider || !audioContext) return;
    
    const angle = parseInt(angleSlider.value);
    const frequency = calculateAngleFrequency(angle);
    playFrequency(frequency, 1000);
}

// Play frequency using Web Audio API
function playFrequency(frequency, duration) {
    if (!audioContext) return;
    
    // Stop current oscillator if playing
    if (currentOscillator) {
        currentOscillator.stop();
        currentOscillator = null;
    }
    
    // Create oscillator
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
    oscillator.type = 'sine';
    
    // Envelope
    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.3, audioContext.currentTime + 0.1);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration / 1000);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration / 1000);
    
    currentOscillator = oscillator;
}

// Update audio visualization
function updateAudioVisualization() {
    const canvas = document.getElementById('audioVisualization');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const signSelector = document.getElementById('signSelector');
    
    if (!signSelector) return;
    
    const signId = signSelector.value;
    const sign = protoElamiteSigns[signId];
    
    if (!sign) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw waveform representation
    const centerY = canvas.height / 2;
    const frequency = sign.frequency;
    const normalizedFreq = frequency / 1000;
    
    ctx.beginPath();
    ctx.strokeStyle = '#2c5aa0';
    ctx.lineWidth = 2;
    
    for (let x = 0; x < canvas.width; x++) {
        const y = centerY + Math.sin(x * 0.05 * normalizedFreq) * 30;
        
        if (x === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.stroke();
    
    // Draw frequency info
    ctx.font = '14px Inter';
    ctx.fillStyle = '#2c5aa0';
    ctx.textAlign = 'center';
    ctx.fillText(`${signId}: ${frequency.toFixed(1)} Hz (${sign.note})`, canvas.width / 2, 20);
}

// Calculate custom frequency
function calculateCustomFrequency() {
    const angle1 = parseFloat(document.getElementById('angle1').value) || 0;
    const angle2 = parseFloat(document.getElementById('angle2').value) || 0;
    const angle3 = parseFloat(document.getElementById('angle3').value) || 0;
    
    const angles = [angle1, angle2, angle3].filter(a => a > 0);
    
    if (angles.length === 0) {
        document.getElementById('customFrequency').textContent = '-- Hz';
        document.getElementById('customNote').textContent = '--';
        document.getElementById('customCategory').textContent = '--';
        return;
    }
    
    // Calculate individual frequencies
    const frequencies = angles.map(angle => calculateAngleFrequency(angle));
    
    // Calculate accumulated frequency
    let accumulatedFreq;
    if (frequencies.length === 1) {
        accumulatedFreq = frequencies[0];
    } else {
        accumulatedFreq = Math.sqrt(frequencies.reduce((sum, f) => sum + f * f, 0)) / frequencies.length;
    }
    
    // Determine category
    let category;
    if (accumulatedFreq >= 600) category = 'High Authority';
    else if (accumulatedFreq >= 400) category = 'Standard Admin';
    else if (accumulatedFreq >= 300) category = 'Common Items';
    else category = 'Basic Elements';
    
    // Update display
    document.getElementById('customFrequency').textContent = accumulatedFreq.toFixed(1);
    document.getElementById('customNote').textContent = frequencyToNote(accumulatedFreq);
    document.getElementById('customCategory').textContent = category;
}

// Analyze pattern
function analyzePattern() {
    const patternInput = document.getElementById('patternInput');
    const patternDetails = document.getElementById('patternDetails');
    
    if (!patternInput || !patternDetails) return;
    
    const input = patternInput.value.trim();
    if (!input) {
        patternDetails.innerHTML = 'Enter angles to analyze pattern';
        return;
    }
    
    try {
        const angles = input.split(',').map(s => parseFloat(s.trim())).filter(a => !isNaN(a) && a > 0);
        
        if (angles.length === 0) {
            patternDetails.innerHTML = 'Please enter valid angles separated by commas';
            return;
        }
        
        // Calculate pattern analysis
        const frequencies = angles.map(angle => calculateAngleFrequency(angle));
        const accumulatedFreq = frequencies.length === 1 ? 
            frequencies[0] : 
            Math.sqrt(frequencies.reduce((sum, f) => sum + f * f, 0)) / frequencies.length;
        
        const acuteCount = angles.filter(a => a < 90).length;
        const rightCount = angles.filter(a => a === 90).length;
        const obtuseCount = angles.filter(a => a > 90).length;
        
        let geometricPattern;
        if (obtuseCount > acuteCount) geometricPattern = 'Obtuse Dominant (High Status)';
        else if (acuteCount > obtuseCount) geometricPattern = 'Acute Dominant (Functional)';
        else geometricPattern = 'Balanced Angular (Administrative)';
        
        let category;
        if (accumulatedFreq >= 600) category = 'High Authority/Luxury Items';
        else if (accumulatedFreq >= 400) category = 'Standard Administrative';
        else if (accumulatedFreq >= 300) category = 'Common Commodities';
        else category = 'Basic Elements';
        
        // Display results
        patternDetails.innerHTML = `
            <div class="pattern-result">
                <h4>Pattern Analysis Results</h4>
                <p><strong>Angles:</strong> ${angles.join('°, ')}°</p>
                <p><strong>Individual Frequencies:</strong> ${frequencies.map(f => f.toFixed(1)).join(', ')} Hz</p>
                <p><strong>Accumulated Frequency:</strong> ${accumulatedFreq.toFixed(1)} Hz</p>
                <p><strong>Musical Note:</strong> ${frequencyToNote(accumulatedFreq)}</p>
                <p><strong>Geometric Pattern:</strong> ${geometricPattern}</p>
                <p><strong>Administrative Category:</strong> ${category}</p>
                <p><strong>Angular Complexity:</strong> ${angles.length} angles</p>
            </div>
        `;
        
        // Draw pattern visualization
        drawPatternVisualization(angles);
        
    } catch (error) {
        patternDetails.innerHTML = 'Error analyzing pattern. Please check your input.';
    }
}

// Draw pattern visualization
function drawPatternVisualization(angles) {
    const canvas = document.getElementById('patternCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Draw angles
    const colors = ['#2c5aa0', '#e76f51', '#f4a261', '#2a9d8f', '#264653'];
    
    angles.forEach((angle, index) => {
        const angleRad = (angle * Math.PI) / 180;
        const color = colors[index % colors.length];
        
        // Draw line
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + radius * Math.cos(-angleRad), centerY + radius * Math.sin(-angleRad));
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // Draw angle arc
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * (0.2 + index * 0.1), 0, -angleRad, true);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.stroke();
    });
    
    // Draw reference line
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + radius, centerY);
    ctx.strokeStyle = '#999';
    ctx.lineWidth = 2;
    ctx.stroke();
}

// Download thesis in different formats
function downloadThesis(format) {
    // This would typically connect to a server endpoint
    // For demo purposes, we'll show an alert
    alert(`Downloading Proto-Elamite Decipherment Thesis in ${format.toUpperCase()} format...`);
    
    // In a real implementation, this would trigger a download
    // window.open(`/api/download-thesis?format=${format}`, '_blank');
}

// Scroll to section
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialize animations
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.method-card, .result-card, .implication-card, .tool-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        observer.observe(el);
    });
}

// Utility function to format numbers
function formatNumber(num) {
    return num.toLocaleString();
}

// Export functions for global access
window.playProtoElamiteDemo = playProtoElamiteDemo;
window.playSelectedSign = playSelectedSign;
window.playSequence = playSequence;
window.playAngleTone = playAngleTone;
window.calculateCustomFrequency = calculateCustomFrequency;
window.analyzePattern = analyzePattern;
window.downloadThesis = downloadThesis;
window.scrollToSection = scrollToSection;

console.log('🏛️ Proto-Elamite Decipherment Website Loaded');
console.log('🎯 Revolutionary Angular Frequency Analysis by Nicolas of the Family Brett');
console.log('📐 Third Historic Breakthrough in Ancient Script Decipherment');
