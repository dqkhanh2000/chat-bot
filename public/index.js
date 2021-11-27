$("#button-send").click(() => {
  let message = $("#message").val().trim();
  if (message.length === 0) {
    return;
  }

  let data = {
    question: message,
  };

  let url = `http://${location.hostname}:${location.port}/api/chat`;

  $.post(url, data, function (data, status) {
    data = JSON.parse(data);
    console.log(data)
    if (status === "success" && data.confident > 0.1) {
      addMessage(data.answer, false);
    } else {
      addMessage(
        "Em xin xin lỗi, em không hiểu được anh đang nói gì nè, có thể do em đang còn nhỏ tuổi quá, mong anh thông cảm nhe, em sẽ học dần dần để cố gắng trả lời anh nè ^_^",
        false
      );
    }

    scrollToNewMessage();
  });

  addMessage(message);
  $("#message").val("");
  scrollToNewMessage();
});

function scrollToNewMessage() {
  $("#chat-area").animate({ scrollTop: $("#chat-area").height() + 1000 }, 100);
}

function addMessage(message, sender = true) {
  let html;
  if (sender) {
    html =
      `<div class="d-flex flex-row-reverse p-3">` +
      `<img src="https://img.icons8.com/color/48/000000/circled-user-male-skin-type-7.png" width="50" height="50">` +
      `<div class="bg-white mr-2 p-3"><span class="text-muted">${message}</span>` +
      `</div>`;
  } else {
    html =
      `<div class="d-flex flex-row p-3">` +
      `<img src="https://img.icons8.com/color/48/000000/broken-robot.png" width="50" height="50">` +
      `<div class="chat ml-2 p-3">${message}</div>` +
      `</div>`;
  }
  $("#chat-area").append(html);
}
