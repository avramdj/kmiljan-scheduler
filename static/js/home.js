$(document).ready(function(){

    $('body').css('display', 'none');
    $('body').fadeIn(350);
    $('#years').hide()
    if($("#smer option:selected").val().length){
        $('#years').show()
    }

    $('#smer').on('change', function(){
        $('#years').slideDown(350);
    })

    $("#smerform").submit(function(e){
        e.preventDefault();
        const selected = $("#smer option:selected").val();
        if(!selected.length){
            console.log('err')
        }

        let code = generateCode($(':checkbox'));

/*         fetch(`/api/${selected}/${code}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => {
            showCourses(res.json())
        })
         */
        
        window.location.href = `/picker/${selected}/${code}`;

        return false;
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