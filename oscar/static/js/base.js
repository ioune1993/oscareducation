$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

var app = angular.module('oscar', ['ngCookies', 'textAngular'])
    .config(function($interpolateProvider, $provide) {
        $interpolateProvider.startSymbol('{&');
        $interpolateProvider.endSymbol('&}');

        $provide.decorator('taOptions', ['taRegisterTool', '$delegate', function(taRegisterTool, taOptions) {
            taOptions.toolbar = [
                ['h5', 'p', 'pre', 'quote'],
                ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
                ['justifyLeft', 'justifyCenter', 'justifyRight', 'indent', 'outdent'],
                ['html', 'insertLink']
            ];

            return taOptions;
        }]);

    })
    .run(function($http, $cookies){
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    })

$('.menu-tabs a').not(".real-link").click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
