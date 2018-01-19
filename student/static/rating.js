$('[name="rate"]').on('click', function() {
	var id = $(this).attr('id');
	var fields = $('[name="container"]');
	fields.html("");
	var field = $('[id="container'+id+'"]');
	field.html('<input type="radio" name="gender" value="male"> 1 star <input type="radio" name="gender" value="female"> 2 stars <input type="radio" name="gender" value="other"> 3 stars <input type="radio" name="gender" value="other"> 4 stars <input type="radio" name="gender" value="other"> 5 stars');
	field.append('<button type="submit"> Envoyer </button>');
});
