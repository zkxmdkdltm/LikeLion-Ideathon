function check_pw(){
    var pw = document.getElementById('pw').value;
    var SC = ['*','-','.',"/","!","@","#","$","%"];
    var check_SC = 0;

    if(pw.length < 6 || pw.length>16){
        window.alert('비밀번호는 6글자 이상, 16글자 이하만 이용 가능합니다.');
        document.getElementById('pw').value='';
    }
    for(var i=0;i<SC.length;i++){
        if(pw.indexOf(SC[i]) != -1){
            check_SC = 1;
        }
    }
    if(check_SC == 0){
        window.alert('*, -, ·, /, !, @, #, $, % 의 특수문자가 들어가 있지 않습니다.')
        document.getElementById('pw').value='';
    }
    if(document.getElementById('pw').value !='' && document.getElementById('pw2').value!=''){
        if(document.getElementById('pw').value==document.getElementById('pw2').value){
            document.getElementById('check').innerHTML='비밀번호가 일치합니다.'
            document.getElementById('check').style.color='blue';
        }
        else{
            document.getElementById('check').innerHTML='비밀번호가 일치하지 않습니다.';
            document.getElementById('check').style.color='red';
        }
    }
}
function onlyAlphabet(ele) {
    ele.value = ele.value.replace(/[^\\!-z]/gi,"");
}

$(document).on("keyup", "input[numberOnly]", function() {$(this).val( $(this).val().replace(/[^0-9]/gi,"") );})
$(document).on("keyup", "input[koOnly]", function() {$(this).val( $(this).val().replace(/[^ㄱ-힣]/gi,"") );})
$(document).on("keyup", "input[EngNumOnly]", function() {$(this).val( $(this).val().replace(/[^a-zA-Z0-9]/gi,"") );})
