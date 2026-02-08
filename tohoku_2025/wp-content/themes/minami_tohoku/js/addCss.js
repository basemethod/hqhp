/**********************************************************************

 - ヘッダー

**********************************************************************/
/* スクロール量でクラス */
$(window).scroll(function() {
  var scroll = $(this).scrollTop();
  var flnavH = $('#floating_nav').outerHeight(true) + 16;
  if(900 < scroll){
    if(!$('#floating_nav').hasClass('show')){
      $('#floating_nav').addClass('show').removeClass('hide');
      $('#floating_nav').css('top','0');
    }
  } else {
    if($('#floating_nav').hasClass('show')){
      $('#floating_nav').addClass('hide').removeClass('show');
      $('#floating_nav').css('top',flnavH * -1);
    }
  }
});

function header_matchmedia(){
  /* 1450px未満のヘッダー */
  if(window.matchMedia('(max-width:1449.9px)').matches){
    if($('header > div').hasClass('contain-1400')){
      $('header > div').addClass('responsible').removeClass('contain-1400').removeClass('wid-90pct').removeClass('flex');
    }
  } else {
    if($('header > div').hasClass('responsible')){
      $('header > div').addClass('contain-1400').addClass('wid-90pct').addClass('flex').removeClass('responsible');
    }
  }
}
$(window).resize(header_matchmedia);
$(window).on('load', header_matchmedia);

/**********************************************************************

 - スマホナビ

**********************************************************************/
$('.nav_btn').on('click', function(){
  if($(this).hasClass('open')){
    $(this).removeClass('open').addClass('close');
    $('#spNav').removeClass('open').addClass('close');
  } else {
    $(this).removeClass('close').addClass('open');
    $('#spNav').removeClass('close').addClass('open');
  }
});
$('#spNav a').on('click', function(){
  $('.nav_btn').removeClass('open').addClass('close');
  $('#spNav').removeClass('open').addClass('close');
});

/**********************************************************************

 - トップページ

**********************************************************************/
function index_matchmedia(){
  if(window.matchMedia('(max-width:1040px)').matches){
    if($('#news_block.index > div').hasClass('flex')){
      $('#news_block.index > div').addClass('responsible').removeClass('flex');
    }
    if($('#recruit_block.index > div > div').hasClass('flex')){
      $('#recruit_block.index > div > div').addClass('responsible').removeClass('flex');
    }
  } else {
    if($('#news_block.index > div').hasClass('responsible')){
      $('#news_block.index > div').addClass('flex').removeClass('responsible');
    }
    if($('#recruit_block.index > div > div').hasClass('responsible')){
      $('#recruit_block.index > div > div').addClass('flex').removeClass('responsible');
    }
  }
}
$(window).resize(index_matchmedia);
$(window).on('load', index_matchmedia);

/**********************************************************************

 - 固定ページ

**********************************************************************/
function page_matchmedia_1200(){
  if(window.matchMedia('(max-width:1200px)').matches){
    if($('.aboutus.first-block .text').hasClass('flex')){
      $('.aboutus.first-block .text').addClass('responsible').removeClass('flex');
    }
    if($('#main-article.recruit .recruit.first-block').hasClass('flex')){
      $('#main-article.recruit .recruit.first-block').addClass('responsible').removeClass('flex');
    }
  } else {
    if($('.aboutus.first-block .text').hasClass('responsible')){
      $('.aboutus.first-block .text').addClass('flex').removeClass('responsible');
    }
    if($('#main-article.recruit .recruit.first-block').hasClass('responsible')){
      $('#main-article.recruit .recruit.first-block').addClass('flex').removeClass('responsible');
    }
  }

  if(window.matchMedia('(max-width:960px)').matches){
      if($('#interviewList > li').hasClass('flex')){
        $('#interviewList > li').addClass('responsible').removeClass('flex');
      }
    } else {
      if($('#interviewList > li').hasClass('responsible')){
        $('#interviewList > li').addClass('flex').removeClass('responsible');
      }
    }

  if(window.matchMedia('(max-width:860px)').matches){
      if($('#worksList.archive li .cover').hasClass('flex')){
        $('#worksList.archive li .cover').addClass('responsible').removeClass('flex');
      }
    } else {
      if($('#worksList.archive li .cover').hasClass('responsible')){
        $('#worksList.archive li .cover').addClass('flex').removeClass('responsible');
      }
    }
}
$(window).resize(page_matchmedia_1200);
$(window).on('load', page_matchmedia_1200);

/**********************************************************************

 - お知らせ (シングルページ)

**********************************************************************/
function news_img_thumb(){
  var li_width = $('.selector li.small_img').width();
  var li_height = $('.selector li.small_img').height(li_width * 0.75);
}
$(window).resize(news_img_thumb);
$(window).on('load', news_img_thumb);

/* クリックアクション */
$('.single #main-article.news .selector ul li.small_img').on('click', function(){
  /* サムネイル */
  var list_num = $(this).index() + 1;
  var clicked = $('.single #main-article.news .selector ul li.small_img:nth-child(' + list_num + ') .cover');
  var un_clicked = $('.single #main-article.news .selector ul li.small_img:not(:nth-child(' + list_num + ')) .cover');

  if(clicked.hasClass('hide')){
    clicked.addClass('show').removeClass('hide');
    un_clicked.addClass('hide').removeClass('show');
  }

  /* large_image */
  var clicked_img = clicked.find('img').attr('src');
  $('.single #main-article.news .image_block .large_image img').attr('src', clicked_img);
});

/**********************************************************************

 - フッター

**********************************************************************/
function footer_matchmedia(){
  if(window.matchMedia('(max-width:800px)').matches){
    if($('.foot_block.bottom > div').hasClass('flex')){
      $('.foot_block.bottom > div').addClass('responsible').removeClass('flex');
    }
    if($('.foot_block.main > div').hasClass('flex')){
      $('.foot_block.main > div').addClass('responsible').removeClass('flex');
    }
  } else {
    if($('.foot_block.bottom > div').hasClass('responsible')){
      $('.foot_block.bottom > div').addClass('flex').removeClass('responsible');
    }
    if($('.foot_block.main > div').hasClass('responsible')){
      $('.foot_block.main > div').addClass('flex').removeClass('responsible');
    }
  }
}
$(window).resize(footer_matchmedia);
$(window).on('load', footer_matchmedia);
