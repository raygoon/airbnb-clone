const clockTitle = document.querySelector(".my_clock");

function nowDate() {
  const now = new Date();
  // const dTime = now.getTime();
  const dSec = ("00" + now.getSeconds().toString()).slice(-2);
  const dMin = ("00" + now.getMinutes().toString()).slice(-2);
  const dHour = ("00" + now.getHours().toString()).slice(-2);
  const dDay = ("00" + now.getDate().toString()).slice(-2);
  const dMon = ("00" + (now.getMonth() + 1).toString()).slice(-2);
  const dYear = now.getFullYear();
  clockTitle.textContent = `${dYear}-${dMon}-${dDay}-${dHour}-${dMin}-${dSec}`;
}

function hideMessage() {
  var hideObj = document.querySelector(".message-in");
  hideObj.classList.replace("message-in", "message-out");
  // hideObj.style.display = "none";
}

function transformMessage() {
  var transformObj = document.querySelector(".message");
  transformObj.classList.add("message-in");
}

nowDate();
setInterval(nowDate, 1000);
