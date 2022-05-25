var data;
var language='English';
$.getJSON('/getNews', function(content){
    data = content;
    console.log(data);
    if(data['English']['politician'].length >= 2)
    {
        $("#politics1Title").text(data['English']['politician'][0]['title']);
        $("#politics1Summary").text(data['English']['politician'][0]['summary']);
        $("#politics2Title").text(data['English']['politician'][1]['title']);
        $("#politics2Summary").text(data['English']['politician'][1]['summary']);
    }
    if(data['English']['celebrity'].length >= 2)
    {
        $("#celebrity1Title").text(data['English']['celebrity'][0]['title']);
        $("#celebrity1Summary").text(data['English']['celebrity'][0]['summary']);
        $("#celebrity2Title").text(data['English']['celebrity'][1]['title']);
        $("#celebrity2Summary").text(data['English']['celebrity'][1]['summary']);
    }
    if(data['English']['business'].length >= 2)
    {
        $("#business1Title").text(data['English']['business'][0]['title']);
        $("#business1Summary").text(data['English']['business'][0]['summary']);
        $("#business2Title").text(data['English']['business'][1]['title']);
        $("#business2Summary").text(data['English']['business'][1]['summary']);
    }
    if(data['English']['sports'].length >= 3)
    {
        $("#sports1Title").text(data['English']['sports'][0]['title']);
        $("#sports1Summary").text(data['English']['sports'][0]['summary']);
        $("#sports2Title").text(data['English']['sports'][1]['title']);
        $("#sports2Summary").text(data['English']['sports'][1]['summary']);
        $("#sports3Title").text(data['English']['sports'][2]['title']);
        $("#sports3Summary").text(data['English']['sports'][2]['summary']);
    }
});
function changeLanguage(ele)
{
    if(ele.innerHTML=='Translate to Hindi')
    {
        if(data['Hindi']['politician'].length >= 2)
        {
            $("#politics1Title").text(data['Hindi']['politician'][0]['title']);
            $("#politics1Summary").text(data['Hindi']['politician'][0]['summary']);
            $("#politics2Title").text(data['Hindi']['politician'][1]['title']);
            $("#politics2Summary").text(data['Hindi']['politician'][1]['summary']);
        }
        if(data['Hindi']['celebrity'].length >= 2)
        {
            $("#celebrity1Title").text(data['Hindi']['celebrity'][0]['title']);
            $("#celebrity1Summary").text(data['Hindi']['celebrity'][0]['summary']);
            $("#celebrity2Title").text(data['Hindi']['celebrity'][1]['title']);
            $("#celebrity2Summary").text(data['Hindi']['celebrity'][1]['summary']);
        }
        if(data['Hindi']['business'].length >= 2)
        {
            $("#business1Title").text(data['Hindi']['business'][0]['title']);
            $("#business1Summary").text(data['Hindi']['business'][0]['summary']);
            $("#business2Title").text(data['Hindi']['business'][1]['title']);
            $("#business2Summary").text(data['Hindi']['business'][1]['summary']);
        }
        if(data['Hindi']['sports'].length >= 3)
        {
            $("#sports1Title").text(data['Hindi']['sports'][0]['title']);
            $("#sports1Summary").text(data['Hindi']['sports'][0]['summary']);
            $("#sports2Title").text(data['Hindi']['sports'][1]['title']);
            $("#sports2Summary").text(data['Hindi']['sports'][1]['summary']);
            $("#sports3Title").text(data['Hindi']['sports'][2]['title']);
            $("#sports3Summary").text(data['Hindi']['sports'][2]['summary']);
        }
        ele.innerHTML='Translate to English';
        language = 'Hindi';
    }
    else
    {
        if(data['English']['politician'].length >= 2)
        {
            $("#politics1Title").text(data['English']['politician'][0]['title']);
            $("#politics1Summary").text(data['English']['politician'][0]['summary']);
            $("#politics2Title").text(data['English']['politician'][1]['title']);
            $("#politics2Summary").text(data['English']['politician'][1]['summary']);
        }
        if(data['English']['celebrity'].length >= 2)
        {
            $("#celebrity1Title").text(data['English']['celebrity'][0]['title']);
            $("#celebrity1Summary").text(data['English']['celebrity'][0]['summary']);
            $("#celebrity2Title").text(data['English']['celebrity'][1]['title']);
            $("#celebrity2Summary").text(data['English']['celebrity'][1]['summary']);
        }
        if(data['English']['business'].length >= 2)
        {
            $("#business1Title").text(data['English']['business'][0]['title']);
            $("#business1Summary").text(data['English']['business'][0]['summary']);
            $("#business2Title").text(data['English']['business'][1]['title']);
            $("#business2Summary").text(data['English']['business'][1]['summary']);
        }
        if(data['English']['sports'].length >= 3)
        {
            $("#sports1Title").text(data['English']['sports'][0]['title']);
            $("#sports1Summary").text(data['English']['sports'][0]['summary']);
            $("#sports2Title").text(data['English']['sports'][1]['title']);
            $("#sports2Summary").text(data['English']['sports'][1]['summary']);
            $("#sports3Title").text(data['English']['sports'][2]['title']);
            $("#sports3Summary").text(data['English']['sports'][2]['summary']);
        }
        ele.innerHTML='Translate to Hindi';
        language = 'English';
    }
}
function speak()
{
    var englishSpeech = document.getElementById("englishSpeech");
    var hindiSpeech = document.getElementById("hindiSpeech");
    englishSpeech.load();
    hindiSpeech.load();
    if(language=='English')
    {
        englishSpeech.play();
    }
    else
    {
        hindiSpeech.play();
    }
}