var myUrl="http://127.0.0.1:5202";

$(function(){
	getAllData();  //初始化页面数据
	projectNameList(); //获取项目名称list
	//add btn
	$("#add-btn").click(function(){
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
	


})
//jquery end


