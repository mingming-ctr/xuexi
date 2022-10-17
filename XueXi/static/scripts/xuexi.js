

$(document).ready(function () {

    // 缩略图预览
    //$imgs = document.querySelector('.weui-uploader__files')
    $imgs = $('.weui-uploader__files')
    console.log("tupian", $imgs)
    $imgs.click(function (e) {

        var target = e.target;

        while (!target.classList.contains('weui-uploader__file') && target) {
            target = target.parentNode;
        }
        if (!target) return;

        var url = target.getAttribute('style') || '';
        var id = target.getAttribute('data-id');

        if (url) {
            url = url.match(/url\((.*?)\)/)[1].replace(/"/g, '');
        }
        var gallery = weui.gallery(url, {
            className: 'custom-name',
            onDelete: function onDelete() {
                weui.confirm('确定删除该图片？', function () {
                    --uploadCount;
                    uploadCountDom.innerHTML = uploadCount;

                    for (var i = 0, len = uploadList.length; i < len; ++i) {
                        var file = uploadList[i];
                        if (file.id == id) {
                            file.stop();
                            break;
                        }
                    }
                    target.remove();
                    gallery.hide();
                });
            }
        });
    });

});


function upload(stepid, selectDay) {

    var uploadCount = 1;

    options = {
        url: '/imageprocess',
        auto: true,
        type: 'file',
        fileVal: 'fileVal',
        onBeforeSend: function (data, headers) {
            console.log(this, data, headers);
            debugger
            $.extend(data, { stepid: stepid, position: uploadCount, selectDay: selectDay });

            // $.extend(data, { test: 1 }); // 可以扩展此对象来控制上传参数
            // $.extend(headers, { Origin: 'http://127.0.0.1' }); // 可以扩展此对象来控制上传头部

            // return false; // 阻止文件上传
        },
    onSuccess: function (ret) {
        console.log(this, ret);
        uploadCount = uploadCount + 1
            // return true; // 阻止默认行为，不使用默认的成功态
        }
    }

    select = "#uploader" + stepid
    weui.uploader(select, options,);
}