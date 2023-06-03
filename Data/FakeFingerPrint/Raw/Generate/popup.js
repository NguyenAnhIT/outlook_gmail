const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);
var listCookies = [];
document.addEventListener('DOMContentLoaded',function(){
    renderProfile()
    showCookies()
    saveCookies()
    buttonLoadCookie()
    btnClearCookies()
})


// Handel Show Cookies
function showCookies(){
    if(localStorage.check){
        $('#showCookie').value = localStorage.check;
    } else {
        chrome.tabs.getSelected(null,function(){
            chrome.cookies.getAll({url:"https://tots.fo4.garena.vn/"},function(cookies){
                var result = ''
                for (var cookie of cookies){
                    var cname = cookie.name;
                    var cvalue = cookie.value;
                    result += cname + '=' + cvalue + ';';
                };
                $('#showCookie').value = result;
            });
        });
    }
    
};


// Handel SaveCookies

function saveCookies(){
    
    var btnSaveCookies = $$('#SaveCookie');
    btnSaveCookies.forEach(function(btnSaveCookie,index){
        btnSaveCookie.onclick = () =>{
            chrome.tabs.query({active: true}, function(tabs){
                chrome.tabs.sendMessage(tabs[0].id, {name:'newFingerprint'});  
            });
        };
    });
};;


function addNewCookie(objCookie){
    //Handel Render To UI
    var divList = $('.rowslabel')
    var createDiv = document.createElement('div')
    createDiv.id = 'listcookies'
    var createSpan1 = document.createElement('span')
    createSpan1.className = 'btn-text'
    createSpan1.innerText = `Facebook: ${objCookie.name}`
    var createSpan2 = document.createElement('span')
    createSpan2.className = 'btn-remove'
    createSpan2.innerText = "X"
    createDiv.appendChild(createSpan1)
    createDiv.appendChild(createSpan2)
    divList.appendChild(createDiv)
    // Handel Clicked
    function buttonText(){
        var btnTexts = $$('.btn-text');
        btnTexts.forEach(function(btnText,index){
            btnText.onclick =  function(){
                listCookies = JSON.parse(localStorage.listCookies);   
                importCookies(listCookies[index].cookie)
                $('#showCookie').value = listCookies[index].cookie
                localStorage.check = listCookies[index].cookie
            }
        })
    };
    buttonText();
    //Handel RemoveClicked
    function buttonRemove(){
        var btnRemoves = $$('.btn-remove');
        btnRemoves.forEach(function(btnRemove,index){
            btnRemove.onclick = function(){
                listCookies = JSON.parse(localStorage.listCookies);
                listCookies.splice(index,1);
                localStorage.listCookies = JSON.stringify(listCookies);
                this.parentNode.remove();
            };
        });
    };
    buttonRemove();
};


//Auto Render Profile

function renderProfile(){
    if(localStorage.listCookies){
        listCookies = JSON.parse(localStorage.listCookies)
        for (var listCookie of listCookies){
            addNewCookie(listCookie);
        }
    }   
}


function addCookies(){
    var cookies = "_ga=GA1.1.1802978558.1658638061;_ga_W16BGTK74T=GS1.1.1658638060.1.1.1658638081.0;_ga=GA1.1.1802978558.1658638061;csrftoken=XMtOziX5bdb8LbZSfYPRiRQYZaNHGsRRrq4CLsFwYShZMJOl57l0ZEfuDMiiETME;sessionid=7g5tufmdesmrofvb2js411vtfnnevipv;_ga_W16BGTK74T=GS1.1.1658823103.2.0.1658823103.0;"
    for (var cookie of cookies.split(';')){
        var name = String(cookie.split('=')[0]);
        var value = String(cookie.split('=')[1]);
        setCookie(name,value)
    }
    alert('done')
    // var name = "csrftoken"
    // var value = "fDSvPo1otzvmeA0z94zTk7UZ6Lcmd82IatSZ3IzxrXWAIhHRumstZ8Gzs0eSlT4X"
    // chrome.cookies.set({url:'https://tots.fo4.garena.vn',name,value});
    // var name = "_ga"
    // var value = "GA1.1.224055198.1658638678"
    // chrome.cookies.set({url:'https://tots.fo4.garena.vn',name,value});
    // var name = "sessionid"
    // var value = "xpn2ulun2r1bfb3spezzjfk0ce29y7jz"
    // chrome.cookies.set({url:'https://tots.fo4.garena.vn',name,value});
    // var name = "_ga_W16BGTK74T"
    // var value = "GS1.1.1658638677.1.1.1658638700.0"
    // chrome.cookies.set({url:'https://tots.fo4.garena.vn',name,value});
    // console.log('done')
}



//Handel Import Cookies

function importCookies(cookie){
    clearCookies(function(){
        addCookies()})
         
    };
    

//Handel Btn-Loadcookie

function buttonLoadCookie(){
    var btnLoads = $$('#LoadCookies');
    btnLoads.forEach(function(btnLoad,index){
        btnLoad.onclick = function(){
            importCookies()
        }
    })
}

//Handel Btn ClearCookies

function btnClearCookies(){
    var btnClears = $$('#ClearCookie');
    btnClears.forEach(function(btnClear,index){
        btnClear.onclick = function(){
            chrome.cookies.getAll({},function(cookies){
                for (var cookie of cookies){
                    var url = "http" + (cookie.secure ? "s" : "") + "://" + cookie.domain + cookie.path;
                    chrome.cookies.remove({ "url": url, "name": cookie.name });        
                };
                alert('See You Again !');
                localStorage.check = []
            })
        };
        
    });

};

//handel ClearCookies 

function clearCookies(callback){
    if (!chrome.cookies) {
        chrome.cookies = chrome.experimental.cookies;
    }
    chrome.cookies.getAll({},function(cookies){
        for (var cookie of cookies){
            var url = "http" + (cookie.secure ? "s" : "") + "://" + cookie.domain + cookie.path;
            chrome.cookies.remove({ "url": url, "name": cookie.name });
        };
        callback()
    }); 
};


function setCookie(name,value){
    chrome.cookies.set({url:'https://tots.fo4.garena.vn',name,value})
    chrome.cookies.set({url:'https://.garena.vn',name,value});
}