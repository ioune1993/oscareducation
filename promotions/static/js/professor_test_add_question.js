$(function() {
    var add_question = function() {
        var btn = $(this);

        btn.on("click", function () {

            $.ajax({
                url: '/professor/professor_test_add_question/',
                data: {
                    'skill': skill,
                    'test_exercice': test_exercice,
                },
                dataType: 'json',
                success: function (data) {

                }
            });
        });
    }

    $(".add_question").each(add_question);
});