/*
Author: @oliviernt
*/
$(function(){
  $(".share-tw").click(function(){
    var $t = $(this),
        url = $t.attr("href"),
        title = $t.attr("title");
    url += "?text=Check out this pic I just uploaded: " + location.href;
    popup(url, title)
    return false;
  });
  $(".share-fb").click(function(){
    var $t = $(this),
        url = "http://www.facebook.com/sharer.php",
        title = $t.attr("title"),
        href = location.href.indexOf("localhost")!=-1 ? "http://www.pictur.me" : location.href;
    
    url += "?u=" + href;
    url += "&t=" + escape( "I just uploaded an image on picture.me");

    console.log(url);

    popup(url, title)
    return false;
  });
  $("form").bind("reset", function(){
      //return confirm("Are you sure?");
  });
  $("#loader").ready(function(){
      var $t = $("#loader");

      setInterval(function(){
        if ($t.text().length >= 3) {
            $t.text(".");
        }
        else {     
            $t.append(".");   
        }
    }, 1000);
  });
});

var popup = function(url, title) {
    return window.open(url, title, "height=250,width=550");
};