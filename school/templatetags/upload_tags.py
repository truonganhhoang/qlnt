# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.simple_tag
def upload_js():
    return """
    <script id="template-upload" type="text/x-jquery-tmpl">
        <tr class="template-upload{{if error}} ui-state-error{{/if}}">
            <td class="preview"></td>
            <td class="name">${name}</td>
            <td class="size">${sizef}</td>
            {{if error}}
                <td class="error" colspan="2">Lỗi:
                    {{if error === 'maxFileSize'}}File đã chọn quá lớn
                    {{else error === 'minFileSize'}}File đã chọn quá nhỏ
                    {{else error === 'acceptFileTypes'}}File đã chọn không phải file Excel
                    {{else error === 'maxNumberOfFiles'}}Số file tải lên vượt quá giới hạn
                    {{else}}${error}
                    {{/if}}
                </td>
            {{else}}
                <td class="progress"><div></div></td>
                <td class="start"><button>Tải lên</button></td>
            {{/if}}
            <td class="cancel"><button>Hủy</button></td>
        </tr>
    </script>
    <script id="template-download" type="text/x-jquery-tmpl">
        <tr class="template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <td></td>
                <td class="name">${name}</td>
                <td class="size">${sizef}</td>
                <td class="error" colspan="2">Lỗi:
                    {{if error === 1}}File exceeds upload_max_filesize (php.ini directive)
                    {{else error === 2}}File exceeds MAX_FILE_SIZE (HTML form directive)
                    {{else error === 3}}File was only partially uploaded
                    {{else error === 4}}No File was uploaded
                    {{else error === 5}}Missing a temporary folder
                    {{else error === 6}}Failed to write file to disk
                    {{else error === 7}}File upload stopped by extension
                    {{else error === 'maxFileSize'}}File is too big
                    {{else error === 'minFileSize'}}File is too small
                    {{else error === 'acceptFileTypes'}}Filetype not allowed
                    {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                    {{else error === 'uploadedBytes'}}Uploaded bytes exceed file size
                    {{else error === 'emptyResult'}}Empty file upload result
                    {{else}}${error}
                    {{/if}}
                </td>
            {{else}}
                <td class="preview">
                    <a href="${url}" target="_blank" class="ui-icon-document ui-icon"></a>
                </td>
                <td class="name">
                    <a href="${url}"{{if thumbnail_url}} target="_blank"{{/if}}>${name}</a>
                </td>
                <td class="size">${sizef}</td>
                <td colspan="2" class="message">${message}</td>
            {{/if}}
            <td class="delete">
                <button data-type="DELETE">Xóa</button>
            </td>
        </tr>
    </script>
    """
