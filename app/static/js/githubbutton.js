$(() => {

    ghlogo = $("#ghlogo")
    ghlink = $('#ghlink')

    ghlink.css('display', 'none');

    ghlogo.hover(function(){
        //enter
        ghlogo.stop().fadeTo(250, 1)
        ghlink.stop().fadeToggle(250)
    }, function(){
        //leave
        ghlogo.stop().fadeTo(250, 0.5)
        ghlink.stop().fadeToggle(250)
    })

    /* ghlogo.on("click", function(){
        document.location.href = "https://github.com/avramdj/Smolify"
    }) */
    
})