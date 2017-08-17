$(function() {
    var color_good = function() {
        var btn = $(this);
        var id = btn.parent().attr("id");

        $.ajax({
            url: '/professor/professor_iscorrect/',
            data: {
                'id': id
            },
            dataType: 'json',
            success: function (data) {
                if (data.correction == 1){
                    btn.addClass("btn-success");
                }
            }
        });

        $(this).on("click", function () {

            // Color the button
            btn.addClass("btn-success");

            // Change the heading color
            var panel = btn.parent().parent().parent().parent().parent().parent().parent().parent();
            panel.addClass("panel-success");
            panel.removeClass("panel-warning");
            panel.removeClass("panel-danger");

            // Remove selection color of the other button
            var bad_btn = btn.parent().find(".bad");
            bad_btn.removeClass("btn-danger");

            $.ajax({
                url: '/professor/professor_correct/',
                data: {
                    'correction': 1,
                    'id': id
                },
                dataType: 'json',
                success: function (data) {
                    if (data.result){
                        // msg: Question corrigée
                    }
                    else{
                        // msg: Question déjà corrigée
                    }
                }
            });
        });
    }

    var color_bad = function() {
        var btn = $(this);
        var id = btn.parent().attr("id");

        $.ajax({
            url: '/professor/professor_iscorrect/',
            data: {
                'id': id
            },
            dataType: 'json',
            success: function (data) {
                if (data.correction == 0){
                    btn.addClass("btn-danger");
                }
            }
        });

        $(this).on("click", function () {

            // Color the button
            btn.addClass("btn-danger");

            // Change the heading color
            var panel = btn.parent().parent().parent().parent().parent().parent().parent().parent();
            panel.addClass("panel-danger");
            panel.removeClass("panel-warning");
            panel.removeClass("panel-success");

            // Remove selection color of the other button
            var good_btn = btn.parent().find(".good");
            good_btn.removeClass("btn-success");

            $.ajax({
                url: '/professor/professor_correct/',
                data: {
                    'correction': 0,
                    'id': id
                },
                dataType: 'json',
                success: function (data) {
                    if (data.result){
                        // msg: Question corrigée
                    }
                    else{
                        // msg: Question déjà corrigée
                    }
                }
            });
        });
    }

    var infos = function() {
        var btn = $(this);
        var id = btn.attr("id");

        $(this).on("click", function () {

            // Hide the button
            btn.hide();

            var source = $('#source_' + id);
            var indication = $('#indication_' + id);
            source.show();
            indication.show();

            // Remove selection color of the other button
            var good_btn = btn.parent().find(".good");
            good_btn.removeClass("btn-success");
        });
    }

    var hiddeninfo = function() {
        $(this).hide();
    }

    $(".good").each(color_good);
    $(".bad").each(color_bad);
    $(".infos").each(infos);
    $(".hiddeninfo").each(hiddeninfo);
});