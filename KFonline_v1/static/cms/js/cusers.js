$(function () {
    $('#save-user-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $('#user-dialog');
        var nameInput = $("input[name='username']");
        var passwordInput = $("input[name='password']");
        var emailInput = $("input[name='email']");

        var username = nameInput.val();
        var password = passwordInput.val();
        var email = emailInput.val();
        var submitType = self.attr('data-type');
        var userId = self.attr('data-id');

        if(!username||!password||!email){
            zlalert.alertInfoToast("请输入完整的数据");
            return;
        }
        var url = '';
        if (submitType == 'update'){
            url = '/cms/uuser/';
        }else {
            url = '/cms/auser/';
        }

        zlajax.post({
            "url":url,
            "data":{
                "username":username,
                "password":password,
                "email":email,
                "user_id":userId
            },
            'success':function (data) {
                dialog.modal('hide');
                if(data['code']==200){
                    window.location.reload()
                }else {
                    zlalert.alertInfo(data['message'])
                }
            },
            'fail':function () {
                zlalert.alertNetworkError();
            }
        })
    })
});



// $(function () {
//     $('.edit-user-btn').click(function () {
//         var self = $(this);
//         var tr = self.parent().parent();
//         var name = tr.attr('data-name');
//         var user_id = tr.attr('data-id');
//
//         zlalert.alertOneInput({
//             'text':'请输入新的用户名称！',
//             'placeholder':name,
//             'confirmCallback':function (inputValue) {
//                 zlajax.post({
//                     'url':'/cms/uuser/',
//                     'data':{
//                         'user_id':user_id,
//                         'name':inputValue,
//
//                     },
//                     'success':function (data) {
//                         if(data['code']==200){
//                             window.location.reload();
//                         }else{
//                             zlalert.alertInfo(data['message']);
//                         }
//                     }
//                 })
//             }
//         })
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
                    'url':'/cms/duser/',
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






