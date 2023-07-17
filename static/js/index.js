const video = document.getElementById('video');
const canvas = document.getElementById('overlay');




var socket = io.connect('http://127.0.0.1:5000');
socket.on( 'connect', function() {
  console.log("SOCKET CONNECTED")
})

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
Promise.all([
  faceapi.loadFaceLandmarkModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadFaceRecognitionModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadTinyFaceDetectorModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadFaceLandmarkModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadFaceLandmarkTinyModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadFaceRecognitionModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadFaceExpressionModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadMtcnnModel("http://127.0.0.1:5000/static/models/"),
  faceapi.loadSsdMobilenetv1Model("http://127.0.0.1:5000/static/models/"),
])
  .then(startScreenCapture)
  .catch(err => console.error(err));
  
  function startScreenCapture() {
        navigator.mediaDevices.getDisplayMedia({ video: true })
          .then(stream => {
            video.srcObject = stream;
          })
          .catch(err => {
            console.error('Error al capturar la pantalla:', err);
          });
      }

//function startVideo() {
//  console.log("access");
//  navigator.getUserMedia(
//    {
//      video: {}
//    },
//    stream => video.srcObject = stream,
//    err => console.error(err)
//  )
// }

video.addEventListener('play', () => {
  // console.log('thiru');

  //const canvas = faceapi.createCanvasFromMedia(video);
  //document.body.append(canvas);
  
  
  
  const dims = faceapi.matchDimensions(canvas, video, true);

  
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceExpressions();
    console.log(detections)
    socket.emit( 'my event', {
      data: detections
    })
    
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
    //faceapi.draw.drawFaceExpressions(canvas, resizedDetections, 0.05);
    const expressions = resizedDetections[0].expressions;
const expressionsArray = Object.entries(expressions);
const sortedExpressions = expressionsArray.sort((a, b) => b[1] - a[1]);

canvas.getContext('2d').font = '${fontWeight} 10px Arial';
//canvas.getContext('2d').fillStyle = '#FF0000';

let yOffset = 0;

sortedExpressions.forEach((expression) => {
  const [emotion, score] = expression;

  let emotionText = '';

  switch (emotion) {
    case 'neutral':
      emotionText = 'Neutral';
      break;
    case 'happy':
      emotionText = 'Feliz';
      break;
    case 'sad':
      emotionText = 'Triste';
      break;
    case 'angry':
      emotionText = 'Enojado';
      break;
    case 'fearful':
      emotionText = 'Asustado';
      break;
    case 'disgusted':
      emotionText = 'Disgustado';
      break;
    case 'surprised':
      emotionText = 'Sorprendido';
      break;
    default:
      emotionText = emotion;
  }
  
  let color = '#FF0000'; // Color predeterminado
  let fontWeight = 'bold';
  

      if (emotion === sortedExpressions[0][0] || emotion === sortedExpressions[1][0]) {
        color = '#00FF00'; // Cambia el color para la emoción con el mayor puntaje
         canvas.getContext('2d').shadowColor = '#FFFF00'; // Establece el color del sombreado
        canvas.getContext('2d').shadowBlur = 10;
      }else {
        canvas.getContext('2d').shadowColor = 'transparent'; // Restablece el sombreado para las otras emociones
      }


      canvas.getContext('2d').fillStyle = color;

  canvas.getContext('2d').fillText(`${emotionText}: ${Math.round(score * 100)}%`, 10, 30 + yOffset);
  yOffset += 20; // Ajusta este valor según la separación vertical deseada
});




    console.log(detections);
  }, 50)
})