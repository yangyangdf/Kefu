$(function () {
    var ue = UE.getEditor('editor', {
        'serverUrl': '/ueditor/upload',
        'toolbars': [[
            'nudo',
            'redo',
            'bold',
            'italie',
            'source',
            'blockqueote',
            'selectall',
            'insertcode',
            'fontfamily',
            'simpleupload',
            'emotion'
        ]]
    });
    window.ue = ue
});

$(function () {
    $('#comment-btn').click(function (event) {
        event.preventDefault();
        var loginTag = $('#login-tag').attr('data-is-login');
        if(!loginTag){
            window.location = '/signin/';
        }else{
            var content = window.ue.getContent();
            var post_id = $('#post-content').attr('data-id');
            zlajax.post({
                'url':'/acomment/',
                'data':{
                    'content':content,
                    'post_id':post_id
                },
                'success':function (data) {
                    if(data['code']==200){
                        window.location.reload();
                    }else {
                        zlalert.alertInfo(data['message']);
                    }
                }
            })
        }
    })
});


