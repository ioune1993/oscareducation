$(function() {
    var modify = function() {
        var btn = $(this);
        var id = btn.attr("id");

        btn.on("click", function () {

            var new_name = $("#new_name").val();

            $.ajax({
                url: '/professor/professor_rename_test/',
                data: {
                    'id': id,
                    'name': new_name
                },
                dataType: 'json',
                success: function (data) {
                    $(".test-name").html(data.name);
                    $("#name_modified_message").show().delay(2000).fadeOut();
                }
            });
        });
    }

    $(".modify").each(modify);
});