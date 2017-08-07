$(function(){

    let countFiles = 0;
    let countLinks = 0;
    let countitems = 0;

    $('.addMore').on('click', function( event ){

        event.preventDefault();

        let target = $( this ).data( 'target' );
        let newElement
        countitems++

        switch( target ){

            case 'file':
                
                countFiles++

                newElement = $('#personal_resource ul li.file').eq(0).clone()
                
                console.log('file', newElement )
                $('#personal_resource ul').append( newElement )
                $(newElement).removeClass('hidden');
                $('.btn-files').children('span.badge').text(countFiles)

            break;


            case 'link':
                countLinks++
                newElement = $('#personal_resource ul li.link').eq(0).clone()
                console.log('link', newElement )
                $('#personal_resource ul').append( newElement )
                $(newElement).removeClass('hidden');
                $('.btn-links').children('span.badge').text(countLinks)

            break;

                $( newElement ).children('span.badge').text(countitems)



        }
        



    })



})