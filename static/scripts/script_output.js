
function delayScrollAnime() {
    var time = 0.2;//遅延時間を増やす秒数の値
    var value = time;
    $('.delayScroll').each(function () {
        var parent = this;//親要素を取得
        var elemPos = $(this).offset().top;//要素の位置まで来たら
        var scroll = $(window).scrollTop();//スクロール値を取得
        var windowHeight = $(window).height();//画面の高さを取得
        var childs = $(this).children();    //子要素を取得
        
        if (scroll >= elemPos - windowHeight && !$(parent).hasClass("play")) {//指定領域内にスクロールが入ったらまた親要素にクラスplayがなければ
            $(childs).each(function () {
                
                if (!$(this).hasClass("fadeUp")) {//アニメーションのクラス名が指定されているかどうかをチェック
                    
                    $(parent).addClass("play"); //親要素にクラス名playを追加
                    $(this).css("animation-delay", value + "s");//アニメーション遅延のCSS animation-delayを追加し
                    $(this).addClass("fadeUp");//アニメーションのクラス名を追加
                    value = value + time;//delay時間を増加させる
                    
                    //全ての処理を終わったらplayを外す
                    var index = $(childs).index(this);
                    if((childs.length-1) == index){
                        $(parent).removeClass("play");
                    }
                }
            })
        }else {
            $(childs).removeClass("fadeUp");//アニメーションのクラス名を削除
            value = time;//delay初期値の数値に戻す
        }
    })
}

// 画面をスクロールをしたら動かしたい場合の記述
    $(window).scroll(function (){
        delayScrollAnime();/* アニメーション用の関数を呼ぶ*/
    });// ここまで画面をスクロールをしたら動かしたい場合の記述

// 画面が読み込まれたらすぐに動かしたい場合の記述
    $(window).on('load', function(){
        delayScrollAnime();/* アニメーション用の関数を呼ぶ*/
    });// ここまで画面が読み込まれたらすぐに動かしたい場合の記述


// 動きのきっかけの起点となるアニメーションの名前を定義
function BgFadeAnime(){

    // 背景色が伸びて出現（左から右）
  $('.bgLRextendTrigger').each(function(){ //bgLRextendTriggerというクラス名が
    var elemPos = $(this).offset().top-50;//要素より、50px上の
    var scroll = $(window).scrollTop();
    var windowHeight = $(window).height();
    if (scroll >= elemPos - windowHeight){
        $(this).addClass('bgLRextend');// 画面内に入ったらbgLRextendというクラス名を追記
    }else{
        $(this).removeClass('bgLRextend');// 画面外に出たらbgLRextendというクラス名を外す
    }
}); 

   // 文字列を囲う子要素
  $('.bgappearTrigger').each(function(){ //bgappearTriggerというクラス名が
    var elemPos = $(this).offset().top-50;//要素より、50px上の
    var scroll = $(window).scrollTop();
    var windowHeight = $(window).height();
    if (scroll >= elemPos - windowHeight){
        $(this).addClass('bgappear');// 画面内に入ったらbgappearというクラス名を追記
    }else{
        $(this).removeClass('bgappear');// 画面外に出たらbgappearというクラス名を外す
    }
});
}

// 画面をスクロールをしたら動かしたい場合の記述
$(window).scroll(function (){
    BgFadeAnime();/* アニメーション用の関数を呼ぶ*/
});// ここまで画面をスクロールをしたら動かしたい場合の記述

// 画面が読み込まれたらすぐに動かしたい場合の記述
$(window).on('load', function(){
    BgFadeAnime();/* アニメーション用の関数を呼ぶ*/
});// ここまで画面が読み込まれたらすぐに動かしたい場合の記述


window.onload = function() {
  particlesJS('particles-js',{
   "particles": {
     "number": {
       "value": 30,
       "density": {
         "enable": false,
         "value_area": 50
       }
     },
     "color": {
       "value": "#fff"
     },
     "shape": {
       "type": "image",
       "stroke": {
         "width": 0,
         "color": "#ffffff"
       },
       "polygon": {
         "nb_sides": 5
       },
       "image": {
         "src": "/static/images/blue_triangle.png",
         "width": 100,
         "height": 100
       }
     },
     "opacity": {
       "value": 0.8,
       "random": true,
       "anim": {
         "enable": false,
         "speed": 1,
         "opacity_min": 0.1,
         "sync": false
       }
     },
     "size": {
       "value": 50,
       "random": false,
       "anim": {
         "enable": false,
         "speed": 5,
         "size_min": 10,
         "sync": false
       }
     },
     "rotate": {
       "value": 360,
       "random": true,
       "anim": {
         "enable": true,
         "speed": -10
       }
     },
     "line_linked": {
       "enable": false,
       "distance": 500,
       "color": "#ffffff",
       "opacity": 0.4,
       "width": 2
     },
     "move": {
       "enable": true,
       "speed": 5,
       "direction": "bottom",
       "random": true,
       "straight": false,
       "out_mode": "out",
       "bounce": false,
       "attract": {
         "enable": false,
         "rotateX": 6234,
         "rotateY": 6155
       }
     }
   },
   "interactivity": {
     "detect_on": "canvas",
     "events": {
       "onhover": {
         "enable": false,
         "mode": "repulse"
       },
       "onclick": {
         "enable": true,
         "mode": "push"
       },
       "resize": true
     },
     "modes": {
       "grab": {
         "distance": 400,
         "line_linked": {
           "opacity": 0.5
         }
       },
       "bubble": {
         "distance": 400,
         "size": 4,
         "duration": 0.3,
         "opacity": 1,
         "speed": 3
       },
       "repulse": {
         "distance": 200,
         "duration": 0.4
       },
       "push": {
         "particles_nb": 4
       },
       "remove": {
         "particles_nb": 2
       }
     }
   },
   "retina_detect": true
 });
};

//box1の指定
$('#box1').on('inview', function(event, isInView) {
	if (isInView) {
		//要素が見えたときに実行する処理
		$("#box1 .count-up").each(function(){
			$(this).prop('Counter',0).animate({//0からカウントアップ
		        Counter: $(this).text()
		    }, {
				// スピードやアニメーションの設定
		        duration: 2000,//数字が大きいほど変化のスピードが遅くなる。2000=2秒
		        easing: 'swing',//動きの種類。他にもlinearなど設定可能
		        step: function (now) {
		            $(this).text(Math.ceil(now));
		        }
		    });
		});
	}
});