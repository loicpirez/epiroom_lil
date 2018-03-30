
String.prototype.toTitleCase = function () {
  return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

let card_id = 1

var createCard = function(data, room) {
  rooms = data['rooms']
  taken_col = ["free", "warning", "busy"]
  all_day = rooms[room] == undefined
  taken = (!rooms[room]) ? 0 : rooms[room]['taken']
  acti = (!rooms[room]) ? "Libre" : rooms[room]["course"]["description"]
  state = (taken == 0.1) ? "free" : taken_col[taken * 2]
  percent = (!rooms[room]) ? 100 : rooms[room]['percent']
  let intl = new Intl.NumberFormat("arab", {minimumIntegerDigits: 2});
  time = (!rooms[room]) ? "Toute la journée" : rooms[room]["time"].split('.')[0]
  if (time != "Toute la journée") {
    let dt = new Date()
    let time_s = time.split(':')
    dt.setHours(time_s[0])
    dt.setMinutes(time_s[1])
    dt.setSeconds(time_s[2])
    inc = 1
    if (taken >= 0.5)
      inc = -1
    time = `${intl.format(dt.getHours())}:${intl.format(dt.getMinutes())}:${intl.format(dt.getSeconds() + 1)}`
    time = "<div inc='" + inc + "' class='time text-center'>" + time + "</div>"
  } else
    time = "<div class='text-center'>Toute la journée</div>"
  card = $("<div class='col-12 card-box'>\
              <div class='card text-white bg-" + state + "'>\
                <div class='card-header'><b style='display: inline-block; width: 80%;white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>" + room.toTitleCase() + "</b></div>\
                <div class='card-body'>\
                  <b style='text-align: center; display: inline-block; width: 100%;white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>" + acti.toTitleCase() + "</b>\
                  <div class='progress' style='margin-bottom: 5px; background: none; border: 1px solid #fff; height: 10px'>\
                    <div class='progress-bar' style='width: " + percent + "%; background: #fff'></div>\
                  </div>" + time + "\
                </div>\
              </div>\
            </div>")
  col = parseInt(card_id / (max_room_col + 1)) + 1
  card_id += 1
  $(".col" + col).append(card)
}

var setRoom = function(data, room, taken) {
  var rooms = data['rooms']
  var date = null
  fill_color = ["#27ae60", "#ffb300", "#e74c3c"]
  createCard(data, room)
  $('#svg svg #' + room).css('fill', fill_color[taken * 2])
}

var refresh_time = function(elm, inc) {
  let intl = new Intl.NumberFormat("arab", {minimumIntegerDigits: 2});
  let time = new Date()
  let time_s = elm.html().split(':')
  time.setHours(time_s[0])
  time.setMinutes(time_s[1])
  time.setSeconds(time_s[2])
  time.setSeconds(time.getSeconds() + parseInt(elm.attr('inc')))
  elm.html(`${intl.format(time.getHours())}:${intl.format(time.getMinutes())}:${intl.format(time.getSeconds())}`)
}

var api_request = function() {
  $('#reload').css('display', "block")
  $.ajax({
    dataType: "json",
    url: "/api/dispo"
  }).done(function(data) {
    card_id = 1
    let now = new Date(data['time_now'])
    let intl = new Intl.NumberFormat("arab", {minimumIntegerDigits: 2});
    $('#hour').html(`${intl.format(now.getHours())}:${intl.format(now.getMinutes())}:${intl.format(now.getSeconds())}`)
    let rooms = data['rooms']
    $('.col1').html("")
    $('.col2').html("")
    $('#svg svg path').css('fill', 'none')
    for (key in rooms)
      setRoom(data, key, rooms[key] ? rooms[key].taken : 0)
    $('#reload').css('display', "none")
  })
}

window.setInterval(api_request, 60000)
window.setTimeout(function() {
  window.setInterval(function() {
    refresh_time($("#hour"), 1)
    $(".card-box .card-body .time").each(function(id) {
      refresh_time($(".card-box .card-body .time").eq(id), -1)
      if ($(".card-box .card-body .time").eq(id).html() == "00:00:00")
        api_request()
    })
  }, 1000)
}, 1000)
api_request()
