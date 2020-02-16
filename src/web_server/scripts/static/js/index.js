
var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr); // N.B ideally should return xhr.response
      } else {
        callback(status, xhr);
      }
    };
    xhr.send();
};

var date_object = new Date();

var shutdown_btn = document.getElementById("shutdown_btn")
var reset_task_btn = document.getElementById("reset_task_btn");
var eurobot_kill_task_btn = document.getElementById("eurobot_kill_task_btn");
var start_task_purple_btn = document.getElementById("start_task_purple_btn");
var start_task_yellow_btn = document.getElementById("start_task_yellow_btn");


var update_info_btn = document.getElementById("update_info_btn");

var robot_x   = document.getElementById("robot_x");
var robot_y   = document.getElementById("robot_y");
var robot_yaw = document.getElementById("robot_yaw");

var reset_odometry_btn = document.getElementById("reset_odometry_btn");


function update_robot_position()
{
    getJSON(window.location.origin + "/get_robot_position", (status, xhr)=>{
        var data = xhr.response;
        robot_x.value   = (data.x).toFixed(5);
        robot_y.value   = (data.y).toFixed(5);
        robot_yaw.value = ((data.yaw / Math.PI) * 180.0).toFixed(5);
    });

    // let c = document.getElementById("myCanvas");
    // let ctx = c.getContext("2d");
    // ctx.beginPath();
    // ctx.moveTo(0, 0);
    // ctx.lineTo(robot_x.value, robot_y.value);
    // ctx.stroke();
}

var time_elapsed_val = document.getElementById("time_elapsed_val");

function update_time_elapsed()
{
    getJSON(window.location.origin + "/get_time_elapsed", (status, xhr)=>{
        var data = xhr.response;
        time_elapsed   = data;
        // console.log(time_elapsed);
        // JSON.stringify(time_elapsed);
        time_elapsed_val.value = JSON.stringify(time_elapsed);
        
    });
}

setInterval(update_time_elapsed, 1000);


setInterval(update_robot_position, 1000);

reset_odometry_btn.onclick = function()
{
    var q = "?t=" + date_object.getTime();
    getJSON(window.location.origin + "/reset_odometry" + q, ()=>{});
}



reset_task_btn.onclick = function()
{
    console.log("reset task");

    var q = "?t=" + date_object.getTime();
    getJSON(window.location.origin + "/eurobot_task_reset" + q, ()=>{});
}

start_task_purple_btn.onclick = function()
{
    console.log("task purple");
    getJSON(window.location.origin + "/eurobot_start_purple", ()=>{});
}

start_task_yellow_btn.onclick = function()
{
    console.log("task yellow");

    var q = "?t=" + date_object.getTime();
    getJSON(window.location.origin + "/eurobot_start_yellow" + q, ()=>{});
}

eurobot_kill_task_btn.onclick = function()
{
    console.log("kill task");

    var q = "?t=" + date_object.getTime();
    getJSON(window.location.origin + "/eurobot_kill_task" + q, ()=>{});
}

shutdown_btn.onclick = function()
{
    console.log("shutdown")

    var q = "?t=" + date_object.getTime();
    getJSON(window.location.origin + "/shutdown" + q, ()=>{});
}
