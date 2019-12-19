const googlehome = require('google-home-notifier')
const language = 'ja';

//ここにGoogleフォームのipアドレスを記入
googlehome.ip('', language);

//Googleフォームに喋ってもらいたい内容を記入
var voice_list = ["怒らないでください","ドンマイです","嫌な顔しないでください","今のは怖かったですね","楽しいですね","悲しいですか","驚きましたね"];

for(var i = 0;i < process.argv.length; i++){
  console.log("argv[" + i + "] = " + process.argv[i]);
}

//console.log(voice_list[process.argv[2]]);

if (process.argv[2]==4 && Math.random()<0.3){
  googlehome.notify(voice_list[process.argv[2]]);
} else if(process.argv[2]!=4 ) {
  googlehome.notify(voice_list[process.argv[2]]);
}
