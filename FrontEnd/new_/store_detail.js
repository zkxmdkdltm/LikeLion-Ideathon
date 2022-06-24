var food = document.querySelectorAll('.food');
var foodindex = 0; 
const follow_content = document.querySelector(".order_content");



function food_click(idx){
  food[idx].onclick = function(){
    foodindex = idx;
    const foodName = document.getElementsByClassName("foodName")[foodindex].innerText;
    var price = document.getElementsByClassName("price")[foodindex].innerText;
    
    let Area = document.querySelector(".order_content");
    let orderList = document.createElement('div');
    orderList.setAttribute('class','orderList');
    let fn = document.createElement('div');
    fn.setAttribute('class','FN');
    let count = document.createElement('div');
    count.setAttribute('class','count');
    let amount = document.createElement('input');
    amount.setAttribute('type','number')
    amount.setAttribute('name','amount');
    amount.setAttribute('value','1');
    amount.setAttribute('min','1');
    let p = document.createElement('div');
    p.setAttribute('class','P')

    Area.appendChild(orderList);
    orderList.appendChild(fn);
    orderList.appendChild(count);
    orderList.appendChild(p);
    count.appendChild(amount);
    fn.innerHTML = foodName;
    p.innerHTML = price;
    
    const sumPrice = document.querySelector('.sumP');
    const sumP = 0;
    sumPrice.innerText = `${sumP}원`;

    console.log(foodName);
    console.log(price);
  };
}

for(var i=0; i<food.length; i++){
  food_click(i);  
}