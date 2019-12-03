$(function () {
   $('#save-role-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       var dialog = $('#roles-dialog');
       var emailInput = $("input[name='email']");
       var roleInput = $("input[name='role']");

       var email = emailInput.val();
       var role = roleInput.val();
       var submitType = self.attr('data-type');
       var userId = self.attr('data-id');

       if (!email||!role){
           zlalert.alertInfoToast("请输入完整的数据");
           return;
       }
       var url = '';
       if(submitType == 'update'){
           url = '/cms/uroles/';
       }else {
           url = '/cms/aroles/'
       }

       zlajax.post({
           "url":url,
           "data":{
               "email":email,
               "role":role
           },
           "success":function (data) {
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

   })
});




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
                    'url':'/cms/droles/',
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