// static/script.js
const video = document.getElementById('webcam');
const startButton = document.getElementById('startButton');
const statusElement = document.getElementById('status');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

let detectionInterval;

// Función para solicitar acceso a la cámara web
async function setupWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 },
            audio: false 
        });
        video.srcObject = stream;
        return new Promise((resolve) => {
            video.onloadedmetadata = () => {
                resolve(video);
            };
        });
    } catch (err) {
        console.error("Error al acceder a la cámara: ", err);
        statusElement.textContent = "Error: No se pudo acceder a la cámara.";
    }
}

// Función para enviar un frame al backend y obtener la predicción
async function sendFrameForPrediction() {
    // Ajustar el tamaño del canvas al del video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Dibujar el frame actual del video en el canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Obtener la imagen del canvas en formato Base64
    const imageDataURL = canvas.toDataURL('image/jpeg');

    try {
        // Enviar la imagen al servidor
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageDataURL }),
        });
        
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const data = await response.json();

        // Mostrar el resultado en la pantalla
        statusElement.textContent = data.postura;

    } catch (error) {
        console.error('Error al enviar el frame:', error);
        statusElement.textContent = "Error de conexión con el servidor.";
        // Detener el intervalo si hay un error para no sobrecargar la red
        clearInterval(detectionInterval);
    }
}

// Evento del botón para iniciar la detección
startButton.addEventListener('click', async () => {
    statusElement.textContent = "Iniciando cámara...";
    await setupWebcam();
    video.play();
    
    // Si ya hay un intervalo, lo limpiamos para evitar duplicados
    if (detectionInterval) {
        clearInterval(detectionInterval);
    }

    // Iniciar el envío de frames cada 200 milisegundos (5 veces por segundo)
    detectionInterval = setInterval(sendFrameForPrediction, 200); 
    
    statusElement.textContent = "Detección activa...";
});