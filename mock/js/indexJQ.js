

$(function(){
	getAllData();  //初始化页面数据
	projectNameList(); //获取项目名称list
	$("#fileupload").attr("data-url",myUrl+'/import_excel');  //上传文件请求地址
	//add btn
	$("#add-btn").click(function(){
		$(".r-title").val("");
		$(".r-method option").removeProp("selected");
		$(".r-method .method-sed").prop("selected","selected");
		$(".r-reqparams").val("");
		$(".r-resparams").val("");
		$(".r-des").val("");
		$(".r-domain").val("");
		$(".r-reqparams").val("");
		$(".isJYrequst").removeClass("myckbox-visited").addClass("myckbox-normal");
		
		$(".ctrl-pop .pop-tit").text("+ 新增");
		$(".ctrl-pop").removeClass("hidden");
		$(".sure").attr("data-type","add");
	})
	//cancle btn
	$(".cancle").click(function(){
		$(".ctrl-pop").addClass("hidden");
	})
	
	//	edit btn
	$("#msg-table").on("click",".edit",function(){
		$(".ctrl-pop").removeClass("hidden");
		$(".sure").attr("data-type","edit");
	})
	//tr title
	$("#msg-table").on("click",".tr-tit",function(){
		var nextTr=$(this).next();
		if(nextTr.hasClass("hidden")){
			nextTr.removeClass("hidden");
			$(this).css("background","#fcf5f0");
		}else{
			nextTr.addClass("hidden");
			$(this).css("background","#fff");
		}
		return false;
	})
//	file up
	$('#fileupload').fileupload({
        add: function (e, data) {
            data.submit();
        },
        done: function (e, data) {
        	if(data._response.result.msg=="fail"){
        		alert(data._response.result.remark);
        		return;
        	}
            alert('上传成功！');
            getAllData();  //初始化页面数据
			projectNameList(); //获取项目名称list
        }
    });


})
//jquery end


