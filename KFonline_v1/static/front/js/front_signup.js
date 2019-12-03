$(function () {

    $("#captcha-img").click(function (event) {
        var self=$(this);
        var src=self.attr("src");
        var newsrc=zlparam.setParam(src,"xx",Math.random());
        self.attr("src",newsrc);
    });
});
$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephone_input=$("input[name='telephone']");
        // var sms_captcha_input=$("input[name=sms_captcha]");
        var username_input=$("input[name='username']");
        var password_input=$("input[name='password']");
        var password2_input=$("input[name='password2']");
        var captcha_input=$("input[name='graph_captcha']");

        var telephone = telephone_input.val();
        var username=username_input.val();
        var password=password_input.val();
        var password2=password2_input.val();
        var graph_captcha=captcha_input.val();

        zlajax.post({
            "url":"/signup/",
            "data":{
                "telephone":telephone,
                "username":username,
                "password":password,
                "password2":password2,
                "graph_captcha":graph_captcha
            },
            "success":function (data) {
                if(data['code']==200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        window.location = return_to;
                    }else{
                        window.location = '/';
                    }
                }else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function(){
                zlalert.alertNetworkError();
            }

        });

    });

});









