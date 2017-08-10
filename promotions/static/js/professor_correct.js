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
                        alert("Question corrigée ! Good");
                    }
                    else{
                        alert("La question a déjà été corrigée ! Good");
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
                        alert("Question corrigée ! Bad");
                    }
                    else{
                        alert("La question a déjà été corrigée ! Bad");
                    }
                }
            });
        });
    }

    $(".good").each(color_good);
    $(".bad").each(color_bad);

    /*$(".btn.btn-default.good").each(function (index) {
        $(this).on("click", function () {
            var id = this.name;

            $.ajax({
                url: '/professor/professor_correct/',
                data: {
                    'fff': 1
                },
                dataType: 'json',
                success: function (data) {
                    if (data.correct) {
                        alert(id);
                    }
                }
            });
        });
    });*/
});