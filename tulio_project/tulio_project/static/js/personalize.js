//=========================================
//Change cursor in right button textarea
//=========================================
$("textarea").mousemove(function(e) {
    var myPos = $(this).offset();
    myPos.bottom = $(this).offset().top + $(this).outerHeight();
    myPos.right = $(this).offset().left + $(this).outerWidth();
    
    if (myPos.bottom > e.pageY && e.pageY > myPos.bottom - 16 && myPos.right > e.pageX && e.pageX > myPos.right - 16) {
        $(this).css({ cursor: "nw-resize" });
    }
    else {
        $(this).css({ cursor: "" });
    }
})

//==============================
//Constant time Get comentarios
//==============================
var updateComment = setInterval(getComments,10000)

//========================
//Get comentarios
//========================
function getComments(){
	$.get("/getComments",function(data){
	listComments = JSON.parse(data)
	$("#commentsTable").html("")
	
	liveImages = $(".bigDraw")
	for(i=0;i<listComments.length;i++){
		img = liveImages[i]
		check = false

		for(j = 0; j < liveImages.length ; j++){
			if (listComments[i].imgid == liveImages[j].attributes.src.value){
				check = true
				break
			}
		}

		if(!check){
			$.get("/deleteComment",{id:listComments[i].id},function(data){
				if ("Comentário deletado" != data.message){
					alert("Houve um problema em deletar o comentário no servidor.")
					}
			})
		}

	}

	for (i = 0;i < listComments.length; i++){
		comment = listComments[i]
		name = comment.name
		imgid = comment.imgid
		id = comment.id
		comment = comment.comment
		
		//=========================
		//Check if img was deleted
		//=========================


		if ($("#logged").val() == "1"){
			$("#commentsTable").append("<tr>\
											<td style='width:40%;'>\
												<img src=" + imgid + " class='commentImg'/>\
											</td>\
												\
											<td style='width:20%; word-wrap:break-word;'>\
												<span class='nameComment' style='word-wrap:break-word'>" + name + ": </span>\
											</td>\
											<td style='width:38%; word-wrap:break-word;'>\
												<span class='commentComment' style='word-wrap:break-word'>" + comment + "</span>\
											</td>\
											<td style='width:2%'>\
												<input type='hidden' value='" + id + "''/>\
												<span class='deleteComment'>X</span>\
											</td>\
										</tr>")
			}
		else{
			$("#commentsTable").append("<tr>\
											<td style='width:40%;'>\
												<img src=" + imgid + " class='commentImg'/>\
											</td>\
												\
											<td style='width:20%; word-wrap:break-word;'>\
												<span class='nameComment' style='word-wrap:break-word'>" + name + ": </span>\
											</td>\
											<td style='width:40%; word-wrap:break-word;'>\
												<span class='commentComment' style='word-wrap:break-word'>" + comment + "</span>\
											</td>\
										</tr>")
		
		}

		}
	
		//========================
		//Delete comentarios
		//========================
		$(".deleteComment").click(function(){
			id = this.previousElementSibling.value
			actual = this
			$.get("/deleteComment",{id:id},function(data){
				if ("Comentário deletado" == data.message){
					$(actual.parentNode.parentNode).fadeOut()
					}
				else{
					alert("Houve um problema em deletar o comentário no servidor.")
				}
			})
		})

		//===============================
		//Remove SetInterval onMouseOver
		//===============================
		$("#commentsTable").mouseover(function(){
			clearInterval(updateComment)
		}).mouseout(function(){
			updateComment = setInterval(getComments,2000)
		});
	});
}

//===============================
//Arrow
//===============================
var isUp = true
	$("#downArrow").click(function(){
		if (isUp){
			actual =  $(".caixaComentario")
			actual.removeClass("caixaComentario")
			actual.addClass("caixaComentarioDown")
			$("#downArrowImg").attr("src","/static/images/upArrow.png")		
			isUp = false
		}
		else{
			actual =  $(".caixaComentarioDown")
			actual.removeClass("caixaComentarioDown")
			actual.addClass("caixaComentario")
			$("#downArrowImg").attr("src","/static/images/downArrow.png")		
			isUp = true
		}					
	});
//========================
	//Add comentarios
	//========================
	function addCommentHandler(actual){
				actual.unbind('click')
		  		actual.html("<form>\
		  		<span style=\"position:relative;top:-20%;padding: 5px;\">Nome:\
        		<input type=\"text\" name=\"nameComment\" style=\"float:right\" value=\"\"/>\<br\><br\>\
        		<span style=\"position:relative;top:-20%;padding: 5px;\">Comentário:\
        		<input type=\"text\" name=\"commentComment\" style=\"float:right\" value=\"\"/>\
        		<input id=\"addCommentButton\" type=\"submit\" class=\"\" style=\"opacity:0;\" name=\"addcomments.form\" value=\"Enviar\" />\
    	   		</form>")
    	   		$("#addCommentButton").click(function(){
    	   		event.preventDefault();
    	   		actual = this;
    	   		
    	   		while(actual.tagName.toLowerCase() != "a"){
					actual = actual.parentNode
				}

				img = $(actual).find("img")
			
				imgid = img.attr("alt")
        	   	name = document.getElementsByName("nameComment")[0].value
				comment = document.getElementsByName("commentComment")[0].value
    	   		$.get("/addComment",{name:name,comment:comment,imgid:imgid},function(data){
    	   			$(actual).find(".addComment").html(data.message)
    	   		})
    	   		
    	   		})
	}