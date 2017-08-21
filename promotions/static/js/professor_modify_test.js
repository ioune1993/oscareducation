$(function() {
    var modify_name = function() {
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

    var add_question = function() {
        var btn = $(this);

        btn.on("click", function () {

            var id = btn.attr("id");

            $.ajax({
                url: '/professor/professor_test_add_question/',
                data: {
                    'id': id,
                },
                dataType: 'json',
                success: function (data) {
                    // Refresh the page
                    location.reload();
                }
            });
        });
    }

    var delete_question = function() {
        var btn = $(this);

        btn.on("click", function () {

            var id = btn.attr("id");

            $.ajax({
                url: '/professor/professor_test_delete_question/',
                data: {
                    'test_exercice_id': id,
                },
                dataType: 'json',
                success: function (data) {
                    // Remove the Context from the template
                    $("#display_context_"+id).remove()
                }
            });
        });
    }

    var add_skill = function() {
        var btn = $(this);

        btn.on("click", function () {

            var test_id = btn.attr("id");
            // Find the selected skill to add
            var skill_id = $("#skills_to_add option:selected").attr("id");

            $.ajax({
                url: '/professor/professor_test_add_skill/',
                data: {
                    'test_id': test_id,
                    'skill_id': skill_id,
                },
                dataType: 'json',
                success: function (data) {
                    // Refresh the page
                    location.reload();
                }
            });
        });
    }

    var delete_skill = function() {
        var btn = $(this);

        btn.on("click", function () {

            var id = btn.attr("id");

            $.ajax({
                url: '/professor/professor_test_delete_skill/',
                data: {
                    'id': id,
                },
                dataType: 'json',
                success: function (data) {
                    // Remove the skill title from the template
                    $("#display_skill_"+data.skill_id).remove();
                    // Remove the contexts linked to the skill deleted from the template
                    $(".skill-"+data.skill_id).remove();
                }
            });
        });
    }

    $(".modify").each(modify_name);
    $(".add-question").each(add_question);
    $(".delete-question").each(delete_question);
    $(".add-skill").each(add_skill);
    $(".delete-skill").each(delete_skill);
});
