var classes;

$(document).ready(function(){

    $('body').css('display', 'none');
    $('body').fadeIn(350);
    table = $('tbody')
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
        .then(() => {

            if(!classes){
                showError("raspored ne postoji")
                return false
            } else {
                window.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: 'smooth'
                });
                showSchedule()
                fillSchedule()
            }

        })
        .catch(error => alert(error))
        
        return false
    });

    $("#nazad").click(function(){
        location.reload()
    })

    function unshowSchedule(){
        $('#schedule').fadeOut(200)
        $('#courseform').fadeIn(200)
        $('#courseform').attr('hidden')
        $('#schedule').removeAttr('hidden')
    }

    function showSchedule(){
        $('#schedule').fadeIn(200)
        $('#courseform').fadeOut(200)
        $('#courseform').attr('hidden')
        $('#schedule').removeAttr('hidden')
    }

    function fillSchedule(){
        classes.sort((a, b) => {
            if(a.day != b.day){
                return b.day - a.day
            } else {
                return b.end - a.end
            }
        })
        for(c in classes){
            placeInTable(classes[c])
        }
    }

    function cleanTable(course){
        rows = table.children()
        day = rows[course.day]
        td = (day.children)[course.start-7]
        td.textContent = `${course.description}`
        if(course.course_type != 'lecture'){
            td.textContent += `\n(${course.course_type[0] == 'e' ? 'vezbe' : 'praktikum'})`
        }
        td.setAttribute('colspan', course.duration)
    }

    function hashCode(str) { // java String#hashCode
        var hash = 0;
        for (var i = 0; i < str.length; i++) {
           hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        return hash;
    } 
    
    function intToRGB(i){
        i = hashCode(i)
        var c = (i & 0x00FFFFFF)
            .toString(16)
            .toUpperCase();
    
        return "00000".substring(0, 6 - c.length) + c;
    }
    

    function placeInTable(course){
/*         td = $(`#td-${course.day}-${course.start-7}`)
        console.log(`#td-${course.day}-${course.start-7}`)
        td.text(course.description + " " + course.course_type)
  */       
        rows = table.children()
        day = rows[course.day]
        td = (day.children)[course.start-7]
        td.textContent = course.description
        if(course.course_type != 'lecture'){
            td.textContent += `\n(${course.course_type[0] == 'e' ? 'vezbe' : 'praktikum'})`
        }
        td.setAttribute('colspan', course.duration)
        td.setAttribute('hashcode', hashCode(td.textContent))
        td.style.background = `#${intToRGB(course.description)}`
        /* url('/static/img/bg.png') left top"; */
        /*td.style.color = '#ffffff' */

        for(let i = 1; i < course.duration; i++){
            excess = (day.children)[course.start-6]
            excess.remove()
        }
    }

    function showError(msg){
        alert(msg)
    }

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