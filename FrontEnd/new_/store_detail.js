
// 체크된 메뉴 인덱스 찾기
var checkIndex = [];

function addCheck(){
  var chs = document.getElementsByName("choose");
  checkIndex = [];
  for(var i=0; i<chs.length; i++){

      if(chs[i].checked==true){

         checkIndex.push(i);
      }
  }
  console.log(checkIndex);
}

// 찾은 인덱스 내 주문 옵션으로 불러오기

let showMyMenu = () => {
  removeAllchild(); // 초기화

  for(var i=0; i<checkIndex.length;i++){
    
    const foodName = document.getElementsByClassName("foodName")[checkIndex[i]].innerText;
    var price = document.getElementsByClassName("price")[checkIndex[i]].innerText;

    let Area = document.querySelector(".order_content");
    let orderList = document.createElement('div');
    orderList.setAttribute('class','orderList');

    let fn = document.createElement('div');
    fn.setAttribute('class','FN');

    let count = document.createElement('div');
    count.setAttribute('class','count');

    let amount = document.createElement('input');
    amount.setAttribute('type','number')
    amount.setAttribute('class','amount');    
    amount.setAttribute('value','1');
    amount.setAttribute('min','1');
    amount.setAttribute('onchange','sumPirce()')

    let p = document.createElement('div');
    p.setAttribute('class','P')

    Area.appendChild(orderList);
    orderList.appendChild(fn);
    orderList.appendChild(count);
    orderList.appendChild(p);
    count.appendChild(amount);

    fn.innerHTML = foodName;
    p.innerHTML = `${price}원`
  }

  sumPirce();
}

//초기화: order content 안에 생성된 자식 요소 모두 삭제하기 
let removeAllchild = () => {
  const Area = document.querySelector(".order_content");
  while ( Area.hasChildNodes() ){
     Area.removeChild( Area.firstChild );       
  };
}


// 내 주문 옵션에 불려온 가격 총합 구하기 + 변경된 수량값 계산하기
const sumP = document.querySelector(".sumP");

let sumPirce = () => {
  
  var sum = 0;
  var deliver_price = parseInt(document.getElementsByClassName("deliver_price")[0].innerText); 

  for(var i=0; i<checkIndex.length;i++) {
    const changePrice_area = document.getElementsByClassName("P")[i];
    var count = parseInt(document.getElementsByClassName("amount")[i].value);
    var price = parseInt(document.getElementsByClassName("price")[checkIndex[i]].innerText);
    sum += count * (price*1000) ;
    changePrice_area.innerText= `${count * price*1000}원`;
  }
  sum += deliver_price;
  
  sumP.innerText = `${sum}원`;
}


// 찜
const heart = document.querySelector(".heart");

let activeHeart = () => {
  const hasClass = heart.classList.contains("full");

  if(!hasClass){
    heart.classList.add("full");
    heart.innerText = "🧡"
  } else {
    heart.classList.remove("full");
    heart.innerText = "🤍"
  };
}