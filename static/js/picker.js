$(document).ready(function(){

    $('body').css('display', 'none');
    $('body').fadeIn(350);

    $("#courseform").submit(function(){
        console.log($(':checkbox:checked'))
        return false
    });

    function generateCode(cbs){
        let code = [0, 0, 0, 0];
        for(let i = 0; i < 4; i++){
            code[i] = cbs[i].checked ? 1 : 0 
        }
        return code.join("");
    }

    function showCourses(courses){
        
    }

});