// https://stackoverflow.com/a/73826022/1062668

function insertVersion(versions) {
    console.log(versions)
    var dl = document.getElementById('docs-versions');
    dl.innerHTML = ""

    $.each(versions, function (i, v) {
        var version = versions[i];
        dl.innerHTML = dl.innerHTML + `<dd><a href="${version.href}">${version.name}</a></dd>`
    });
}

$(document).ready(() => {
    if (!window.location.href.startsWith("file://")) {
        $.getJSON('../versions', function (data) {
            insertVersion(data)
        });
    }

    // TODO remove
    insertVersion([{name: "latest", href: "somewhere"}, {name: "stable", href: "somewhere"}])
})
