$(function () {
    $('#save-user-btn').click(function (event) {

        event.preventDefault();
        var self = $(this);
        var dialog = $('#user-dialog');
        var telephoneInput = $("input[name='telephone']");
        var usernameInput = $("input[name='username']");
        var passwordInput = $("input[name='password']");

        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var password = passwordInput.val();
        var submitType = self.attr('data-type');
        var userId = self.attr('data-id');

        if(!telephone||!username||!password){
            zlalert.alertInfoToast("请输入完整的数据");
            return;
        }
        var url = "";
        if(submitType == 'update'){
            url = '/cms/ufuser/';
        }else{
            url='/cms/afuser/';
        }
        zlajax.post({
            "url":url,
            "data":{
                "telephone":telephone,
                "username":username,
                "password":password,
                "user_id":userId,
            },
            'success':function (data) {
                dialog.modal('hide');
                if(data['code']==200){
                    window.location.reload()
                }else{
                    zlalert.alertInfo(data['message'])
                }
            },
            'fail':function () {
                zlalert.alertNetworkError();
            }
        })
    });
});

// $(function () {
//     $('.edit-user-btn').click(function () {
//         var self = $(this);
//         var dialog = $('#user-dialog');
//         dialog.modal('show');
//
//         var tr = self.parent().parent();
//         var telephone = tr.attr('data-telephone');
//         var username = tr.attr('data-name');
//         var password = tr.attr('data-pwd');
//         var userId = tr.attr('data-id');
//
//         var telephoneInput = dialog.find("input[name='telephone']");
//         var usernameInput = dialog.find("input[name='username']");
//         var passwordInput = dialog.find("input[name='password']");
//         var saveBtn = dialog.find('#save-user-btn');
//
//         telephoneInput.val(telephone);
//         usernameInput.val(username);
//         passwordInput.val(password);
//         saveBtn.attr('data-type', 'update');
//
//         saveBtn.attr('data-id',userId);
//
//
//         // zlalert.alertOneInput({
//         //     'text':'请输入新的用户名称！',
//         //     'placeholder':name,
//         //     'confirmCallback':function (inputValue) {
//         //         zlajax.post({
//         //             'url':'/cms/ufuser/',
//         //             'data':{
//         //                 'user_id':user_id,
//         //                 'name':inputValue
//         //             },
//         //             'success':function (data) {
//         //                 if(data['code']==200){
//         //                     window.location.reload();
//         //                 }else{
//         //                     zlalert.alertInfo(data['message']);
//         //                 }
//         //             }
//         //         })
//         //     }
//         // })
//
//     })
// });

$(function () {
    $('.delete-user-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg": "您确定要删这个用户吗？",
            "confirmCallback":function () {
                zlajax.post({
                    'url':'/cms/dfuser/',
                    'data':{
                        'user_id':user_id
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            window.location.reload();
                        }else {
                            zlalert.alertInfo(data['mssage'])
                        }
                    }
                })
            }
        })
    })
});