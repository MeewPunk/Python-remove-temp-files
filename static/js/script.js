var socket = io();

const form = document.getElementById('form');
const startButton = document.getElementById('start-button');
const result = document.getElementById('result');

setInterval(()=> {
    socket.emit('data', {data: ''});
}, 100)

socket.on('my response', function(data) {
    result.textContent = data;
    console.log(data);
})

form.addEventListener('submit', (event) => {
  event.preventDefault();
  result.innerHTML = '';

  const days = document.getElementById('days').value;
  const path = document.getElementById('path').value;

  startButton.disabled = true;
  startButton.textContent = 'กำลังทำงาน...';
  console.log('days',days)
  console.log('path',path)
  socket.emit('Remove_Temp', {days: days , path: path });

});

$("#reset-button").click(function() {
    location.reload();
});