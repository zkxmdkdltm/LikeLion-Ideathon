let content = "당신이 호스트가 되어, 지인들의 주문을 받을 수 있습니다.\n"
+ "음식점을 탐색해보세요!\n또는 다른 호스트의 주문에 참여 해 보세요!\n"
let text = document.querySelector(".text2");
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
setInterval(typing, 50)