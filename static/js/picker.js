var classes;

$(document).ready(function(){

    $('body').css('display', 'none');
    $('body').fadeIn(350);
    const smer = $('#smer').text();

    $("#courseform").submit(function(){

        let picked = []
        let checked = $(':checkbox:checked')
        checked.each(function(){
            picked.push($(this).attr('id'))
        })


        fetch(`/api/scheduler/${smer}`, {
            method: 'POST',
            body: JSON.stringify(picked),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => classes = data['courses'])
        .then(() => console.log(classes))

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
        console.log(courses)
    }

});