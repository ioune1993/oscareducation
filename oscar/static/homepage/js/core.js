$(function(){


  
      //$('.owl-carousel').slick();
      $('.blockquote').slick({

        adaptiveHeight:true,
        arrows : false,
        slidesToShow: 2,
        slidesToScroll: 2,
         dots: true,
         responsive: [
                {
                  breakpoint: 1024,
                  settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                  }
                },
                {
                  breakpoint: 600,
                  settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                  }
                },
                {
                  breakpoint: 480,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                  }
                }
             
              ]

      });
 



})