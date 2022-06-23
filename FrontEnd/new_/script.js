let content = "나만의 WAITER, 이름하여 WE(b)ITER 웨이터\n" 
+ "WE BITE 우리는 항상 끊임없이 음식을 먹습니다.\n"
+ "당신의 손짓 하나로 친구들의 메뉴까지 한번에 알려주는\n"
+"당신만의 스마트한 웹서비스.\n우리는 WE(b)iter 입니다.\n"
let text = document.querySelector(".text");
let i = 0;

function typing(){
    if (i < content.length) {
        let txt = content.charAt(i);
        text.innerHTML += txt=== "\n" ? "<br/>": txt;
        i++;
        if(i==content.length){
            $(".blink").hide();
        }
    }
}
setInterval(typing, 100)
