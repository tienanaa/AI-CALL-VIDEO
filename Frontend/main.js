console.log("Kết nối thành công!");
const lobby = document.getElementById("lobby-container");
const screen = document.querySelector(".screen");

// Biến cho Guest
const roomInput = document.getElementById("room-id");
const joinBtn = document.getElementById("join-btn");

// Biến cho Host
const createRoomBtn = document.getElementById("create-room-btn");
const hostSetup = document.getElementById("host-setup");
const generatedIdText = document.getElementById("generated-id");
const startCallBtn = document.getElementById("start-call-btn");
const roomPass = document.getElementById("require-password");
const roomPassContainer = document.getElementById("room-password-container");
const roomPassInput = document.getElementById("room-password-input");
const roomPassBtn = document.getElementById("room-password-btn");

let localStream;
let peer;

let isCamOn = true;
const camBtn = document.querySelector("#cam-btn");
const camIcon = camBtn.querySelector(".material-symbols-outlined");

let isMicOn = true;
const micBtn = document.querySelector("#mic-btn");
const micIcon = micBtn.querySelector(".material-symbols-outlined");

let isChatOpen = false;
const msgBtn = document.querySelector("#msg-btn");
const chatBox = document.querySelector("#chat-box");

let mediaRecorder;
let recordedChunks = [];
let isRecording = false;
let remoteStream;
const recordBtn = document.querySelector("#record-btn");
const recordIcon = recordBtn.querySelector(".material-symbols-outlined");

async function openCamera() {
  try {
    localStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    const localVideo = document.getElementById("localVideo");
    localVideo.srcObject = localStream;
    console.log("Open camera successfully");
  } catch (error) {
    console.error("Open camera unsuccessfully", error);
  }
}

camBtn.addEventListener("click", () => {
  if (localStream) {
    const videoTrack = localStream.getVideoTracks()[0];
    if (isCamOn) {
      videoTrack.enabled = false;
      camIcon.innerText = "video_camera_front_off";
      camBtn.classList.add("btn-danger");
      isCamOn = false;
    } else {
      videoTrack.enabled = true;
      camIcon.innerText = "video_camera_front";
      camBtn.classList.remove("btn-danger");
      isCamOn = true;
    }
  }
});

micBtn.addEventListener("click", () => {
  if (localStream) {
    const audioTrack = localStream.getAudioTracks()[0];
    if (isMicOn) {
      audioTrack.enabled = false;
      micIcon.innerText = "mic_off";
      micBtn.classList.add("btn-danger");
      isMicOn = false;
    } else {
      audioTrack.enabled = true;
      micIcon.innerText = "mic";
      micBtn.classList.remove("btn-danger");
      isMicOn = true;
    }
  }
});

msgBtn.addEventListener("click", () => {
  if (isChatOpen) {
    chatBox.classList.add("hidden");
    isChatOpen = false;
  } else {
    chatBox.classList.remove("hidden");
    isChatOpen = true;
  }
});

async function startRecording() {
  try {
    const screenStream = await navigator.mediaDevices.getDisplayMedia({
      video: true,
    });
    console.log("Da lay duoc hinh anh ma hinh", screenStream);
    const audioCtx = new AudioContext();
    const dest = audioCtx.createMediaStreamDestination();
    if (localStream && isMicOn) {
      const localSource = audioCtx.createMediaStreamSource(localStream);
      localSource.connect(dest);
    }
    if (remoteStream && remoteStream.getAudioTracks().length > 0) {
      const remoteSource = audioCtx.createMediaStreamSource(remoteStream);
      remoteSource.connect(dest);
      console.log("Da them voice cua doi phuong");
    } else {
      console.log("chua co am thanh");
    }
    const videoTrack = screenStream.getVideoTracks()[0];
    const audioTrack = dest.stream.getAudioTracks()[0];
    const combinedStream = new MediaStream([videoTrack, audioTrack]);

    mediaRecorder = new MediaRecorder(combinedStream);
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data);
      }
    };
    recordedChunks = [];

    mediaRecorder.start();
    return true;
  } catch (err) {
    console.error("Loi hoac da huy", err);
    return false;
  }
}

function stopRecording() {
  if (mediaRecorder && isRecording) {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
      if (recordedChunks.length > 0) {
        const blob = new Blob(recordedChunks, { type: "video/webm" });
        const videoURL = URL.createObjectURL(blob);

        downloadVideo(videoURL);
      } else {
        console.warn("Khong co du lieu nao duoc ghi lai");
      }
    };
  }
}

function downloadVideo(url) {
  const a = document.createElement("a");
  a.style.display = "none";
  a.href = url;
  a.download = `Cuoc-goi-${Date.now()}.webm`;
  document.body.appendChild(a);
  a.click();

  setTimeout(() => {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 100);
}

recordBtn.addEventListener("click", async () => {
  if (!isRecording) {
    const success = await startRecording();
    if (success) {
      isRecording = true;
      recordIcon.innerText = "stop_circle";
      recordBtn.classList.add("btn-danger");
    }
  } else {
    stopRecording();
    isRecording = false;
    recordIcon.innerText = "screen_record";
    recordBtn.classList.remove("btn-danger");
  }
});

joinBtn.addEventListener("click", () => {
  const roomID = roomInput.value;
  if (roomID.trim() !== "") {
    console.log("Tham gia phòng: ", roomID);
    lobby.classList.add("hidden");
    screen.classList.remove("hidden");

    peer = new Peer(roomID);
    peer.on("open", (id) => {
      console.log("Đã kết nối với ID:", id);
    });

    openCamera();
  } else {
    alert("Vui lòng nhập mã phòng!");
  }
});

createRoomBtn.addEventListener("click", () => {
  // Ẩn nút "Tạo phòng mới" và hiện khu vực cài đặt
  createRoomBtn.classList.add("hidden");
  hostSetup.classList.remove("hidden");

  // Khởi tạo Peer không truyền tham số để tự động sinh ID ngẫu nhiên
  peer = new Peer(); 

  peer.on("open", (id) => {
    console.log("Mã phòng vừa được tạo là:", id);
    
    // NHIỆM VỤ: Hiển thị id này lên màn hình
    generatedIdText.innerText = id;
  });
});

startCallBtn.addEventListener("click", () =>{
  lobby.classList.add("hidden");
  screen.classList.remove("hidden");
  openCamera();
})

roomPass.addEventListener("change", () => {
  if (roomPass.checked) {
    roomPassContainer.classList.remove("hidden");
  } else {    
    roomPassContainer.classList.add("hidden");
    roomPassInput.value = "";
  }
});