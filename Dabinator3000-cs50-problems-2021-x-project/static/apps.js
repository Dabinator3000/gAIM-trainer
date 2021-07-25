
var c_counter = 0;          //initialising variables for classic game
var c_start = 0;
var c_end = 0;
var c_se = 0;
var c_target = 30;
window.c_avg = 0;

var r_pos = 0;              //initalising variables for rapid game
var r_time = 15000;
var r_not_on =0;
var r_sum = 0;
var r_startn =0;
var r_gate = 0;
var r_score = 0;

function random(min, max) {     //global random alorithm to be accessed by both the games
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min) + min);
      }


function c_modify() {       //main classic game algorithm


    if(c_counter < c_target){
        if (c_counter == 1){
             c_start = Date.now();
        }
        var h = window.screen.availHeight/5;        //randomly spawns target in a given div
        var w = window.screen.availWidth/5;
         var x1 = random(-w,w);
         var x2 = random(-h,h);
         /*console.log(x1,x2);*/
         document.getElementById("ic").style.left = x1+"px";
         document.getElementById("ic").style.top = x2+"px";
         c_counter = c_counter + 1;
        document.getElementById("heading2").innerHTML= c_target - c_counter + "  More to Go";
      }
    if(c_counter == c_target) {     //when target quota is met the game ends
         c_end = Date.now();

        document.getElementById("ic").style.left = "0px";           //targets are reset
        document.getElementById("ic").style.top = "0px";
        c_se = c_end - c_start;
        c_avg = Math.floor(c_se/c_counter);         //score is counted
        console.log(c_avg);                         //score is the average time required to elimitate all the targets
        document.getElementById("heading2").innerHTML= "You took " + Math.floor(c_avg) + " ms to hit each target";
        document.getElementById("save").innerHTML= "Click on the button above to save your results!";
        document.getElementById("score").innerHTML=c_avg;
        c_counter = c_counter + 11;

    }



}


function c_refresh() {      //refreshes the game and target is placed at default position
    c_counter = 0;
    document.getElementById('heading2').innerHTML=  c_target + " More to Go";
    document.getElementById("ic").style.left = "0px";
    document.getElementById("ic").style.top = "0px";
    document.getElementById("save").innerHTML= "";
    document.getElementById("score").innerHTML= "";
    c_start = 0;
    c_end = 0;
}



function c_save() {     //save highscore for classic game
        let xhr = new XMLHttpRequest();
        xhr.open('GET', "/?Xc="+c_avg);
        xhr.send();
}





function r_refresh() {      //refresh  for rapid game
    document.getElementById('heading3').innerHTML=   "  More to Go";
    document.getElementById("img").style.left = "0px";
    document.getElementById("img").style.top = "0px";

    r_not_on =0;
    r_pos = 0;
    r_score = 0;
    r_sum = 0;
    r_startn =0;
    r_gate = 0;


}

function r_comeback() {     //incase the target is too far or outside the div this function will call it back to default postion
    document.getElementById("img").style.left = "0px";
    document.getElementById("img").style.top = "0px";

}
function r_start() {    //starts the rapid game

    if(r_gate > 0)
    {
        stop();


    }
    else {

            jQuery(function($) {        //jQuery for moving the target away based on user's pointer movements; for when user's mouse is over the target
            $('#img').mouseover(function() {
                var dWidth = $("#sa").width() - 100, // 100 = image width
                    dHeight = $("#sa").height(), // 100 = image height
                    nextX = Math.floor(Math.random() /1.2 * dWidth),
                    nextY = Math.floor(Math.random() *1.9 * dHeight);
                $(this).animate({ left: nextX + 'px', top: nextY + 'px' });
            });
        });
        jQuery(function($) {        //jQuery for moving the target away based on user's pointer movements; for when user's mouse is not over the target
            $('#img').mouseout(function() {
                var dWidth = $("#sa").width() - 100, // 100 = image width
                    dHeight = $("#sa").height(), // 100 = image height
                    nextX = Math.floor(Math.random() /1.92 * dWidth),
                    nextY = Math.floor(Math.random() *1.5* dHeight);
                $(this).animate({ left: nextX + 'px', top: nextY + 'px' });
            });
        });


}

}

function rp_timer() { //Calculaes the time user was ON the target
    r_on = Date.now();
}
function rr_timer() {   //Calculates the time use was off the target
    r_not_on = Date.now();
    console.log(r_sum,r_not_on);
    r_sum = r_not_on-r_on  + r_sum;
    console.log(r_sum,r_not_on,r_on);
}
function stop() {       //stop function to terminate the game
    r_gate = r_gate+ 10;
    document.getElementById("img").style.left = "0px";
    document.getElementById("img").style.top = "0px";
    r_score = Math.floor(r_sum*100/r_time);
   document.getElementById('heading3').innerHTML=  r_score +" % Tracking";
}

function r_save() { //save function to save highscores for rapid game
        let xhr = new XMLHttpRequest();
        xhr.open('GET', "/?Xr="+r_score);
        xhr.send();
}
