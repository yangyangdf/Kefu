$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var oldpwdE=$("input[name='oldpwd']");
        var newpwdE=$("input[name='newpwd']");
        var newpwd2E=$("input[name='newpwd2']");

        var oldpwd=oldpwdE.val();
        var newpwd=newpwdE.val();
        var newpwd2=newpwd2E.val();

        zlajax.post({
            "url":"/cms/resetpwd/",
            'data':{
                "oldpwd":oldpwd,
                "newpwd":newpwd,
                "newpwd2":newpwd2,
            },
            "success":function (data) {
                if(data["code"]==200){
                    zlalert.alertSuccessToast("恭喜你,密码修改成功");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }
                else{
                    zlalert.alertInfo(data["message"]);
                }
            },
            "fail":function (data) {
                zlalert.alertNetworkError();
            }
        });
    });
});