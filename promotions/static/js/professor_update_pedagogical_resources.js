$(function(){

    countFiles = 0;
    countLinks = 0;
    countitems = 0;

    $('.addMore').on('click', function( event ){
        event.preventDefault();

        let target = $( this ).data( 'target' );
        let newElement;
        countitems++;

        switch( target ){

            case 'file':
                // TODO : TO OPTIMIZE
                countFiles++;
                newElement = $(this).closest('div.panel-body').find('#form_resource ul li.file').eq(0).clone(true,true);
                $(newElement).find('.clearablefileinput').attr("name","file_"+countFiles);
                $(newElement).find('.form-control').attr("name","file_type_"+countFiles);
                $(newElement).find('.textinput').attr("name", "file_name_"+countFiles);
                $(this).closest('div.panel-body').find('#form_resource').append( newElement );
                $(newElement).removeClass('hidden');
                $('.btn-files').children('span.badge').text(countFiles);

            break;


            case 'link':
                // TODO : TO OPTIMIZE
                countLinks++;
                newElement = $(this).closest('div.panel-body').find('#form_resource ul li.link').eq(0).clone(true,true);
                $(newElement).find('.urlinput.form-control').attr("name","url_"+countLinks);
                $(newElement).find('.select.form-control').attr("name","link_type_"+countLinks);
                $(newElement).find('.textinput.textInput.form-control').attr("name", "link_name_"+countLinks);
                $(this).closest('div.panel-body').find('#form_resource').append( newElement );
                $(newElement).removeClass('hidden');
                $('.btn-links').children('span.badge').text(countLinks);

            break;

                $( newElement ).children('span.badge').text(countitems)

        }
    });

    $('.remove').on('click', function( event ){
        var confirm = window.confirm("Ok ?");
        if (confirm) {
            target = $( this ).data( 'target' );
            event.preventDefault();
            $(this).parent().parent().remove();
            console.log(target);
            switch (target) {
                case 'file':
                    countFiles--;
                    $('.btn-files').children('span.badge').text(countFiles);

                    break;

                case 'link':
                    countLinks--;
                    $('.btn-links').children('span.badge').text(countLinks);
                    break;
            }
        }
    });

});