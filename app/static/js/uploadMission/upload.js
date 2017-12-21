$("#uploadfile").fileinput({
    uploadUrl: "/upload", //上传的地址
    allowedFileExtensions: ['pcap'],//接收的文件后缀
    // //uploadExtraData:{"id": 1, "fileName":'123.mp3'},
    //uploadAsync: true, //默认异步上传
    showUpload: true, //是否显示上传按钮
    showRemove : true, //显示移除按钮
    showPreview : false, //是否显示预览
    showCaption: true,//是否显示标题
    browseClass: "btn btn-primary", //按钮样式     
    dropZoneEnabled: false,//是否显示拖拽区域
    maxFileSize: 0,//单位为kb，如果为0表示不限制文件大小
    minFileCount: 0,
    maxFileCount: 1, //表示允许同时上传的最大文件个数
    enctype: 'multipart/form-data', 
    validateInitialCount:true,
    previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
    msgFilesTooMany: "选择上传的文件数量({n}) 超过允许的最大数值{m}！"
});


//异步上传返回结果处理
$("#uploadfile").on("fileuploaded", function (event, data, previewId, index) {
    // console.log(data.id);
    // console.log(data.index);
    // console.log(data.file);
    // console.log(data.reader);
    // console.log(data.files);
    // var obj = data.response;
    // alert(JSON.stringify(data.success));

});

//同步上传错误处理
$('#uploadfile').on('filebatchuploaderror', function(event, data, msg) {
    // console.log(data.id);
    // console.log(data.index);
    // console.log(data.file);
    // console.log(data.reader);
    // console.log(data.files);
    // // get message
    // alert(msg);

});

//同步上传返回结果处理
$("#uploadfile").on("filebatchuploadsuccess", function (event, data, previewId, index) {
    // console.log(data.id);
    // console.log(data.index);
    // console.log(data.file);
    // console.log(data.reader);
    // console.log(data.files);
    // var obj = data.response;
    // alert(JSON.stringify(data.success));
 
});

//上传前
$('#uploadfile').on('filepreupload', function(event, data, previewId, index) {
    // var form = data.form, files = data.files, extra = data.extra,
    // response = data.response, reader = data.reader;
    // console.log('File pre upload triggered');

});
