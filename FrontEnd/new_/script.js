// let content = "\n나만의 WAITER, 이름하여 WE(b)ITER 웨이터\n\n" 
// + "당신의 손짓 하나로 친구들의 메뉴까지 한번에 알려주는\n"
// +"당신만의 스마트한 웹서비스.\n우리는 WE(b)ITER 입니다.\n"
// let text = document.querySelector(".text");
// let i = 0;

// function typing(){
//     if (i < content.length) {
//         let txt = content.charAt(i);
//         if(txt === 'W'){
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         } else if(txt === 'A')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === 'I')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === 'T')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === 'E')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === 'R')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === '(')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === ')')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === 'b')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else if(txt === 'B')
//             text.innerHTML += `<span style="font-weight:bold;">${txt}</span>`;
//         else
//             text.innerHTML += txt=== "\n" ? "<br/>": txt;
//         i++;
//         if(i==content.length){
//             $(".blink").hide();
//         }
//     }
// }
// setInterval(typing, 50)

$(".1").fadeIn(1000, function(){
    $(".2").fadeIn(1000, function(){
        $(".3").fadeIn(1000, function(){
            $(".4").fadeIn(1000);
        });
    });
});

var words = document.getElementsByClassName('word');
var wordArray = [];
var currentWord = 0;

words[currentWord].style.opacity = 1;
for (var i = 0; i < words.length; i++) {
  splitLetters(words[i]);
}

function changeWord() {
  var cw = wordArray[currentWord];
  var nw = currentWord == words.length-1 ? wordArray[0] : wordArray[currentWord+1];
  for (var i = 0; i < cw.length; i++) {
    animateLetterOut(cw, i);
  }
  
  for (var i = 0; i < nw.length; i++) {
    nw[i].className = 'letter behind';
    nw[0].parentElement.style.opacity = 1;
    animateLetterIn(nw, i);
  }
  
  currentWord = (currentWord == wordArray.length-1) ? 0 : currentWord+1;
}

function animateLetterOut(cw, i) {
  setTimeout(function() {
    cw[i].className = 'letter out';
  }, i*80);
}

function animateLetterIn(nw, i) {
  setTimeout(function() {
    nw[i].className = 'letter in';
  }, 340+(i*80));
}

function splitLetters(word) {
  var content = word.innerHTML;
  word.innerHTML = '';
  var letters = [];
  for (var i = 0; i < content.length; i++) {
    var letter = document.createElement('span');
    letter.className = 'letter';
    letter.innerHTML = content.charAt(i);
    word.appendChild(letter);
    letters.push(letter);
  }
  
  wordArray.push(letters);
}

changeWord();
setInterval(changeWord, 2000);