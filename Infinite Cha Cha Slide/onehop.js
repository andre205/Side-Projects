var filenames = `back.wav
back_1.wav
back_2.wav
back_3.wav
back_4.wav
back_5.wav
back_6.wav
back_7.wav
chaCha.wav
chaCha_1.wav
chaCha_2.wav
chaCha_3.wav
chaCha_4.wav
chaCha_5.wav
chaCha_6.wav
charlieBrown.wav
clap.wav
clapping.wav
crissCross.wav
crissCross_1.wav
everybodyClap.wav
fiveHops.wav
handsOnYourKnees.wav
hop.wav
intro.wav
left.wav
leftAgain.wav
leftStomp.wav
leftStomp_1.wav
leftStomp_2.wav
leftStomp_3.wav
leftStomp_4.wav
leftStomp_5.wav
leftTwoStomp.wav
leftTwoStomp_1.wav
left_1.wav
left_2.wav
left_3.wav
left_4.wav
left_5.wav
left_6.wav
low.wav
oneHop.wav
oneHop_1.wav
oneHop_2.wav
oneHop_3.wav
oneHop_4.wav
oneHop_5.wav
oneHop_6.wav
reverse.wav
reverse_1.wav
reverse_2.wav
reverse_3.wav
right.wav
rightAgain.wav
rightStomp.wav
rightStomp_1.wav
rightStomp_2.wav
rightStomp_3.wav
rightStomp_4.wav
rightStomp_5.wav
rightTwoStomp.wav
rightTwoStomp_1.wav
slideLeft.wav
slideLeft_1.wav
slideLeft_2.wav
slideRight.wav
slideRight_1.wav
slideRight_2.wav
top.wav
twoHops.wav
twoHops_1.wav
twoHops_2.wav
twoHops_3.wav`

var test = [];
var p = [];
var f = filenames.split("\n");
for (i = 0; i < f.length; i++) {
    //console.log(f[i]);
    var a = new Audio('files/' + f[i]);
    a.ontimeupdate = updateTime;
    p.push(a);
}

var stop = true;
var first = true;
var index = 24;

function pClick() {
    if(!stop)
    {
        document.getElementById("p").innerHTML = "PLAY";
        pauseAll();
    }
    else {
        document.getElementById("p").innerHTML = "PAUSE";
    }
    //console.log("C Clicked");
    stop = !stop;

    p[index].onended = playRand;

    if(first)
    {
        //document.getElementById('track').play();
        index = 24;
        p[24].onended = playRand;
        p[24].play();
        document.getElementById("par").innerHTML = "Playing " + f[index].slice(0,-4);
        first = false;
    }
    else {
        playRand();
    }

}

function playRand(){
    {
        if(!stop)
        {
            index = Math.floor(Math.random() * p.length);
            if (index == 24)
            {
                index = 25;
            }
            document.getElementById("par").innerHTML = "Playing " + f[index].slice(0,-4);
            //console.log("playing " + index);

            p[index].play();
            //p[index].onended = playRand;

        }
        else {
            document.getElementById("par").innerHTML = "You're killing it!";
        }
    }
}

function testClick(){

    console.log(p[index].currentTime);
    console.log(p[index].duration);

    p[index].pause();
    p[index].currentTime = p[index].duration;


}

function updateTime(){
    if(p[index].currentTime >= p[index].duration - .1)
    {
        p[index].pause();
        playRand();
    }

    try{
        document.getElementById('tracktime').innerHTML = Math.floor(p[index].currentTime) + ' / ' + Math.floor(p[index].duration);
    }
    catch(err)
    {
        console.log(err);
    }
}

function pauseAll() {
    for (i = 0; i < p.length; i++) {
        //console.log(f[i]);
        p[i].pause();
    }
}
