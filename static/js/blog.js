var blogLoadAllTemplate = function(content){
    var t = `<div class="blog-cell-all-content markdown-body">${ content }
             </div>
             <div class="right">
                <button class="blog-button-summary gua-hover">收起全文</button>
             </div>
             `
    return t
}

var commentTemplate = function(comment){
    var c = comment
    var t = `<div class="blog-comment-cell comment-hover clear-fix">
                        <div class="blog-comment-content left clear-fix">
                           ${ c.user_id }: ${ c.content }
                        </div>
                        <div class="blog-comment-time  right">
                            ${ c.created_time }
                        </div>
                    </div>`
    return t
}
$(document).ready(function(){
    var log = function(){
        console.log(arguments)
    }




    // markdown
    //var renderMarkDown = function () {
    //    marked.setOptions({
    //        renderer: new marked.Renderer(),
    //        gfm: true,
    //        tables: true,
    //        breaks: true,
    //        pedantic: true,
    //    });
    //
    //    $('.markdown-body').each(function () {
    //        var tag = $(this);
    //        var raw = tag.text();
    //        tag.html(marked(raw));
    //    });
    //
    //    $('pre > code').each(function () {
    //        var tag = $(this);
    //        var attr = tag.attr('class');
    //        var code = tag.text();
    //        var options = {
    //            value: code,
    //            lineNumbers: true,
    //            readOnly: true,
    //            theme: 'material',
    //        };
    //
    //        if (attr != undefined) {
    //            var language = attr.split('-')[1];
    //            options['mode'] = language;
    //        } else {
    //            options['mode'] = '';
    //        }
    //
    //        tag.empty();
    //        var editor = CodeMirror(this, options);
    //        editor.setSize("100%", "100%");
    //    });
    //};


    // 评论计数
    //$('.blog-cell').each(function(){
    //    var comments = $(this).find('.blog-comment-cell').length
    //    var counterDiv = $(this).find('.blog-comment-a')
    //    counterDiv.text(comments)
    //})

    // 展开评论
    $('.blog-comment-a').on('click', function(){
        var div = $(this).closest('.blog-cell')
        var commentDiv = div.find('#blog-comment-id')
        //log(commentDiv.attr('class'), 'class')
        commentDiv.slideToggle()
    })

    $('.blog-button-add').on('click', function(){
        var title = $('.blog-input-title').val()
        var summary = $('.blog-textarea-summary').val()
        var sort = $('.blog-input-sort:checked').val()
        var content = $('.blog-textarea-content').val()
        var blog = {
            title: title,
            summary: summary,
            sort: sort,
            content: content,
        }
        var response = function(r){
            if(r.success) {
                alertify.success(r.message)
                window.location.href = '/blog/' + r.data.user_id
            }else {
                alertify.error(r.message)
            }
        }
        api.blogAdd(blog, response)
    })

    // 加载全文
    $('.blog-button-content').on('click', function(){
        var button = $(this)
        var cell = $(this).closest('.blog-cell')
        var blogId = cell.data('id')
        var div = cell.find('.blog-cell-summary')
        var form = {
            id: blogId
        }
        var response = function(r){
            if(r.success) {
                var content = r.data
                div.parent().prepend(blogLoadAllTemplate(content))
                div.hide()
                button.hide()
            }else {
                alertify.error(r.message)
            }
        }
        var contentDiv = cell.find('.blog-cell-all-content')
        if (contentDiv.length>0) {
            div.hide()
            button.hide()
            cell.find('.blog-cell-all-content').slideDown('slow')
            //cell.find('.blog-cell-all-content').show('slow')
            cell.find('.blog-button-summary').show()
        }else {
            api.contentAll(form, response)
        }
    })
    // 收起全文
    $('.blog-cell-content').on('click', '.blog-button-summary', function(){
        var div = $(this).closest('.blog-cell-content')

        //div.find('.blog-cell-all-content').hide('slow')
        div.find('.blog-cell-summary').show()
        div.find('.blog-button-content').show()
        div.find('.blog-cell-all-content').slideUp('slow')
        $(this).hide()
    })

    // 添加评论
    $('.blog-comment-button').on('click', function(){
        var div = $(this).closest('.blog-cell')
        var blog_id = div.data('id')
        var inputDiv = div.find('.blog-comment-input')
        var insertDiv = div.find('.blog-comment-h2')
        var content = inputDiv.val()
        var form = {
            blog_id: blog_id,
            content: content,
        }
        var response = function(r){
            if(r.success == 302) {
                alertify.success(r.message)
                window.location.href = '/'
            }else if(r.success == true) {
                alertify.success(r.message)
                var comment = r.data
                insertDiv.after(commentTemplate(comment))
                inputDiv.val('')
            }else {
                alertify.error(r.message)
            }
        }
        api.commentAdd(form, response)
    })

    // 更新blog
    $('.blog-button-update').on('click', function(){
        var title = $('.blog-input-title').val()
        var summary = $('.blog-textarea-summary').val()
        var sort = $('.blog-input-sort:checked').val()
        var content = $('.blog-textarea-content').val()
        var id = $('.blog-update-id').val()
        var url = '/api/blog/update/' + id
        var blog = {
            title: title,
            summary: summary,
            sort: sort,
            content: content,
        }
        var response = function(r){
            if(r.success) {
                window.location.href = '/blog/' + r.data.user_id
                alertify.success(r.message)
            }else {
                alertify.error(r.message)
            }
        }
        api.blogUpdate(url, blog, response)
    })

    // 删除blog
    $('.blog-button-delete').on('click', function(){
        var cell = $(this).closest('.blog-cell')
        var id = cell.data('id')
        var url = '/api/blog/delete/' + id
        var response = function(r){
            if(r.success) {
                alertify.success(r.message)
                cell.slideUp()
            }else {
                alertify.error(r.message)
            }
        }
        api.blogDelete(url, response)
    })


    //renderMarkDown()

})

