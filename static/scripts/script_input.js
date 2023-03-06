	
function delayScrollAnime() {
	var time = 0.2;//遅延時間を増やす秒数の値
	var value = time;
	$('.delayScroll').each(function () {
		var parent = this;					//親要素を取得
		var elemPos = $(this).offset().top;//要素の位置まで来たら
		var scroll = $(window).scrollTop();//スクロール値を取得
		var windowHeight = $(window).height();//画面の高さを取得
		var childs = $(this).children();	//子要素を取得
		
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



window.addEventListener('DOMContentLoaded', function () {
	// input要素を取得
	var input_name = document.getElementById("input-url");
	// イベントリスナーでイベント「change」を登録
	input_name.addEventListener("change", function () {
		if (input_name.value.match(/https:\/\/www.youtube.com\/watch\?v=/)) {
			var video_id = input_name.value.substr(-11);
			var img = document.getElementById('youtube-img');
			img.setAttribute('src', "https://i.ytimg.com/vi/" + video_id + "/sddefault.jpg");
		}else {
			var img = document.getElementById('youtube-img');
			img.setAttribute('src', "");
		}
	});
	// イベントリスナーでイベント「input」を登録
	input_name.addEventListener("input", function () {
		if (input_name.value.match(/https:\/\/www.youtube.com\/watch\?v=/)) {
			var video_id = input_name.value.substr(-11);
			var img = document.getElementById('youtube-img');
			img.setAttribute('src', "https://i.ytimg.com/vi/" + video_id + "/sddefault.jpg");
		} else {
			var img = document.getElementById('youtube-img');
			img.setAttribute('src', "");
		}
	});

	var input_img = document.getElementById("file-select-input");
	// イベントリスナーでイベント「input」を登録
	input_img.addEventListener("input", function () {
		const file = input_img.files[0];
		const img = document.createElement('img');
		img.classList.add('preview-img');

		const reader = new FileReader();
		reader.onload = (event) => {
			img.src = event.target.result;
			updateHTMLCode();
		}
		reader.readAsDataURL(file);
		document.getElementById('previews').appendChild(img);
	});
});

function addParam() {
	const cricle = document.createElement('div');
	cricle.classList.add("spinner-border", "spinner-border-sm", "mr-1");
	cricle.setAttribute("id", "loading");
	cricle.setAttribute("role", "status");
	cricle.setAttribute("aria-hidden", "true");

	var btn = document.getElementById('post-btn')
	btn.insertBefore(cricle, btn.firstChild);

	var f = document.getElementById('form-info')

	var newValue = document.createElement('input');
	newValue.classList.add("hidden");
	newValue.name = "file_btn";
	var img_video_tab_classname = document.getElementById('img-video-tab').className;
	if (img_video_tab_classname.match(/active/)) {
		newValue.value = true;
	} else {
		newValue.value = false;
	}
	// フォームの要素に加えることで、submit時に追加したパラメータも送信される
	f.appendChild(newValue);

	var newValue = document.createElement('input');
	newValue.classList.add("hidden");
	newValue.name = "category";
	newValue.value = document.getElementById('input-category').value;
	f.appendChild(newValue);

	var newValue = document.createElement('input');
	newValue.classList.add("hidden");
	newValue.name = "youtube_url";
	newValue.value = document.getElementById('input-url').value;
	f.appendChild(newValue);
	f.submit();
}

// HTML コードの確認用
const updateHTMLCode = () => {
	const container = document.getElementById('my-container');
	document.getElementById('html-code').innerText = html_beautify(
		container.innerHTML, {
		indent_size: 2,
		end_with_newline: true,
		preserve_newlines: false,
		max_preserve_newlines: 0,
		wrap_line_length: 0,
		wrap_attributes_indent_size: 0,
		unformatted: ['b', 'em']
	}
	);
}
document.getElementById('file-select-input').addEventListener('change', (evt) => {
	previewAndInsert(evt.target.files[0]);
});

// 画像プレビューと input 追加
const previewAndInsert = (files) => {
	const file = files[0];
	const input = document.createElement('input');
	input.type = 'file';
	input.setAttribute("id","input-img-video")
	input.classList.add('hidden');
	if (files.length > 1 && typeof DataTransfer !== 'undefined') {
		const dt = new DataTransfer();
		dt.items.add(files[0]);
		input.files = dt.files;
	} else {
		input.files = files;
	}
	document.getElementById('previews').appendChild(input);

	const img = document.createElement('img');
	img.classList.add('preview-img');

	const reader = new FileReader();
	reader.onload = (event) => {
		img.src = event.target.result;
		updateHTMLCode();
	}
	reader.readAsDataURL(file);
	document.getElementById('previews').appendChild(img);
}

document.body.onload = () => {
	updateHTMLCode();
};

window.onload = function () {
	particlesJS('particles-js', {
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
					"src": "static/images/blue_triangle.png",
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
