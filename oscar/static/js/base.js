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

var app = angular.module('oscar', ['ngCookies'])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{&');
        $interpolateProvider.endSymbol('&}');
    })
    .run(function($http, $cookies){
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    })

$('.menu-tabs a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})
