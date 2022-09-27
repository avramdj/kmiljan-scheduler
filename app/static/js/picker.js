var schedules;
var cur;

$(document).ready(function(){

    const smer = $('#smer').text();
    table_parent = $("#tableparent")
    empty_table = $('#table').clone()
    processing = false
    $('body').fadeIn(350);

    $("#coursebtn").click(function(){

        if(processing){
            return;
        }
        processing = true

        $('#courseform').fadeOut(200)

        showLoading()

        let picked = {}
        let checked = $(':checkbox:checked')
        checked.each(function(){
            let name = $(this).attr("id")
            let selected = $("[course='"+name+"']:selected")
            prefs = {}
            selected.each(function(){
                prefs[$(this).attr("ctype")] = $(this).attr("value")
            })
            picked[$(this).attr('id')] = prefs
        })
        console.log(picked)

        fetch(`/api/scheduler/${smer}`, {
            method: 'POST',
            body: JSON.stringify(picked),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => { 
            schedules = data['schedules']
            $("#schedule-counter").html(`Schedule 1/${schedules.length}`);
        })
        .then(() => console.log(schedules))
        .then(() => {

            hideLoading()

            if(schedules.length == 0){
                showError("raspored ne postoji")
                hideSchedule()
            } else {
                window.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: 'smooth'
                });
                fillSchedule(0)
                showSchedule()
            }
        })
        .catch(error => alert(error))
        processing = false
    });

    $("#nazad").click(hideSchedule)

    $("#home").click(function(){
        window.location = '/';
    })

    $("#sledeci").click(function(){
        if(cur < schedules.length-1) {
            cleanTable()
            fillSchedule(cur+1)
            $("#schedule-counter").html(`Schedule ${cur+1}/${schedules.length}`);
        }
    })

    $("#prethodni").click(function(){
        if(cur > 0) {
            cleanTable()
            fillSchedule(cur-1)
            $("#schedule-counter").html(`Schedule ${cur+1}/${schedules.length}`);
        }
    })

/*     $("input.checkbox").change(function(){
        $(this).next().next().slideToggle()
    })
    function unshowSchedule(){
        $('#schedule').fadeOut(200)
        $('#courseform').fadeIn(200)
        $('#courseform').attr('hidden')
        $('#schedule').removeAttr('hidden')
    }
 */

    function hideSchedule(){
        $('#schedule').fadeOut(200, ()=>{
            $('#courseform').fadeIn(200)
            $('#schedule').attr('hidden')
            $('#courseform').removeAttr('hidden')
            cleanTable()
        })
    }

    function showSchedule(){
        $('#courseform').fadeOut(200, ()=>{
            $('#schedule').fadeIn(200)
            $('#courseform').attr('hidden')
            $('#schedule').removeAttr('hidden')
        })
    }

    function showLoading(){
        $("#loading").fadeIn(50)
    }

    function hideLoading(){
        $("#loading").fadeOut(50)
    }

    function fillSchedule(i){
        cur = i;
        for(c in schedules[i]){
            placeInTable(schedules[i][c])
        }
    }

    function cleanTable(course){
        table_parent.find(":first-child").remove()
        table_parent.prepend(empty_table)
        empty_table = $('#table').clone()
    }

    function hashCode(str){
        str += str;
        var hash = 0;
        for (var i = 0; i < str.length; i++) {
           hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        hash = hash < 0 ? -hash : hash;
        return hash.toString();
    } 
    
    function intToRGB(i){
        i = hashCode(i)
        var c = (i & 0x00FFFFFF)
            .toString(16)
            .toUpperCase();
    
        return "00000".substring(0, 6 - c.length) + c;
    }
    
    function getRandomColor(name) {
        var letters = 'ACDEF'.split('');
        var color = '';
        for (var i = 0; i < 6; i++ ) {
            color += letters[hashCode(name)[i] % letters.length];
        }
        return color;
    }

    function placeInTable(course){
/*         td = $(`#td-${course.day}-${course.start-7}`)
        console.log(`#td-${course.day}-${course.start-7}`)
        td.text(course.description + " " + course.course_type)
  */       
        table = $('tbody')
        rows = table.children()
        day = rows[course.day]
        td = (day.children)[course.start-7]
        td.innerHTML = course.description
        if(course.course_type != 'lecture'){
            td.innerHTML += ` (${course.course_type[0] == 'e' ? 'vezbe' : 'praktikum'})`
        }
        td.innerHTML += `<br/>${course.teacher}`
        td.innerHTML += `<br/>${course.classroom}`
        td.setAttribute('colspan', course.duration)
        td.setAttribute('hashcode', hashCode(td.innerHTML))
        td.style.background = `#${getRandomColor(course.description)}`
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

    function showSchedules(schedules){
        console.log(schedules)
    }

});