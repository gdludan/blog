function randomHexColor() { //随机生成十六进制颜色
    var hex = Math.floor(Math.random() * 16777216).toString(16); //生成ffffff以内16进制数
    while (hex.length < 6) { //while循环判断hex位数，少于6位前面加0凑够6位
    hex = '0' + hex;
    }
    return '#' + hex; //返回‘#'开头16进制颜色
}
function randomRgbaColor() { //随机生成RGBA颜色
 var r = Math.floor(Math.random() * 256); //随机生成256以内r值
 var g = Math.floor(Math.random() * 256); //随机生成256以内g值
 var b = Math.floor(Math.random() * 256); //随机生成256以内b值
 var alpha = Math.random(); //随机生成1以内a值
 return `rgb(${r},${g},${b},${alpha})`; //返回rgba(r,g,b,a)格式颜色
}
function randomRgbColor() { //随机生成RGB颜色
 var r = Math.floor(Math.random() * 256); //随机生成256以内r值
 var g = Math.floor(Math.random() * 256); //随机生成256以内g值
 var b = Math.floor(Math.random() * 256); //随机生成256以内b值
 return `rgb(${r},${g},${b})`; //返回rgb(r,g,b)格式颜色
}
var a_idx = 0;
jQuery(document).ready(function($) {
    $("html").click(function(e) {
        var a = new Array("富强", "民主", "文明", "和谐", "自由", "平等", "公正" ,"法治", "爱国", "敬业", "诚信", "友善");
        var $i = $("<span/>").text(a[a_idx]);
        a_idx = (a_idx + 1) % a.length;
        var x = e.pageX,
        y = e.pageY;
        var color =randomHexColor();
        var color2 = randomRgbaColor();
        var rcolor3 = randomRgbColor();
        $i.css({
            "z-index": 2147483647,
            "top": y - 20,
            "left": x,
            "position": "absolute",
            "font-weight": "bold",
            "color": rcolor3
        });
        $("body").append($i);
        $i.animate({
            "top": y - 180,
            "opacity": 0
        },
        1500,
        function() {
            $i.remove();
        });
    });
});
function onLoginError() {
    alert("你还没登录，不能对文章进行此操作。");
}
function goole_search(){
    window.open("https://www.google.com.hk/search?q="+searchbar.value, "_search");
}
function search_user(){
    window.open('/search/user?q='+document.getElementById("searchbar").value, "_self");
}
function search_post(){
    window.open('/search/post?q='+document.getElementById("searchbar").value, "_self");
}