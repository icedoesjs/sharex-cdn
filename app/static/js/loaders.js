// Video Handler & Loader
const video = document.createElement('video');
video.src = '/storage/389558396195438593/s0I_G1mnsDax.mp4';
video.controls = true;
video.height = 240;
video.width = 320;
video.autoplay = true;
const holder = document.getElementById('holder');
holder.appendChild(video);