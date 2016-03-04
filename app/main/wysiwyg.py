# -*- coding:utf-8 -*-
# can't use now
from flask import render_template
from wtforms.widgets.core import HTMLString, html_params, escape
from wtforms import StringField,TextField,Field
from wtforms.compat import text_type, string_types, iteritems


class WysiwygWidget(object):

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = u''
        html += u'<div class=\"btn-toolbar m-b-sm btn-editor\" data-role=\"editor-toolbar\"data-target=\"#editor\">' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm dropdown-toggle\" data-toggle=\"dropdown\" title=\"Font\"><i class=\"icon-font\"> </i><b class=\"caret\"></b></a>' \
                            u'<ul class=\"dropdown-menu\">' \
                            u'</ul>' \
                    u'</div>' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm dropdown-toggle\" data-toggle=\"dropdown\" title=\"Font Size\"><i class=\"icon-text-height\"></i>&nbsp;<b class=\"caret\"></b></a>' \
                            u'<ul class=\"dropdown-menu\">' \
                            u'<li><a data-edit=\"fontSize 5\"><font size=\"5\">大号</font></a></li>' \
                            u'<li><a data-edit=\"fontSize 3\"><font size=\"3\">正常</font></a></li>' \
                            u'<li><a data-edit=\"fontSize 1\"><font size=\"1\">小号</font></a></li>' \
                            u'</ul>' \
                    u'</div>' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"bold\" title=\"加粗 (Ctrl/Cmd+B)\"><i class=\"icon-bold\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"italic\" title=\"倾斜 (Ctrl/Cmd+I)\"><i class=\"icon-italic\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"strikethrough\" title=\"删除线\"><i class=\"icon-strikethrough\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"underline\" title=\"下划线 (Ctrl/Cmd+U)\"><i class=\"icon-underline\"></i></a>' \
                    u'</div>' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"insertunorderedlist\" title=\"无序列表\"><i class=\"icon-list-ul\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"insertorderedlist\" title=\"有序列表\"><i class=\"icon-list-ol\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"outdent\" title=\"减少缩进 (Shift+Tab)\"><i class=\"icon-indent-left\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"indent\" title=\"增加缩进 (Tab)\"><i class=\"icon-indent-right\"></i></a>' \
                    u'</div>' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"justifyleft\" title=\"左对齐 (Ctrl/Cmd+L)\"><i class=\"icon-align-left\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"justifycenter\" title=\"居中 (Ctrl/Cmd+E)\"><i class=\"icon-align-center\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"justifyright\" title=\"右对齐 (Ctrl/Cmd+R)\"><i class=\"icon-align-right\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"justifyfull\" title=\"整理 (Ctrl/Cmd+J)\"><i class=\"icon-align-justify\"></i></a>' \
                    u'</div>' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm dropdown-toggle\" data-toggle=\"dropdown\" title=\"超链接\"><i class=\"icon-link\"></i></a>' \
                            u'<div class=\"dropdown-menu\"><div class=\"input-group m-l-xs m-r-xs\">' \
                                u'<input class=\"form-control input-sm\" placeholder=\"URL\" type=\"text\" data-edit=\"createLink\"  />' \
                                u'<div class=\"input-group-btn\"><button class=\"btn btn-default btn-sm\" type=\"button\">加入</button>' \
                                u'</div>' \
                            u'</div>' \
                    u'</div>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"unlink\" title=\"取消链接\"><i class=\"icon-cut\"></i></a>' \
                    u'</div>' \
                    u'<div class=\"btn-group hide\">' \
                        u'<a class=\"btn btn-default btn-sm\" title=\"插入图片\" id=\"pictureBtn\"><i class=\"icon-picture\"></i></a>' \
                        u'<input type=\"file\" data-role=\"magic-overlay\" data-target=\"#pictureBtn\"  data-edit=\"insertImage\" />' \
                    u'</div>' \
                    u'<div class=\"btn-group\">' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"undo\" title=\"撤销 (Ctrl/Cmd+Z)\"><i class=\"icon-undo\"></i></a>' \
                        u'<a class=\"btn btn-default btn-sm\" data-edit=\"redo\" title=\"前进 (Ctrl/Cmd+Y)\"><i class=\"icon-repeat\"></i></a>' \
                        u'<input type="text" data-edit="inserttext" id="语音输入" x-webkit-speech="">' \
                    u'</div></div>'
        html += u'<textarea class=\"hide flask-wysiwyg\"  data-editor=\"editor\" %s>%s</textarea>'
        html += u'<div id=\"editor\" style=\"overflow:scroll;height:150px;max-height:150px\"  class="bootstrap-wysiwyg form-control" >%s</div>'

        # html=''
        # html+='<div class=\"btn-toolbar m-b-sm btn-editor\" data-role=\"editor-toolbar\"data-target=\"#editor\"><div class=\"btn-group\"><a class=\"btn btn-default btn-sm dropdown-toggle\" data-toggle=\"dropdown\"        title=\"Font\"><i class=\"icon-font\"></i><b class=\"caret\"></b></a><ul class=\"dropdown-menu\"></ul></div><div class=\"btn-group\"><a class=\"btn btn-default btn-sm dropdown-toggle\" data-toggle=\"dropdown\"        title=\"Font Size\"><i class=\"icon-text-height\"></i>            &nbsp;<b class=\"caret\"></b></a><ul class=\"dropdown-menu\"><li><a data-edit=\"fontSize 5\"><font size=\"5\">                        Huge</font></a></li><li><a data-edit=\"fontSize 3\"><font size=\"3\">                        Normal</font></a></li><li><a data-edit=\"fontSize 1\"><font size=\"1\">                        Small</font></a></li></ul></div><div class=\"btn-group\"><a class=\"btn btn-default btn-sm\" data-edit=\"bold\" title=\"Bold (Ctrl/Cmd+B)\"><i class=\"icon-bold\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"italic\" title=\"Italic (Ctrl/Cmd+I)\"><i class=\"icon-italic\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"strikethrough\" title=\"Strikethrough\"><i class=\"icon-strikethrough\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"underline\" title=\"Underline (Ctrl/Cmd+U)\"><i class=\"icon-underline\"></i></a></div><div class=\"btn-group\"><a class=\"btn btn-default btn-sm\" data-edit=\"insertunorderedlist\" title=\"Bullet list\"><i class=\"icon-list-ul\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"insertorderedlist\" title=\"Number list\"><i class=\"icon-list-ol\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"outdent\" title=\"Reduce indent (Shift+Tab)\"><i class=\"icon-dedent\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"indent\" title=\"Indent (Tab)\"><i class=\"icon-indent\"></i></a></div><div class=\"btn-group\"><a class=\"btn btn-default btn-sm\" data-edit=\"justifyleft\" title=\"Align Left (Ctrl/Cmd+L)\"><i class=\"icon-align-left\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"justifycenter\" title=\"Center (Ctrl/Cmd+E)\"><i class=\"icon-align-center\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"justifyright\" title=\"Align Right (Ctrl/Cmd+R)\"><i class=\"icon-align-right\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"justifyfull\" title=\"Justify (Ctrl/Cmd+J)\"><i class=\"icon-align-justify\"></i></a></div><div class=\"btn-group\"><a class=\"btn btn-default btn-sm dropdown-toggle\" data-toggle=\"dropdown\"        title=\"Hyperlink\"><i class=\"icon-link\"></i></a><div class=\"dropdown-menu\"><div class=\"input-group m-l-xs m-r-xs\"><input class=\"form-control input-sm\" placeholder=\"URL\" type=\"text\" data-edit=\"createLink\"                /><div class=\"input-group-btn\"><button class=\"btn btn-default btn-sm\" type=\"button\">                        Add</button></div></div></div><a class=\"btn btn-default btn-sm\" data-edit=\"unlink\" title=\"Remove Hyperlink\"><i class=\"icon-cut\"></i></a></div><div class=\"btn-group hide\"><a class=\"btn btn-default btn-sm\" title=\"Insert picture (or just drag & drop)\"        id=\"pictureBtn\"><i class=\"icon-picture-o\"></i></a><input type=\"file\" data-role=\"magic-overlay\" data-target=\"#pictureBtn\"        data-edit=\"insertImage\" /></div><div class=\"btn-group\"><a class=\"btn btn-default btn-sm\" data-edit=\"undo\" title=\"Undo (Ctrl/Cmd+Z)\"><i class=\"icon-undo\"></i></a><a class=\"btn btn-default btn-sm\" data-edit=\"redo\" title=\"Redo (Ctrl/Cmd+Y)\"><i class=\"icon-repeat\"></i></a></div></div>'
        # html+='<textarea class=\"hide flask-wysiwyg\"   data-editor=\"editor\" %s>%s</textarea>'
        # html+='<div id=\"editor\"   style=\"overflow:scroll;height:150px;max-height:150px\"  class="bootstrap-wysiwyg form-control" >%s</div>'
        #

        return HTMLString(html %
                          (html_params(name=field.name, **kwargs),
                           escape(text_type(field._value())),
                           escape(text_type(field._value()))))


class WysiwygField(TextField):
    widget = WysiwygWidget()
