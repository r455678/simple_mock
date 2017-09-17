var allData=[];
//获取项目名称
function projectNameList(){
	$.ajax({
		type:"get",
		url:myUrl+"/searchproject",
		async:true,
		dataType:"json",
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			var _data=res.data;
			var optionHtml="";
			for (var i=0;i<_data.length;i++) {
				optionHtml+='<option value='+_data[i]+'>'+_data[i]+'</option>'
			}
			$(".product-name").append(optionHtml);
		}
	})
}
//获取总数据  && 搜索
function getAllData(){
	var _self=$(event.target);
	var condition=$(".search-box input").val();
	var _project_name=$(".product-name option:selected").attr("value");
	var _url="/search";
	if(!condition && !_project_name){
		_url="/searchall";
	}
	$.ajax({
		type:"get",
		url:myUrl+_url,
		async:true,
		dataType:"json",
		data:{
			title:condition,
			project_name:_project_name
		},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			var _data=res.data;
			allData=_data;
			currentPage=$(".page-active a").text();
			dataShow(allData,1);
			$('#page').jqPaginator({
			    totalCounts: allData.length,
			    pageSize:10,
			    currentPage: 1,
				activeClass:"page-active",
				disableClass:"page-disabled",
			    first: '<li class="first"><a href="javascript:void(0);">首页</a></li>',
			    prev: '<li class="prev"><a href="javascript:void(0);">上一页</a></li>',
			    next: '<li class="next"><a href="javascript:void(0);">下一页</a></li>',
			    last: '<li class="last"><a href="javascript:void(0);">末页</a></li>',
			    page: '<li class="page"><a href="javascript:void(0);" currentPage={{page}}>{{page}}</a></li>',
			    onPageChange: function (num) {
			    	dataShow(allData,num);
			    }
			});
		}
	});
}

//数据解析
function dataShow(allData,currentPage){
	$("#msg-table tr:eq(0)").nextAll().remove();
	if(!currentPage){
		currentPage=1;
	}
	var trHTML="";
	for (var i=0;i<allData.length;i++) {
		var data_i=allData[i];
		if(i>=(currentPage-1)*10 && i<=(currentPage*10-1)){
			trHTML+='<tr class="tr-tit" id='+justObj(data_i.id)+'>'+
				'<td><i class="myckbox myckbox-normal" onclick="mycheckbox();"></i></td>'+
				'<td width="10%">'+justObj(data_i.id)+'</td>'+
				'<td width="10%" class="t-title">'+justObj(data_i.title)+'</td>'+
				'<td width="10%" class="t-methods">'+justObj(data_i.methods)+'</td>'+
				'<td width="15%" class="t-domain">'+justObj(data_i.domain)+'</td>'+
				'<td width="20%" class="describle">'+justObj(data_i.description)+'</td>'+
				'<td width="15%">'+justObj(data_i.updateTime)+'</td>'+
				'<td width="10%">'+
				'	<i class='+'"'+((data_i.status==0)? 'activation left on' : "activation off")+'"'+' onclick="activation();">'+
				'		<i class="activa-bar"></i>'+
				'	</i>'+
				'</td>'+
				'<td width="5%" class="no-padding">'+
				'	<i class="edit left mr5" onclick="edit();"></i>'+
				'	<i class="copy left" onclick="copyHandle();"></i>'+
				'</td>'+
			'</tr>'+
			'<tr class="hidden">'+
				'<td colspan="8">'+
					'<div class="tr-detail">'+
						'<div class="dt-cont">'+
							'<b>请求参数：</b><span class="dt-cont-s">'+justObj(data_i.reqparams)+'</span>'+
						'</div>'+
						'<div class="dt-cont">'+
							'<b>预期返回：</b><span class="dt-cont-y">'+justObj(data_i.resparams)+'</span>'+
						'</div>'+
					'</div>'+
				'</td>'+
			'</tr>';
		}
	}
	$("#msg-table").append(trHTML);
}
//判断对象是否存在
function justObj(obj){
	if(obj && typeof(obj)!="undefined"){
		return obj;
	}else{
		return "-";
	}
}
//checkbox
function mycheckbox(){
	var _self=$(event.target);	
	if(_self.hasClass("myckbox-normal")){
		_self.removeClass("myckbox-normal").addClass("myckbox-visited");
	}else{
		_self.removeClass("myckbox-visited").addClass("myckbox-normal");
	}
	
	var myckbox_all=_self.closest("#msg-table").find("td").find(".myckbox").length;
	var myckbox_vsed=_self.closest("#msg-table").find("td").find(".myckbox-visited").length;
	if(myckbox_vsed<myckbox_all){
		_self.closest("#msg-table").find("#selectAll").removeClass("myckbox-visited").addClass("myckbox-normal");
	}else{
		_self.closest("#msg-table").find("#selectAll").removeClass("myckbox-normal").addClass("myckbox-visited");
	}
}
//activation
function activation(){
	var _self=$(event.target);
	var _id=_self.closest("tr").attr("id");
	var current_status="";
	
	if(_self.hasClass("activa-bar")){
		_self=$(event.target).parent();
	}
	if(_self.hasClass("off")){
//		_self.removeClass("off").addClass("on");
		current_status=0;
	}else{
//		_self.removeClass("on").addClass("off");
		current_status=1;
	}
	$.ajax({
		type:"post",
		url:myUrl+"/manage",
		async:true,
		dataType:"json",
		data:{
			id:parseInt(_id),
			status:current_status
		},
		success:function(res){
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			getAllData();
		}
	});
}
//select all
function selectAll(parent){
	var _self=$(event.target);
	var _parent=_self.closest(parent);
	if(_self.hasClass("myckbox-normal")){
		_self.removeClass("myckbox-normal").addClass("myckbox-visited");
		_parent.find(".myckbox").removeClass("myckbox-normal").addClass("myckbox-visited");
	}else{
		_self.removeClass("myckbox-visited").addClass("myckbox-normal");
		_parent.find(".myckbox").removeClass("myckbox-visited").addClass("myckbox-normal");
	}
}//新增
function add(){
	var type=$(".sure").attr("data-type");
	var _id=$(".ctrl-pop").attr("current_id");
	if(type=="add"){
		var reqUrl=myUrl+"/addinfo";
	}else{
		var reqUrl=myUrl+"/editinfo";
	}
	$.ajax({
		type:"post",
		url:reqUrl,
		async:true,
		dataType:"json",
		data:{
			id:_id?_id:"",
			title:$(".r-title").val(),
			method:$(".r-method option:selected").text(),
			projectName:$(".source-object").val(),
			reqparams:$(".r-reqparams").val(),
			resparams:$(".r-resparams").val(),
			des:$(".r-des").val(),
			domain:$(".r-domain").val(),
			ischeck:$(".isJYrequst").hasClass("myckbox-visited") ? 1 : 0
		},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			getAllData();
			$(".ctrl-pop").addClass("hidden");
		}
	})
}
//删除
function del(){
	var ids=[];
	$(".msg-table tr").each(function(){
		if($(this).find(".myckbox").hasClass("myckbox-visited")){
			var _id=$(this).attr("id");
			ids.push(parseInt(_id));
		}
	})
	$.ajax({
		type:"post",
		url:myUrl+"/delinfo ",
		async:true,
		dataType:"json",
		data:{id:ids},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			alert("删除成功！");
			getAllData();
		}
	})
}
//编辑
function edit(){
	var current_id=$(event.target).closest("tr").attr("id");
	var currentTr=$("#msg-table tr[id="+current_id+"]");
	var _title=currentTr.find(".t-title").text();
	var _domain=currentTr.find(".t-domain").text();
	var _methods=currentTr.find(".t-methods").text();
	var _reqparams=currentTr.next().find(".dt-cont-s").text();
	var _resparams=currentTr.next().find(".dt-cont-y").text();
	var _des=currentTr.find(".describle").text();
	
	$(".ctrl-pop").attr("current_id",current_id);
	$(".ctrl-pop .pop-tit").text("+ 编辑");
	$(".ctrl-pop .r-title").val(_title=="-"?"":_title);
	$(".ctrl-pop .r-domain").val(_domain=="-"?"":_domain);
	$(".ctrl-pop .r-method .method-sed").prop("selected","selected").text(_methods=="-"?"":_methods);
	$(".ctrl-pop .r-reqparams").val(_reqparams=="-"?"":_reqparams);
	$(".ctrl-pop .r-resparams").val(_resparams=="-"?"":_resparams);
	$(".ctrl-pop .r-des").val(_des=="-"?"":_des);
}
//复制
function copyHandle(){
	var _id=$(event.target).closest("tr").attr("id");
	$.ajax({
		type:"post",
		url:myUrl+"/copy ",
		async:true,
		dataType:"json",
		data:{id:_id},
		success:function(res){			
			if(res.msg!="ok"){
				alert(res.remark);
				return;
			}
			alert("复制成功！");
			getAllData();
		}
	})
}





















